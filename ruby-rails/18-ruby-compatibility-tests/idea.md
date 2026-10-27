## Understand the idea

Start by recording exact Ruby, Rails, gem, database, and frontend versions. A fork may differ from upstream.

A copied snippet is a hypothesis until the relevant boundary test runs in an authorized isolated environment.

Common seams deserve explicit tests: keyword forwarding, autoload/reload, callback order, job serialization, database constraints, request error mapping, and browser component behavior. Keep legacy behavior separate from a deliberate modernized lab.

Characterization tests record what the system currently does. They are useful before refactoring, but do not make a defect desirable forever.

Mark a known bad behavior as a decision to change with a new intended contract.