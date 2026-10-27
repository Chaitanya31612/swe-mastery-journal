class PolicyDocument < ApplicationRecord
  def self.visible_to(actor)
    current_actor = Actor.find_by(id: actor.id, active: true)
    current_actor ? where(tenant_id: current_actor.tenant_id, published: true) : none
  end
end
