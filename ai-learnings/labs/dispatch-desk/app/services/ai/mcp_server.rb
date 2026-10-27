module Ai
  class McpServer
    def self.for_actor(actor)
      MCP::Server.new(name:'dispatch_training',version:'1.0.0',
        tools:[ReadShipmentFactsTool],server_context:{actor:actor})
    end
  end
end
