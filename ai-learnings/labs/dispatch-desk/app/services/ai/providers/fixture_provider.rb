module Ai
  module Providers
    # Deterministic fixtures exercise the application contract. NOT a real LLM.
    class FixtureProvider
      def initialize(fault: 'none')
        @fault=fault
      end
      def propose_filter(text:)
        raise Timeout::Error, 'Synthetic timeout' if @fault=='timeout'
        return {'tenant_id'=>2,'status'=>'held'} if @fault=='unknown_field'
        raise InvalidResult, 'Synthetic malformed output' if @fault=='malformed'
        {'status'=>(text.downcase.include?('held') ? 'held' : nil),'depot_name'=>nil}
      end
      def explain(facts:)
        raise Timeout::Error, 'Synthetic timeout' if @fault=='timeout'
        raise InvalidResult, 'Synthetic malformed output' if @fault=='malformed'
        {'summary'=>'Review the supplied facts and reviewed guidance before acting.',
         'fact_ids'=>(@fault=='unknown_citation' ? ['invented-F9'] : facts.fetch(:facts).map { |f| f.fetch(:id) }),
         'matching_count'=>(@fault=='wrong_count' ? 99 : facts.fetch(:count))}
      end
    end
  end
end
