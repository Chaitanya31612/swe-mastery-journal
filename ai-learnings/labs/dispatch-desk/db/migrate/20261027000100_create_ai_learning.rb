class CreateAiLearning < ActiveRecord::Migration[7.2]
  def change
    enable_extension 'vector'
    create_table :actors do |t|
      t.string :handle, null: false
      t.integer :tenant_id, null: false
      t.boolean :active, null: false, default: true
    end
    add_index :actors, :handle, unique: true
    create_table :shipments do |t|
      t.integer :tenant_id, null: false
      t.string :title, null: false
      t.string :depot_name, null: false
      t.string :status, null: false
      t.boolean :address_complete, null: false, default: false
      t.boolean :label_printed, null: false, default: false
      t.timestamps
    end
    create_table :policy_documents do |t|
      t.integer :tenant_id, null: false
      t.string :title, null: false
      t.string :source_version, null: false
      t.text :body, null: false
      t.boolean :published, null: false, default: true
      t.column :embedding, 'vector(3)'
    end
    create_table :ai_runs do |t|
      t.references :actor, null: false, foreign_key: true
      t.references :shipment, null: false, foreign_key: true
      t.string :state, null: false, default: 'queued'
      t.string :source_version
      t.string :fault, null: false, default: 'none'
      t.jsonb :result, null: false, default: {}
      t.timestamps
    end
  end
end
