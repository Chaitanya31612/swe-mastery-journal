FROM ruby:3.3.6-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev cmake pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /lab
COPY Gemfile Gemfile.lock* ./
RUN bundle install
COPY . .
EXPOSE 3000
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
