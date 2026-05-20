# Splitwise: The Master's Interview Playbook

This guide focuses on **the pattern of communication and thought** required to crush the Splitwise LLD interview. This problem is heavily focused on Object-Oriented Design patterns, float precision, and data structures.

---

## 🧠 The 5-Phase Interview Pattern
1. **Harvest & Clarify (5-7 mins):** Understand the math. Ask about rounding and netting out debts.
2. **Entity & Relationship Mapping (5-10 mins):** Identify the core ledgers and split types.
3. **Architecture & Patterns (5-10 mins):** Propose the Strategy Pattern for splits early. It proves you understand extensibility.
4. **Core Implementation (15-20 mins):** Implement the math cleanly. Keep calculation separate from state mutation.
5. **Review & Scale (5 mins):** Discuss graph algorithms (Simplify Debts) and Database ACID transactions.

---

## Step 1: Requirement Harvest

**🧠 The Master's Approach:** Show that you understand this is a Fintech-lite problem. Mention precision and auditability early.

**🗣️ Interviewer Communication Script:**
> *"To ensure we build the right MVP, let's lock down requirements. At its core, Splitwise is an expense sharing ledger. Users add expenses, specify how they are split—like Equal, Exact amounts, or Percentages—and the system tracks who owes whom. Do we need to support groups, or just a global pool of users for now?"*

**Core Requirements (The MVP)**
- Register Users.
- Add an Expense paid by one user, shared by many.
- Multiple Split Strategies: EQUAL, EXACT, PERCENTAGE.
- Global Balance Sheet tracking bidirectionally (A owes B).

**Out of Scope (Declare these)**
- *"I'll assume authentication, real payment gateways, and database schema are out of scope for the in-memory LLD."*

---

## Step 2: Clarifying Questions & Boundaries

**🧠 The Master's Approach:** This is where you score massive points by bringing up edge cases related to money.

**🗣️ Interviewer Communication Script:**
> *"Since we are dealing with money, I have two critical clarifying questions. First, rounding errors. If 3 people equally split $100, that's $33.33 each, leaving 1 cent. How should we handle the remainder? (Interviewer: 'Give it to the first person'). Understood. Second, do we want to net out balances dynamically? Meaning if A owes B $50, and B owes A $20, the system just reports A owes B $30? (Interviewer: 'Yes'). Perfect, I'll build that netting into the Ledger directly."*

---

## Step 3: Entity Identification (The Nouns)

**🗣️ Interviewer Communication Script:**
> *"Looking at the entities, we need a `User`, an `Expense` record, and a `Split` object to represent a user's share. Because the math for splitting bills can grow infinitely (shares, itemized, etc.), I strongly propose using a `SplitStrategy` interface. Lastly, we need a `Ledger` or `BalanceSheet` to act as our central graph of debts."*

- **ExpenseManager**: [Facade] Orchestrates the workflow.
- **User**: [Entity] Id, Name.
- **Expense**: [Entity] Total amount, payer, list of resolved splits.
- **Split**: [ValueObject] (User, Amount).
- **SplitStrategy**: [Strategy] Algorithm for EQUAL, EXACT, PERCENT.
- **Ledger**: [Service] Maintains the `Hash[Debtor][Creditor] = Amount`.

---

## Step 4: Relationships & Responsibilities (The Verbs)

**🧠 The Master's Approach:** Emphasize separation of concerns. Math calculation should NEVER touch the Ledger.

**🗣️ Interviewer Communication Script:**
> *"A crucial design decision here is separating the calculation from the state mutation. The `SplitStrategy` is purely functional—it takes a total amount and raw splits, validates them, and returns calculated amounts. It knows nothing about the balance sheet. The `ExpenseManager` takes those calculated amounts and pushes them to the `Ledger`. This ensures our math is highly testable and our ledger stays clean."*

---

## Step 5: Class Diagram / Interface Design

**🗣️ Interviewer Communication Script:**
> *"Here is the architecture. Notice the Strategy pattern on the left. If you later ask me to add a 'Split by Ratio' feature, I only have to add one class implementing `SplitStrategy`. The rest of the system remains untouched, strictly following the Open/Closed Principle."*

```text
 +------------------+        +-------------------+
 |  ExpenseManager  | 1----1 |      Ledger       |
 |------------------|        |-------------------|
 | -users           |        | -balances         |
 | -expenses        |        |-------------------|
 | -ledger          |        | +record(from, to) |
 |------------------|        +-------------------+
 | +add_expense()   |
 +--------+---------+
          |
          | uses
          v
 +------------------+
 | <<Strategy>>     |
 |  SplitStrategy   | <|---- EqualSplit
 |------------------| <|---- ExactSplit
 | +calculate(...)  | <|---- PercentSplit
 +------------------+

 +------------------+        +-------------------+
 |     Expense      | 1----* |      Split        |
 +------------------+        +-------------------+
```

---

## Step 6: Core Implementation

**🧠 The Master's Approach:** Code the `Ledger` and `Strategy` first. They are the core logic. Talk through the float math and validation.

**🗣️ Interviewer Communication Script (While coding):**
> *"I'll start with the Ledger. I'm using a nested Hash to represent the debt graph. When recording debt, I immediately apply netting. If debtor == creditor, I abort, because a user paying for their own share shouldn't pollute the ledger."*

# ============================================================
# CODE BEGINS
# ============================================================

