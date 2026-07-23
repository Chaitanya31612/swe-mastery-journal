# Rate Limiter LLD

## Problem Statement
Design a rate limiter that allows a given number of requests only and blocks others for a given user unless the requests tokens are replenished

## Usecase Flow / Requirements

- There are users, (maybe there are different rate limits based on user types - e.g. standard or premium)
- user makes a request (which is being rate limited per user), so given requests can be made, request are forwarded to the endpoint otherwise we return 429 (Too many requests)
- Different strategies for rate limiting - Fixed window, sliding window, token bucket, leaky bucket
  - fixed window: there are specified windows boundaries under which requests can be made only to the allowed count, and once the requests are made requests are blocked for the remainder of the window, for example if we have 3 requests allowed per hour, and user makes 3 requests in under 5 mins, he will be blocked for the remainder of the hour.
  - sliding window: solves shortcoming of fixed window which was, that requests can bulk up during the closing and opening of the window. For example if 3 requests are allowed per hour, user can make 3 requests in last 5 mins of the hour and next 3 requests in the first 5 mins of the next hour, effectively making 6 requests in 10 mins. Sliding window solves this by keeping track of requests in sliding window of last hour. Only allows requests if the count in the window is less than the permitted count.
  - token bucket: there is a bucket with specified number of tokens, when request comes, token is consumed, if no token is available, request is rejected. Tokens are refilled at a constant rate.
  - leaky bucket: It is primarliy used for making the requests at a constant rate rather than as they are coming, It uses queue for maintaining the requests upto a limit, above which requests are dropped. The requests in queue are processed at a constant rate. For example, given you are hitting a third party service api and they permit 3 requests per minute, so you can use this algo to make requests at a rate of 3 per minute by storing requests in the queue and processing them at a rate of 3 per minute.

## Core

- Users should be identified by id and can have type (standard or premium)
- rate limiter will have one method allowRequest(userId), which return true or false.

## Extensible

- The rate limiter can have multiple strategies and should be allowed to extend without modifying the existing structure. (OCP) (Strategy Pattern)
- The persistence can also use strategy pattern, like storing in memory or distributed storage like redis (ideal).

## Concurrency

- If two or more concurrent requests hit our rate limiter, it should be able to handle them gracefully
- Rate limiter should be thread safe

## Design Pattern
- Strategy Pattern for rate limiter algos
- Factory Pattern for creating rate limiters
- Builder pattern for creating the rate limiter config

## API

GET /v1/api/rate_limit?userId={userId}

Response
{
  "allow": boolean (true - allowed, false - rejected)
}

## Implementation

```java

class User {
  private String name;
  private int id;
  private UserType type;

  User(String name, int id, UserType type) {
    this.name = name;
    this.id = id;
    this.type = type;
  }

  public String getName() { return name;}
  public int getId() { return id;}
  public UserType getType() { return type;}
}

enum UserType {
  STANDARD,
  PREMIUM
}

enum RateLimitStrategyType {
  FIXED_WINDOW,
  SLIDING_WINDOW,
  TOKEN_BUCKET
}


class RateLimiterConfig {
  private int capacity;
  private int refillRate;
  private int timeWindow;
  private RateLimitStrategyType type;

  public RateLimiterConfig(int capacity, int refillRate, int timeWindow, RateLimitStrategyType type) {
    this.capacity = capacity;
    this.refillRate = refillRate;
    this.timeWindow = timeWindow;
    this.type = type;
  }

  public int getCapacity() { return capacity;}
  public int getRefillRate() { return refillRate;}
  public int getTimeWindow() { return timeWindow;}
  public RateLimitStrategyType getType() { return type;}
}

class RateLimiterFactory {
  public static RateLimiter create(RateLimiterConfig config) {

  }
}




class Driver {
  public static void main() {
    // RateLimiterConfig tokenBucketConfig = new RateLimiterConfig.Builder(3)
    //                                         .ofType(RateLimitStrategyType.TOKEN_BUCKET)
    //                                         .withRefillRate(1)
    //                                         .withTimeWindowInSeconds(60)
    //                                         .build();

    // RateLimiter rateLimiter = RateLimiterFactory.create(tokenBucketConfig);

    User standardUser = new User("Alice", 1, UserType.STANDARD);
    User premiumUser = new User("Bob", 2, UserType.PREMIUM);


    print(rateLimiter)

  }

  private static void print(String userId, String userName, boolean allowed) {
    String status = allowed ? "ALLOWED" : "REJECTED";
    System.out.println("User " + userName + " (" + userId + "): " + status);
  }
}

```
