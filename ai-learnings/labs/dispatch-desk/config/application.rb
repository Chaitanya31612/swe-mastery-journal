require_relative 'boot'
require 'rails'
require 'active_record/railtie'
require 'action_controller/railtie'
require 'active_job/railtie'
require 'rails/test_unit/railtie'
Bundler.require(*Rails.groups)
module AiLearning
  class Application < Rails::Application
    config.load_defaults 7.2
    config.api_only = true
    config.eager_load = true
    config.autoload_lib(ignore: %w[assets tasks])
    config.secret_key_base = ENV.fetch('SECRET_KEY_BASE', 'local_training_only')
    config.hosts = ['localhost','127.0.0.1','web','www.example.com']
    config.active_job.queue_adapter = ENV['RAILS_ENV']=='test' ? :test : :async
    config.logger = ActiveSupport::Logger.new($stdout)
  end
end
