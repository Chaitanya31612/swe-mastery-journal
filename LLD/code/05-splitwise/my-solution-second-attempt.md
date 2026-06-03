# Problem statement

Design splitwise application - a system to allow users to manage and split expenses with other users.

# Requirements Clarification

## Must haves

- create users
- two types of expenses - group and non-group
  - non-group are simple/one-off expenses where a user pays for a list of users
  - group can have many participants (users) and can have multiple payments from different users and different subset of participants
- ability to split expenses - equal, percentage, exact amount
- balance sheet for each expense - visible to each user by their id

## Nice to have
- simplify debts in a group

## out of scope
- Payment of balances in the app
- Downloading statements
- Sharing receipts
- splitting differently in an expense for different users - like having equal split and percentage or amount split for some users in an expense

# Entities

- User (class)
  is - a person in the system
  knows - id, name
  does - nothing - only data entity

- Expense (class)
  is - an expense paid by one user for a list of users and optionally can also belong to a group
  knows - id, paidBy, amount, participants, splitType, groupId (optional)
  does - data entity

- BalanceEntry (class)
  is - a record of balance between two users
  knows - id, userFrom, userTo, amount
  does - data entity

- Ledger (class)
  is - singleton class for managing balance entries
  knows - balanceEntries: Map<User, List<BalanceEntry>>
  does - addBalanceEntry(balanceEntry: BalanceEntry): void, getBalanceSheet(user: User): List<BalanceEntry>

- SplitStrategy (interface)
  is - interface for split strategy pattern
  knows - nothing
  does - calculate(total: Decimal, splits: List<Split>): Map<User, Decimal> - returns the amount each user owes

- EqualSplitStrategy (class) | ExactAmountSplitStrategy (class) | PercentageSplitStrategy (class)y

- Split (class)
  is - individual share/split for a user
  knows - user, amount (this can be passed in as well), percentage (optional)
  does - nothing

- Group (class)
  is - collection of users managing group expenses
  knows - id, name, users (this would need a join table - many to many association - so user has many group_id), expenses (has many association to expenses)
  does - addMember(user: User): void, removeMember(user: User): void, addExpense(expense: Expense): void, simplifyDebts(): void

Facade / Orchestrator
- ExpenseManager (class)
  is - facade or entry point
  knows - users, expenses, balanceEntries
  does - addUser(name: String): User, addExpense(paidBy: User, participants: List<User>, total: Decimal, splits: List<Split>, splitType: SplitType, groupId: Integer): Expense, getUserBalanceSheet(user: User): List<BalanceEntry>, logTransactions, addGroup


# Implementation

```ruby


# Facade / Orchestrator
class ExpenseManager
  attr_reader :users, :expenses, :ledger

  def initialize
    @users = []
    @expenses = []
    @ledger = Ledger.new
  end

  def addUser(name: String): User
    @users << User.new(name: name)
  end

  def getUserBalanceSheet(user: User): List<BalanceEntry>
    @ledger.getBalanceSheet(user)
  end

  def logTransactions(): void
    all_balance_entries = ledger.getAllBalanceEntries() # Map<User, List<BalanceEntry>>

    all_balance_entries.each do |user, balances| # iterate on map
      puts "For user: #{user.name}"
      balances.each do |balance_entry|
        action = balance_entry.amount > 0 ? "owes" : "is owed by"
        puts "#{user.name} #{action} #{balance_entry.userTo.name} #{balance_entry.amount.abs()}"
      end
    end
  end

  def addExpense(paidBy: User, participants: List<User>, total: Decimal, splits: List<Split>, splitType: SplitType, groupId: Integer)
    splitStrategy = SplitStrategyFactory.get(splitType)

    splitDetails = splitStrategy.calculate(total, splits) # Map<User, Decimal>

    @expenses << Expense::Builder.new
      .paidBy(paidBy)
      .participants(participants)
      .amount(total)
      .splitType(splitType)
      .groupId(groupId)
      .build()

    # update balances
    splitDetails.each do |user, amount|
      next if user == paidBy
      @ledger.recordTransaction(userFrom: user, userTo: paidBy, amount: amount)
    end
  end
end








```
