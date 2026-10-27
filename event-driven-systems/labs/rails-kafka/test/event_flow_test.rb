require 'test_helper'
class EventFlowTest < ActiveSupport::TestCase
  def setup
    @ticket = Ticket.create!(title: 'Synthetic test')
  end

  test 'duplicate command creates one durable event' do
    2.times { CompleteTicket.call(@ticket.id) }
    assert_equal 'completed', @ticket.reload.status
    assert_equal 1, OutboxEvent.where(aggregate_key: @ticket.id.to_s).count
  end

  test 'outbox failure rolls back business change' do
    OutboxEvent.stub(:create!, ->(**_) { raise 'simulated database failure' }) do
      assert_raises(RuntimeError) { CompleteTicket.call(@ticket.id) }
    end
    assert_equal 'open', @ticket.reload.status
    assert_equal 0, @ticket.event_version
  end

  test 'publish failure keeps intent pending' do
    CompleteTicket.call(@ticket.id)
    bad = Object.new
    def bad.publish(*, **); raise 'broker unavailable'; end
    assert_raises(RuntimeError) { OutboxDispatcher.new(bad).tick }
    assert_nil OutboxEvent.last.published_at
  end

  test 'delivery repeat applies projection once' do
    CompleteTicket.call(@ticket.id)
    event = OutboxEvent.last.envelope
    assert_equal :applied, ApplyReportingEvent.call(event)
    assert_equal :duplicate, ApplyReportingEvent.call(event)
    assert_equal 1, ReportingProjection.find_by!(ticket_id: @ticket.id).completed_count
  end

  test 'failure between inbox and effect rolls both back' do
    CompleteTicket.call(@ticket.id)
    event = OutboxEvent.last.envelope
    assert_raises(RuntimeError) { ApplyReportingEvent.call(event, after_inbox: -> { raise 'projection failed' }) }
    assert_not InboxEvent.exists?(event_id: event.fetch('event_id'))
    assert_not ReportingProjection.exists?(ticket_id: @ticket.id)
    assert_equal :applied, ApplyReportingEvent.call(event)
  end

  test 'unsupported event rejected before inbox' do
    assert_no_difference('InboxEvent.count') do
      assert_raises(ArgumentError) { ApplyReportingEvent.call({'schema_version' => 99}) }
    end
  end
end
