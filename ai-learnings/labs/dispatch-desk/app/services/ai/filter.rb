module Ai
  class Filter
    FIELDS = %w[status depot_name].freeze
    def self.parse!(value)
      raise InvalidResult, 'Expected object' unless value.is_a?(Hash)
      raise InvalidResult, 'Unsupported field' unless (value.keys-FIELDS).empty?
      status, depot = value.values_at('status','depot_name')
      raise InvalidResult, 'Invalid status' unless status.nil? || %w[open held released].include?(status)
      raise InvalidResult, 'Invalid depot' unless depot.nil? || (depot.is_a?(String) && depot.length.between?(1,80))
      new(status, depot)
    end
    def initialize(status,depot)
      @status,@depot=status,depot
    end
    def apply(relation)
      relation=relation.where(status:@status) if @status
      relation=relation.where(depot_name:@depot) if @depot
      relation
    end
    def to_h
      {status:@status,depot_name:@depot}
    end
  end
end
