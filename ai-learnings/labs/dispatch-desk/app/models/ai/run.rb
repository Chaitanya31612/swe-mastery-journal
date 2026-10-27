module Ai
  class Run < ApplicationRecord
    self.table_name='ai_runs'
    belongs_to :actor
    belongs_to :shipment
  end
end
