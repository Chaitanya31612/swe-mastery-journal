# Editing the AI course

The chapter folders and their Markdown/JSON files are the editable source of truth. The app builder reads them without executing their examples.

`build_chapters.py` is the original drafting recipe. It seeds the initial source and overwrites chapter files. Do not run it over later manual edits unless you intend to regenerate and then reapply those edits. The final capstone and lab guides were refined after that initial draft.

`enrich_chapters.py` refreshes the selected overview diagrams and cumulative quiz entries. It removes/replaces its derived `review-` questions, so repeated runs do not duplicate them. Practice answers remain in separate answers folders.

The normal publish command is `python3 backend/pipeline/build_ai_course.py` from the app repository. It bundles current source into the frontend and backend runtime copies. Run the catalog tests afterward. No build command reads or executes a work project.