```ruby
# frozen_string_literal: true

module Splitwise
  # =================================================================
  # CORE ENTITIES
  # =================================================================
  class User
    attr_reader :id, :name
    def initialize(id:, name:)
      @id = id; @name = name
    end
  end

  # Value object passed into Strategy, and stored in Expense
  class Split
    attr_reader :user
    attr_accessor :amount, :percent

    def initialize(user:, amount: 0.0, percent: 0.0)
      @user = user
      @amount = amount
      @percent = percent
    end
  end

  class Expense
    attr_reader :id, :total, :payer, :splits
    def initialize(id:, total:, payer:, splits:)
      @id = id; @total = total; @payer = payer; @splits = splits
    end
  end

  # =================================================================
  # STRATEGIES (The Math)
  # =================================================================
  class SplitStrategy
    def calculate(total_amount, splits)
      raise NotImplementedError
    end
  end

  class ExactSplitStrategy < SplitStrategy
    def calculate(total_amount, splits)
      sum = splits.sum(&:amount)
      unless sum.round(2) == total_amount.round(2)
        raise ArgumentError, "Exact splits sum (#{sum}) doesn't match total (#{total_amount})"
      end
      splits
    end
  end

  class PercentSplitStrategy < SplitStrategy
    def calculate(total_amount, splits)
      total_percent = splits.sum(&:percent)
      unless total_percent.round(2) == 100.00
        raise ArgumentError, "Percentage splits must sum to 100.0"
      end

      sum = 0.0
      splits.each do |s|
        s.amount = ((total_amount * s.percent) / 100.0).round(2)
        sum += s.amount
      end

      # Penny rounding fix
      remainder = (total_amount - sum).round(2)
      splits.first.amount += remainder if remainder != 0.0

      splits
    end
  end

  class EqualSplitStrategy < SplitStrategy
    def calculate(total_amount, splits)
      amount_per_person = (total_amount / splits.size).round(2)
      
      splits.each { |s| s.amount = amount_per_person }

      # Penny rounding fix
      sum = splits.sum(&:amount)
      remainder = (total_amount - sum).round(2)
      splits.first.amount += remainder if remainder != 0.0

      splits
    end
  end

  class SplitFactory
    def self.get(type)
      case type
      when :exact   then ExactSplitStrategy.new
      when :percent then PercentSplitStrategy.new
      when :equal   then EqualSplitStrategy.new
      else raise ArgumentError, "Unknown type"
      end
    end
  end

  # =================================================================
  # LEDGER (The Graph)
  # =================================================================
  class Ledger
    def initialize
      # balances[debtor][creditor] = amount
      @balances = Hash.new { |h, k| h[k] = Hash.new(0.0) }
    end

    def record_debt(debtor_id, creditor_id, amount)
      return if debtor_id == creditor_id
      return if amount <= 0

      # Netting out: automatically resolves bidirectional debt
      @balances[debtor_id][creditor_id] += amount
      @balances[creditor_id][debtor_id] -= amount
    end

    def print_balances
      @balances.each do |debtor, creditors|
        creditors.each do |creditor, amt|
          puts "#{debtor} owes #{creditor}: $#{format('%.2f', amt)}" if amt > 0.0
        end
      end
    end
  end

  # =================================================================
  # FACADE (The Orchestrator)
  # =================================================================
  class ExpenseManager
    def initialize
      @users = {}
      @expenses = []
      @ledger = Ledger.new
    end

    def add_user(user)
      @users[user.id] = user
    end

    def add_expense(total_amount:, payer_id:, type:, splits:)
      payer = @users[payer_id]
      strategy = SplitFactory.get(type)
      
      # 1. Validation and Math calculation
      calculated_splits = strategy.calculate(total_amount, splits)

      # 2. Record keeping
      @expenses << Expense.new(id: @expenses.size, total: total_amount, payer: payer, splits: calculated_splits)

      # 3. Update global balance sheet
      calculated_splits.each do |split|
        @ledger.record_debt(split.user.id, payer.id, split.amount)
      end
    end

    def show_all
      @ledger.print_balances
    end
  end
end
```

---

## Step 7: Post-Solve Reflection (The "Senior" Close-Out)

**🧠 The Master's Approach:** This is where you demonstrate you know how to take this in-memory toy and put it on AWS.

**🗣️ Interviewer Communication Script:**
> *"Alright, the system works and safely handles float rounding. If we were moving this to a real backend, my first concern is database transactions. If two users add an expense simultaneously, updating the Ledger requires an ACID transaction (like `SELECT FOR UPDATE` in Postgres) to prevent race conditions on the balances. Second, floats in Ruby are risky for real money long-term. In production, I would store all amounts as Integer Cents (e.g., $10.00 is `1000`) or use `BigDecimal`."*

### What Else Could Break / Follow-Up Defenses

**Q: "How would you implement 'Simplify Debts'?"**
> **A:** *"Currently, our graph can look like A->B, B->C, C->D. Simplify Debts requires calculating the total net balance of every user (+ or -). We create a list of Debtors and Creditors. Then, using a greedy algorithm, we match the biggest Debtor with the biggest Creditor, create a new transaction, and repeat until balances hit zero. This transforms O(N^2) edges into roughly O(N) edges."*

**Q: "What if a user disputes an expense and we have to delete it?"**
> **A:** *"Because our `Ledger` nets balances destructively, deleting an expense isn't trivial. We would need to implement an 'Undo' by creating an inverse transaction (A paid B $50, Undo = B paid A $50) to reverse the Ledger effect, and then mark the original Expense as voided. This preserves auditability."*

### ❌ The "Junior" Trap (What most people get wrong)
Juniors write one giant `add_expense` method with a massive `switch(type)` statement. Inside the switch, they do the math AND mutate the balance arrays at the same time. If a validation fails halfway through the loop, the ledger is left in a corrupted state. 

**The Senior Move:** Calculate everything purely first. Validate. *Then* apply state changes in one batch. Separation of concerns.
