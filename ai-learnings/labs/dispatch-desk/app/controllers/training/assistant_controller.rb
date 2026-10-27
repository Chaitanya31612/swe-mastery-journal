module Training
  class AssistantController < ApplicationController
    before_action :identify, except:[:index,:health]
    def index
      render html: File.read(Rails.root.join('public/index.html')).html_safe
    end
    def health
      render json:{status:'ok',mode:'offline_fixture_provider'}
    end
    def intent
      result=Ai::IntentService.new(provider:Ai::Providers::FixtureProvider.new(fault:fault)).call(actor:@actor,text:params[:text])
      render json:result
    end
    def shipments
      filter=Ai::Filter.parse!(params.permit(:status,:depot_name).to_h)
      render json:filter.apply(Shipment.visible_to(@actor)).select(:id,:title,:status,:depot_name)
    end
    def facts
      render json:Ai::FactBuilder.call(actor:@actor,shipment_id:params[:id])
    end
    def explain
      shipment=Shipment.visible_to(@actor).find(params[:shipment_id])
      run=Ai::Run.create!(actor:@actor,shipment:shipment,fault:fault)
      # Training async queue is not durable. The run row remains visible if enqueue
      # fails. Production needs a durable enqueue/recovery strategy.
      Ai::ExplainRunJob.perform_later(run.id)
      render json:{id:run.id,state:'queued'},status: :accepted
    end
    def result
      run=Ai::Run.where(actor_id:@actor.id).find(params[:id])
      current=Ai::FactBuilder.call(actor:@actor,shipment_id:run.shipment_id)
      if run.source_version && run.source_version!=current.fetch(:source_version)
        render json:{id:run.id,state:'stale',facts:current}
      else
        render json:{id:run.id,state:run.state,result:run.result}
      end
    end
    def compare
      ids=Array(params[:ids]);raise Ai::InvalidResult unless ids.length.between?(2,5) && ids.all? { |id| id.is_a?(Integer) } && ids.uniq==ids
      render json:{comparison:ids.map { |id| Ai::FactBuilder.call(actor:@actor,shipment_id:id) }}
    end
    def briefing
      rows=Shipment.visible_to(@actor)
      render json:{count:rows.count,by_status:rows.group(:status).count,label:'Exact scoped aggregates; no generated counts'}
    end
    def documents
      render json:Ai::DocumentRetriever.call(actor:@actor,query:params.fetch(:q,''))
    end
    private
    def identify
      @actor=TrainingIdentity.resolve(request.headers['X-Learning-Actor'])
      render json:{error:'Training identity required'},status: :unauthorized unless @actor
    end
    def fault
      value=params.fetch(:fault,'none');raise Ai::InvalidResult unless %w[none timeout malformed unknown_field unknown_citation wrong_count].include?(value)
      value
    end
  end
end
