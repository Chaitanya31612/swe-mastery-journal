class ReadShipmentFactsTool < MCP::Tool
  description 'Read only the shipment facts permitted to this authenticated actor'
  input_schema(properties:{shipment_id:{type:'integer'}},required:['shipment_id'],additionalProperties:false)
  annotations(read_only_hint:true,destructive_hint:false)
  def self.call(shipment_id:,server_context:)
    actor=server_context.fetch(:actor)
    facts=Ai::FactBuilder.call(actor:actor,shipment_id:shipment_id)
    MCP::Tool::Response.new([{type:'text',text:JSON.generate(facts)}])
  rescue ActiveRecord::RecordNotFound
    MCP::Tool::Response.new([{type:'text',text:'Access or source unavailable'}],error:true)
  end
end
