## Walk through an example

An agent proposes adding a review note to shipment 14 at version 3. The user approves. Before execution, another user changes the shipment to version 4. Do not silently apply the old plan just because the approve button was clicked.

An approval token should represent the approved operation, not merely “this chat once had approval.”
