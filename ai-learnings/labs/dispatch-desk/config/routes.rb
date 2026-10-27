Rails.application.routes.draw do
  get '/', to: 'training/assistant#index'
  get '/health', to: 'training/assistant#health'
  post '/training/intent', to: 'training/assistant#intent'
  get '/training/shipments', to: 'training/assistant#shipments'
  get '/training/shipments/:id/facts', to: 'training/assistant#facts'
  post '/training/explanations', to: 'training/assistant#explain'
  get '/training/runs/:id', to: 'training/assistant#result'
  post '/training/compare', to: 'training/assistant#compare'
  get '/training/briefing', to: 'training/assistant#briefing'
  get '/training/documents', to: 'training/assistant#documents'
  mount McpGateway.new => '/mcp'
end
