require 'digest'
module Ai
  class FactBuilder
    RULE_VERSION='warehouse-rules-v1'
    def self.call(actor:,shipment_id:)
      shipment=Shipment.visible_to(actor).find(shipment_id)
      reason=if !shipment.address_complete then 'address_missing'
             elsif !shipment.label_printed then 'label_missing'
             else 'no_supported_blocker' end
      version=Digest::SHA256.hexdigest([shipment.id,shipment.updated_at.utc.iso8601(6),shipment.status,shipment.address_complete,shipment.label_printed,RULE_VERSION].to_json)
      {source_version:version,rule_version:RULE_VERSION,count:1,
       facts:[{id:"shipment-#{shipment.id}",shipment_id:shipment.id,status:shipment.status,reason_code:reason}],
       reviewed_guidance: {'address_missing'=>'Review the address in the normal editor.',
         'label_missing'=>'Review the label workflow.', 'no_supported_blocker'=>'No covered cause; inspect with a human.'}.fetch(reason)}
    end
  end
end
