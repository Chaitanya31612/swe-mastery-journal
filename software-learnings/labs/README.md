# Run a small, separate lab

Use this folder, never the work application. The examples use synthetic data. None reads the work repository or connects to a production database.

```sh
ruby ruby_lab.rb
node frontend_lab.mjs
python3 git_lab.py
```

Ruby: predict each assertion first. Break the hash default, keyword forwarding, or prepend choice and observe the failing test. Then repair it without looking at the original.

Frontend: change the order of promise resolution. Remove only the loading identity guard and observe the failing assertion. Write a test for old-error/new-success as a transfer exercise.

Git: this script creates and deletes only its own temporary repository. It proves staged A versus working B and recovery via a rescue name. For hands-on history, use a fresh scratch repository and the existing [15 Git labs](../../GIT/exercises/01-practice-labs.md). Read each command before running it. Keep the answers closed until your attempt.

Spring: [task-service](../../spring-boot/labs/task-service/README.md) is a separate Maven project. It runs an in-memory H2 training database. It is not a deployment template.

Rails: the lesson fragments require Rails, models, routes, authentication, and a test database. They are marked as fragments. For hands-on integration, create a separate authorized training app and implement the capstone contract. Do not install an old Rails environment into the work checkout for this course.
