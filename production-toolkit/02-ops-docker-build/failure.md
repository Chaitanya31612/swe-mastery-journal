## Break it and reason about the repair

Deleting a secret in a later layer does not erase it from earlier layers. A mutable base/tag can change rebuild output. A shell that does not exec can interfere with signal forwarding.

**Remember:** Cache stable inputs. Keep secrets out. Let signals reach the app.
