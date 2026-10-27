Actor.find_or_create_by!(handle: 'operator-a') { |a| a.tenant_id = 1 }
Actor.find_or_create_by!(handle: 'operator-b') { |a| a.tenant_id = 2 }
Shipment.find_or_create_by!(title: 'Synthetic camera parcel') { |s| s.assign_attributes(tenant_id: 1,depot_name:'East Yard',status:'held',address_complete:false,label_printed:true) }
Shipment.find_or_create_by!(title: 'Synthetic book parcel') { |s| s.assign_attributes(tenant_id: 1,depot_name:'West Yard',status:'held',address_complete:true,label_printed:false) }
Shipment.find_or_create_by!(title: 'Synthetic foreign parcel') { |s| s.assign_attributes(tenant_id: 2,depot_name:'East Yard',status:'held',address_complete:false,label_printed:false) }
PolicyDocument.find_or_create_by!(title:'Dispatch labels',tenant_id:1) { |d| d.assign_attributes(source_version:'v1',body:'Dispatch requires a complete address and a printed label.',embedding:'[1,0,0]') }
PolicyDocument.find_or_create_by!(title:'Returns policy',tenant_id:1) { |d| d.assign_attributes(source_version:'v1',body:'Returns use the published returns policy, not dispatch guidance.',embedding:'[0,1,0]') }
PolicyDocument.find_or_create_by!(title:'Other tenant dispatch',tenant_id:2) { |d| d.assign_attributes(source_version:'v1',body:'Synthetic other-tenant dispatch text must not enter tenant one context.',embedding:'[1,0,0]') }
