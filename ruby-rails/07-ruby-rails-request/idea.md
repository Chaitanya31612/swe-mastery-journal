# The idea

Rails connects a Rack request to a route, a controller action, model work, and a response. A before_action can establish a current user.

It does not automatically limit every database lookup to that user.

Strong parameters select attributes allowed for mass assignment. They do not authorize access to a particular row.

Scope the lookup to the caller’s allowed records, then check action permissions.

A service object is an ordinary Ruby object that can organize one use case without making the controller or model do everything.

The work baseline is Rails 4.2: use params.require(...).permit(...), not modern params.expect. ApplicationRecord is a later convention; models here can inherit ActiveRecord::Base.

These version differences are part of the lesson, not typos.