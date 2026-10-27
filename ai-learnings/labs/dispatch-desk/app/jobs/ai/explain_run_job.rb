module Ai
  class ExplainRunJob < ApplicationJob
    def perform(id)
      run=Run.find(id)
      claimed=run.with_lock do
        next false unless run.state=='queued'
        run.update!(state:'running');true
      end
      return unless claimed
      # No database lock is held during model work. This local demo has no lease
      # recovery for abandoned running jobs; the durable-agents exercise adds it.
      actor=Actor.find(run.actor_id)
      facts=FactBuilder.call(actor:actor,shipment_id:run.shipment_id)
      provider=Providers::FixtureProvider.new(fault:run.fault)
      result=ExplanationService.new(provider:provider).call(facts:facts)
      run.update!(state:result.fetch(:state),source_version:facts.fetch(:source_version),result:result)
    rescue ActiveRecord::RecordNotFound
      run&.update!(state:'unavailable',result:{label:'Access or source unavailable'})
    end
  end
end
