## Follow a concrete example

```dockerfile
FROM ruby:3.3-slim
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
CMD ["bundle", "exec", "puma", "-C", "config/puma.rb"]
```

This is a teaching shape, not the complete lab Dockerfile. Add required system libraries, user/permissions, .dockerignore, and a deliberate release image/digest policy. Never COPY the work project or its secrets into this lab.
