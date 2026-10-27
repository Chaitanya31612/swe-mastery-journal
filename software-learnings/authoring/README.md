# Content authoring

The journal Markdown and module metadata are the editable course source. Normal updates need only the app backend/pipeline/build_software_course.py builder. That builder reads approved journal paths and writes the two runtime catalogs.

expand_intermediate.py contains the original manually authored expansion as structured Python text. Running emit() rewrites its generated chapters. Run enrich_course.py afterward to attach the labs, diagrams, and curated order. Do not regenerate over manual edits without reviewing the diff. Existing module IDs stay stable for browser progress compatibility. These scripts never read the work repository.
