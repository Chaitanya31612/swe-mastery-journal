Rails.application.routes.draw do
  get '/health', to: 'tickets#health'
  get '/tickets/:id', to: 'tickets#show'
  post '/tickets/:id/complete', to: 'tickets#complete'
end
