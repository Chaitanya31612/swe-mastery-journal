Rails.application.configure do
  config.log_level = :warn
  config.logger = ActiveSupport::Logger.new($stderr)
  config.consider_all_requests_local = true
  config.action_dispatch.show_exceptions = :none
end
