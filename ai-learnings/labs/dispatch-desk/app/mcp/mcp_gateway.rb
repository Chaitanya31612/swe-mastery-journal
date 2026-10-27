class McpGateway
  def call(env)
    # Local synthetic identity only. Production requires supported auth middleware
    # and current principal/policy binding; a caller-selected header is NOT auth.
    actor=TrainingIdentity.resolve(env['HTTP_X_LEARNING_ACTOR'])
    return [401,{'content-type'=>'application/json'},['{"error":"training identity required"}']] unless actor
    origin=env['HTTP_ORIGIN']
    allowed=['http://127.0.0.1:3310','http://localhost:3310']
    return [403,{'content-type'=>'application/json'},['{"error":"origin rejected"}']] if origin && !allowed.include?(origin)
    server=Ai::McpServer.for_actor(actor) # no global mutable current_user
    transport=MCP::Server::Transports::StreamableHTTPTransport.new(server,stateless:true,enable_json_response:true)
    transport.call(env)
  end
end
