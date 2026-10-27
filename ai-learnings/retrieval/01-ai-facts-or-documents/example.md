## Walk through an example

Question A: “How many held parcels are in this depot now?” → authorized SQL count.

Question B: “What does the fragile-item policy require?” → published policy retrieval with source version.

Question C: “Why is parcel 14 held?” → scoped parcel lookup and a verified rule; policy context may explain the next step.