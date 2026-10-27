## Break it and reason about the repair

A container listening only on 127.0.0.1 may not accept the intended Pod-network traffic. An Ingress without its controller is only desired routing data.

**Remember:** Name → route → Service → ready endpoint → listener.