## Walk through an example

Compare shipments 14 and 15 across address_complete, label_printed and route_supported. One field is not available for 15. Render that state explicitly; do not let the model interpret it as false.

A briefing groups held shipments by verified reason: address_missing: 3, label_missing: 2. These values are supplied facts, not a request for the model to count a list.
