module Ai
  class IntentService
    def initialize(provider:)
      @provider=provider
    end
    def call(actor:,text:)
      raise InvalidResult, 'Input too large' unless text.is_a?(String) && text.length.between?(1,2000)
      filter=Filter.parse!(@provider.propose_filter(text:text))
      rows=filter.apply(Shipment.visible_to(actor))
      {state:'accepted',filter:filter.to_h,count:rows.count}
    rescue InvalidResult, Timeout::Error
      {state:'unavailable',manual_path:'Use the ordinary status and depot filters.'}
    end
  end
end
