class ApplyReportingEvent
  CONSUMER = 'reporting-v1'

  def self.call(event, after_inbox: nil)
    TicketEvent.validate!(event)
    ApplicationRecord.transaction do
      InboxEvent.create!(consumer_name: CONSUMER, event_id: event.fetch('event_id'))
      after_inbox&.call # deterministic failure seam used only in tests
      projection = ReportingProjection.find_or_create_by!(ticket_id: event.fetch('data').fetch('ticket_id'))
      projection.with_lock do
        projection.update!(completed_count: projection.completed_count + 1,
                           last_version: event.fetch('aggregate_version'))
      end
    end
    :applied
  rescue ActiveRecord::RecordNotUnique
    # Rescue outside the aborted PostgreSQL transaction. Do not hide unrelated
    # unique violations as a successful delivery duplicate.
    raise unless InboxEvent.exists?(consumer_name: CONSUMER, event_id: event.fetch('event_id'))
    :duplicate
  end
end
