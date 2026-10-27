module Ai
  class BoundedAgent
    def initialize(planner:,tools:,max_steps:4)
      @planner,@tools,@max_steps=planner,tools,max_steps
    end
    def call(actor:)
      observations=[]
      @max_steps.times do
        proposal=@planner.call(observations)
        return {state:'denied',reason:'malformed_proposal'} unless proposal.is_a?(Hash) && %w[tool final].include?(proposal[:type])
        return {state:'completed',observations:observations} if proposal[:type]=='final'
        return {state:'denied',reason:'unsupported_tool'} unless proposal[:name]=='read_shipment_facts'
        args=proposal[:arguments]
        return {state:'denied',reason:'invalid_arguments'} unless args.is_a?(Hash) && args.keys==[:shipment_id] && args[:shipment_id].is_a?(Integer)
        observations << @tools.call(actor:actor,shipment_id:args[:shipment_id])
      end
      {state:'partial',reason:'step_limit',observations:observations}
    rescue ActiveRecord::RecordNotFound
      {state:'denied',reason:'access_or_source_unavailable'}
    end
  end
end
