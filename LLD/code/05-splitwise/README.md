# 💰 Problem 05: Splitwise (Expense Sharing)

> **Frequency:** 🟡 P1 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Users can **add expenses** (who paid, how much, who owes)
2. Split types: **EQUAL**, **EXACT** (specific amounts), **PERCENTAGE**
3. Track **balances** between users (who owes whom how much)
4. Show **individual balances** for any user
5. **Simplify debts** — minimize number of transactions

### Nice-to-Have
- Groups (trip expenses, roommates)
- Currency support
- Activity log / history
- Settlement (mark as paid)

---

## 🧩 Key Entities

```
User, Expense, Split (EqualSplit, ExactSplit, PercentSplit),
ExpenseManager, BalanceSheet
```

## 🏗️ Class Diagram

```
┌───────────────┐     ┌──────────────┐
│ExpenseManager │1──*│   Expense    │
├───────────────┤     ├──────────────┤
│ -users        │     │ -paidBy      │
│ -expenses     │     │ -amount      │
│ -balances     │     │ -splits      │
├───────────────┤     │ -type        │
│ +addExpense() │     │ -description │
│ +getBalance() │     └──────────────┘
│ +simplify()   │
└───────────────┘     ┌──────────────┐
                      │   <<abs>>    │
┌───────────┐         │    Split     │
│   User    │         ├──────────────┤
├───────────┤         │ -user        │
│ -id       │         │ -amount      │
│ -name     │         └──────▲───────┘
│ -email    │                ┊
└───────────┘           ┌────┼─────┐
                        │    │     │
                  ┌─────┴┐ ┌┴───┐ ┌┴──────┐
                  │Equal ││Exact││Percent│
                  │Split ││Split││Split  │
                  └──────┘└────┘ └───────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | Split calculation (Equal, Exact, Percent) | Different split logic |
| **Factory** | SplitFactory | Create correct split type |
| **Observer** | Notifications on new expense | Alert affected users |

## 🔑 Key Design Decisions
- **Balance map** — `Map<(userA, userB), double>` to track who owes whom
- **Split validation** — Exact amounts must sum to total; percentages must sum to 100
- **Debt simplification** — Algorithm to minimize transactions (net settlements)
- **Immutable expenses** — Once added, expenses shouldn't be modified

## 📁 Code Structure
```
src/
├── model/
│   ├── User.java
│   ├── Expense.java
│   ├── ExpenseType.java
│   ├── Split.java
│   ├── EqualSplit.java
│   ├── ExactSplit.java
│   └── PercentSplit.java
├── service/
│   ├── ExpenseManager.java
│   ├── BalanceSheet.java
│   └── SplitValidator.java
└── SplitwiseDemo.java
```
