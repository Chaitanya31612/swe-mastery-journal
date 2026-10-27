ENV['RAILS_ENV'] = 'test'
require_relative '../config/environment'
abort 'Tests require a separate test database' unless ActiveRecord::Base.connection_db_config.database.end_with?('_test')
require 'rails/test_help'
require 'minitest/mock'
class ActiveSupport::TestCase
  parallelize(workers: 1)
end
