module Ai
  class ExplanationService
    def initialize(provider:)
      @provider=provider
    end
    def call(facts:)
      proposal=@provider.explain(facts:facts)
      raise InvalidResult unless proposal.is_a?(Hash) && proposal.keys.sort==%w[fact_ids matching_count summary].sort
      ids=proposal['fact_ids'];allowed=facts.fetch(:facts).map { |f| f.fetch(:id) }
      raise InvalidResult unless ids.is_a?(Array) && ids.any? && ids.uniq==ids && (ids-allowed).empty?
      raise InvalidResult unless proposal['matching_count']==facts.fetch(:count)
      raise InvalidResult unless proposal['summary'].is_a?(String) && proposal['summary'].length.between?(1,600)
      # These checks validate provenance membership and an exact count, NOT the
      # semantic truth of arbitrary summary text. The product label reflects it.
      {state:'completed',label:'AI draft - review interpretation',summary:proposal['summary'],facts:facts}
    rescue InvalidResult, Timeout::Error
      {state:'fallback',label:'Model explanation unavailable',facts:facts,
       summary:facts.fetch(:reviewed_guidance)}
    end
  end
end
