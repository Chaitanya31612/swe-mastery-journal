class CreateEventLearning < ActiveRecord::Migration[7.2]
  def change
    create_table :tickets do |t|
      t.string :title, null: false
      t.string :status, null: false, default: 'open'
      t.integer :event_version, null: false, default: 0
      t.timestamps
    end
    create_table :outbox_events do |t|
      t.string :event_id, null: false
      t.string :aggregate_key, null: false
      t.jsonb :envelope, null: false
      t.datetime :published_at
      t.timestamps
    end
    add_index :outbox_events, :event_id, unique: true
    create_table :inbox_events do |t|
      t.string :consumer_name, null: false
      t.string :event_id, null: false
      t.timestamps
    end
    add_index :inbox_events, [:consumer_name, :event_id], unique: true
    create_table :reporting_projections do |t|
      t.bigint :ticket_id, null: false
      t.integer :completed_count, null: false, default: 0
      t.integer :last_version, null: false, default: 0
      t.timestamps
    end
    add_index :reporting_projections, :ticket_id, unique: true
  end
end
