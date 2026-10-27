## Understand the idea

A consumer group shares partition responsibility among its members. A different group has independent progress and can read the same retained records. Within a group, one assigned member normally owns a partition at a time under the selected group protocol.

Distinguish fetched position, a client’s stored progress, and committed group offsets. Exact APIs vary by library. A committed offset conventionally identifies the next record to resume from, not the last business event ID.

Process the durable effect before committing the relevant completed progress. A crash after effect but before commit replays it. Committing too early can skip unfinished work after a crash. Auto offset reset applies when there is no usable committed position; earliest does not rewind a healthy group on every restart.
