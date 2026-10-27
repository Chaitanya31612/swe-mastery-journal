ENV['RAILS_ENV']='test'
require_relative '../config/environment'
abort 'Separate test database required' unless ActiveRecord::Base.connection_db_config.database.end_with?('_test')
require 'rails/test_help'
require 'minitest/mock'
class ActiveSupport::TestCase
  parallelize(workers:1)
  include ActiveJob::TestHelper
  def fixtures_for_lab
    @a=Actor.create!(handle:'test-a',tenant_id:100,active:true)
    @b=Actor.create!(handle:'test-b',tenant_id:200,active:true)
    @shipment=Shipment.create!(title:'Synthetic test parcel',tenant_id:100,depot_name:'East Yard',status:'held',address_complete:false,label_printed:true)
    @foreign=Shipment.create!(title:'Synthetic forbidden parcel',tenant_id:200,depot_name:'East Yard',status:'held',address_complete:false,label_printed:false)
  end
end
