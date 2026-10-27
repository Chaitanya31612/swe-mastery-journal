require 'test_helper'
class TicketsApiTest < ActionDispatch::IntegrationTest
  test 'HTTP completion persists event without broker call' do
    ticket = Ticket.create!(title: 'API sample')
    post "/tickets/#{ticket.id}/complete"
    assert_response :success
    assert_equal 'completed', response.parsed_body.fetch('status')
    assert OutboxEvent.exists?(aggregate_key: ticket.id.to_s)
  end
end
