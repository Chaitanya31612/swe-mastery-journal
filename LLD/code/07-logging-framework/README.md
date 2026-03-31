# 📝 Problem 07: Logging Framework (Log4j-style)

> **Frequency:** 🟡 P1 | **Time:** 90 min | **Difficulty:** ⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Log levels: **DEBUG**, **INFO**, **WARNING**, **ERROR**, **FATAL**
2. Multiple **log handlers**: Console, File, Database
3. Each handler has a **minimum log level** (e.g., File only logs WARNING+)
4. Log messages flow through a **chain** of handlers
5. **Timestamped** log messages with level and message
6. Support for **log formatting** (customizable output format)

### Nice-to-Have
- Asynchronous logging
- Log rotation (max file size)
- Configurable via file/properties
- Thread-safe logging

---

## 🧩 Key Entities

```
Logger, LogLevel, LogMessage, LogHandler (abstract),
ConsoleHandler, FileHandler, DatabaseHandler
```

## 🏗️ Class Diagram

```
┌───────────────┐     ┌───────────────────┐
│    Logger     │────>│   <<abstract>>    │
├───────────────┤     │    LogHandler     │
│ -handlerChain │     ├───────────────────┤
├───────────────┤     │ -level: LogLevel  │
│ +debug(msg)   │     │ -nextHandler      │
│ +info(msg)    │     ├───────────────────┤
│ +warn(msg)    │     │ +handle(msg)      │
│ +error(msg)   │     │ +setNext(handler) │
│ +fatal(msg)   │     │ #write(msg)       │ ← abstract
└───────────────┘     └────────▲──────────┘
                               ┊
                  ┌────────────┼────────────┐
                  ┊            ┊            ┊
           ┌──────┴───┐ ┌─────┴────┐ ┌─────┴──────┐
           │ Console  │ │   File   │ │  Database  │
           │ Handler  │ │  Handler │ │  Handler   │
           └──────────┘ └──────────┘ └────────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Chain of Responsibility** | LogHandler chain | Message flows through handlers |
| **Singleton** | Logger instance | Single logger per application |
| **Decorator** | Formatting, encryption | Add behavior to log output |

## 🔑 Key Design Decisions
- **Chain of Responsibility** is the star pattern here
- Each handler decides whether to process AND whether to forward
- **LogLevel ordering** — DEBUG < INFO < WARNING < ERROR < FATAL
- Handler processes message if `message.level >= handler.level`

## 📁 Code Structure
```
src/
├── model/
│   ├── LogLevel.java
│   └── LogMessage.java
├── handler/
│   ├── LogHandler.java
│   ├── ConsoleLogHandler.java
│   ├── FileLogHandler.java
│   └── DatabaseLogHandler.java
├── Logger.java
└── LoggingDemo.java
```
