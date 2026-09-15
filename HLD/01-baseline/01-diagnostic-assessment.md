# Diagnostic Baseline: Where Do You Stand Today? (Phase 0)

> **Welcome!** Think of this like a quick chat over coffee before we start building things.  
> There are no grades here, no trick questions, and no one is judging you.  
> **Goal:** Figure out what you already know instinctively, what's a bit rusty, and what we should focus on so you don't waste time on stuff you've already mastered.  
> **How to take this:** Don't Google anything! Just answer in 1 to 3 simple sentences off the top of your head. If you don't know something, just say *"Never worked with this"* or *"Fuzzy on this"*. That's 100% fine.

---

## Part A: Quick Concept Check (10 Questions)

1. **Latency vs. Throughput:** Imagine a highway. How would you explain the difference between how fast one car can drive vs. how many cars pass by in an hour? Can you have a road where cars drive fast, but very few cars can fit?
2. **Horizontal vs. Vertical Scaling:** When someone says *"Just buy a bigger AWS box"*, why can't we do that forever? When are you forced to buy multiple smaller machines instead?
3. **Replication vs. Partitioning (Sharding):** If you copy your notebook 3 times and give copies to 3 friends, what is that? If you tear your notebook into 3 chunks and give one chunk to each friend, what is that? Why do we do both in databases?
4. **Cache vs. Database:** Both hold data in memory or disk. But what's the big difference in what happens if the server suddenly loses power?
5. **Message Queue vs. Pub/Sub:** If 3 workers are listening to a Queue and 1 message arrives, who gets it? What if they were listening to a Pub/Sub Topic instead?
6. **SQL vs. NoSQL:** A coworker tells you *"NoSQL is modern and always faster than SQL"*. How would you explain to them why that's not necessarily true?
7. **Synchronous vs. Asynchronous:** When you call someone on the phone and wait for them to pick up vs. sending them a text message. How does choosing phone calls (sync) hurt your system if the other person is slow to answer?
8. **Strong vs. Eventual Consistency:** You update your profile picture. Under Strong Consistency, what does your friend see 1 millisecond later? Under Eventual Consistency, what might they see for a few seconds?
9. **Available vs. Reliable:** Can an API return a fast `200 OK` response with empty `{}` data and technically be "100% available", but completely useless and unreliable to the user?
10. **Durability vs. Availability:** If your database server freezes up and refuses all new writes so it doesn't corrupt or lose existing money transfers, which one is it choosing: Durability or Availability?

---

## Part B: Real-World "What Would You Do?" (8 Questions)

11. **Database is melting on Reads:** Your Postgres database CPU is at 95% because millions of users are reading products. What are 3 practical things you'd try, starting from the easiest/cheapest?
12. **Slow API, but CPU is barely working:** An API is taking 3 seconds to respond, but when you check Datadog, CPU is at 7% and RAM is at 15%. What on earth is the server doing for 3 seconds?
13. **Messages piling up in Kafka:** You have 10 worker servers reading from Kafka, but messages are piling up faster than they can process them. What happens if you don't fix it, and what's your game plan?
14. **Someone bought the last iPhone:** An e-commerce site caches product inventory in Redis. Redis says 1 item is left in stock. But two people click "Buy Now" at the exact same second. What goes wrong, and how do you stop them both from buying it?
15. **Too many writes to handle:** 100,000 smart electric meters send a reading every single second. A standard SQL database is choking on disk writes. What kind of database or trick would you reach for?
16. **The Domino Effect (Cascading Outage):** Service A calls Service B, which calls Service C. Service C slows to a crawl. Walk through how this can knock down Service A, and what safety valve stops it.
17. **The Celebrity Problem (Hot Shard):** You shard your database by `user_id`. Normal users have 200 followers. One day, a celebrity with 80 million followers posts a photo. What happens to the specific machine holding that celebrity's data?
18. **Network Cut in Half (Split-Brain):** You have 2 database servers in New York and 2 in London. The underwater ocean cable between them gets cut. If both sides think the other died and both try to be the boss, what bad thing happens to customer data?

---

## Part C: Quick Napkin Sketches (4 Questions)

19. **TinyURL:** Someone gives you a long link and wants a short one (`tiny.url/xyz123`). When someone clicks the short link, how does your system send them to the real site? What's the main thing that could slow it down?
20. **Who's Online?** You're building a chat app for 5 million users. How do you show a little green dot next to users who are currently active? How do you know when someone closed their laptop or lost signal?
21. **Don't Lose the Receipt:** When an e-commerce order succeeds, you must send an email receipt. If the email provider (like SendGrid) is down, how do you make sure the user's checkout doesn't fail, but the email still goes out later?
22. **Rate Limiter:** Where should a rate limiter live (in the mobile app, at the front door/gateway, inside the service code, or in the database)? Why?

---

## What We Do With Your Answers

Once you jot down your thoughts, we'll turn them into a clear personal roadmap:
* What you already have rock-solid intuition for
* The few tricky concepts where things feel fuzzy
* Exactly which phases we can breeze through, and where we'll spend extra time having fun breaking down architectures!
