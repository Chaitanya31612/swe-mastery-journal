# 10. Services, transactions, locks, and callbacks

Trace a Rails transaction and explain what after_commit does and does not promise.

Version: Ruby 2.7.8 · Rails 4.2.11.3 · Sidekiq 5.2. Budget: about 3 hours, including hands-on practice.

- [The idea](idea.md)
- [A small example](example.md)
- [Follow the execution](trace.md)
- [What can go wrong](failure.md)
- [Repair practice](practice/repair.md)
- [Changed-condition practice](practice/transfer.md)

Take the quiz in the application. Reference answers are in answers/; open them after an honest attempt.

A reference is one valid argument, not the only acceptable design.

## Reading map

Metaprogramming Ruby Rails tour: concerns and hooks

- [Rails 4.2 callbacks](https://guides.rubyonrails.org/v4.2/active_record_callbacks.html)
- [Rails 4.2 query interface](https://guides.rubyonrails.org/v4.2/active_record_querying.html)
