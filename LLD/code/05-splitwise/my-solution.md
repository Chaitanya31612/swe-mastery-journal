

Steps I'll be following in an LLD problem

1. Problem statement
2. Requirements Clarification
   a. Must Haves
   b. Nice to Have or Out of scope
   c. Clarify these two before and nail down before moving forward with implementation
3. Entities Identification from the requirements
   a. Nouns become classes
   b. Verbs become methods
4. Relationship and Class Diagrams
5. Design Pattern Identification
6. Implementation
7. Dry Run and test cases

# Problem Statement

To build Splitwise - a system for splitting expenses among users.

# Requirements Clarification

## Must haves

- users should have an account
- users can create expenses with other users individually or in groups
- Expenses can be split either equal, or percentage wise
- User see their balance sheet i.e. amount they owe or amount they are owed

## Nice to have / Out of scope
- Settle payments on the app
- statements and reports
- sharing receipts
- group management

# Entities Identification from the requirements

- User (class)
- Expense (class) - will have paidBy and participants, splitType, amount, group_id, splitDetails - for storing the split details
- BalanceSheet (class) - user's outgoing and incoming balance
- SplitType (enum) - equal, percentage
- Group (class) - will have multiple users and expense will have group_id if expense in group

```ruby
class User
  - id: Integer
  - name: String
  - balances: List<BalanceEntry> - positive if owes money to other user, negative if other user owes money to this user
  (this can be has many association by foreign key of user_id on balance_entry table)
  (contain only balance entries where userFrom is this user as we are creating duplicate entries for postive and negative credit)

  + getUserBalanceSheet(): List<BalanceEntry> - returns all incoming and outgoing balances for this user
  + getOutstandings(): Map<User, Decimal>  - returns all outgoing balances for this user, where amount is positive
  + getIncomings(): Map<User, Decimal> - returns all incoming balances for this user, where amount is negative
  + updateBalances(balances: List<BalanceEntry>): void - updates the balance for this user
  + addBalance(balance: BalanceEntry): void - adds the balance for this user
  + removeClearedBalances(): void - removes cleared balances
end

# each expense will have balance entry for each user
# userA paid 100 for split among A, B, C
# B owes A -> userFrom=B, userTo=A, amount=50
# C owes A -> userFrom=C, userTo=A, amount=50
# A owed money from B -> userFrom=A, userTo=B, amount=-50
# A owed money from C -> userFrom=A, userTo=C, amount=-50
class BalanceEntry
   - id: Integer
   - userFrom: User
   - userTo: User
   - amount: Decimal - positive if userFrom owes money to userTo, negative if userTo owes money to userFrom
   - date: Date - auto timestamp

   + updateBalance(amount: Decimal): void - updates the balance for this user
   + createBalanceEntry(userFrom: User, userTo: User, amount: Decimal): void - creates two entries, one positive and one negative for userFrom and userTo
end

# Strategy pattern - to use different split algorithm for splitting
# Factory pattern - for determining split strategy based on split type
# Builder pattern - for creating expense
class Expense
   - id: Integer
   - paidBy: User
   - participants: List<User> - exclude paidBy
   - groupId: Integer - null if individual expense, group id if group expense
   - amount: Decimal
   - splitType: SplitType - EQUAL | PERCENTAGE
   - splitStrategy: SplitStrategy - will use strategy pattern to split the amount
   - Builder (inner static nested class) - for building the expense

   + getSplitDetails(): Map<User, Decimal> - returns the amount each user owes - will call splitStrategy.getSplit()
   + getStrategy(): SplitStrategy - factory pattern based on split type
   + updateUserBalances(splitDetails: Map<User, Decimal>): void - updates the balance for all users
   # + createExpense(paidBy: User, participants: List<User>, amount: Decimal, splitType: SplitType, groupId: Integer): Expense - uses expense builder pattern - DONE BY BUILDER PATTERN
end

class Group
   - id: Integer
   - name: String
   - users: List<User>
   - expenses: List<Expense>

   + addMember(user: User): void
   + removeMember(user: User): void
   + *simplifyDebts(): void - will simplify the debts in the group - also update user balance sheets in the group
end

```

# Relationship diagrams

User 1 -- many BalanceEntry
Expense 1 -- 1 User - paidBy
Expense 1 -- many User - participants
Expense 1 -- 1 Group

# Implementation

```ruby

class BalanceEntry
   def createBalanceEntry(userFrom, userTo, amount): void
      balanceEntryOwed = new BalanceEntry(userFrom, userTo, amount)
      balanceEntryOwedTo = new BalanceEntry(userTo, userFrom, -amount)

      userFrom.updateBalances([balanceEntryOwed])
      userTo.updateBalances([balanceEntryOwedTo])
   end

   def updateBalance(amount: Decimal): void
      self.amount += amount
   end
end

class User
   def getOutstandings(): Map<User, Decimal>
      balances.filter { |balance| balance.amount > 0 }
   end

   def getIncomings(): Map<User, Decimal>
      balances.filter { |balance| balance.amount < 0 }
   end

   def addBalance(balance: BalanceEntry): void
      existingBalance = balances.find { |bal| bal.userTo == balance.userTo
      if existingBalance
         existingBalance.updateBalance(balance.amount)
      else
         balances.add(balance)
      end
      removeClearedBalances()
   end

   def updateBalances(balances: List<BalanceEntry>): void
      balances.each { |balance| addBalance(balance) }
   end

   def removeClearedBalances()
      balances.reject! { |balance| balance.amount == 0 }
   end
end

class SplitType
   EQUAL = "equal".freeze
   PERCENTAGE = "percentage".freeze
end

class Expense
   attr_reader :paidBy, :participants, :percentages, :amount, :splitType, :groupId, :splitStrategy

   def initialize(builder)
      @paidBy = builder.paidBy
      @participants = builder.participants
      @percentages = builder.percentages # only when splitType is PERCENTAGE
      @amount = builder.amount
      @splitType = builder.splitType
      @groupId = builder.groupId
      @factory = SplitStrategyFactory.new()
      @splitStrategy = @factory.getSplitStrategy(builder.splitType)
   end

   def updateUserBalances()
      splitDetails = splitStrategy.getSplit(self)

      splitDetails.each do |user, amount|
         BalanceEntry.new.createBalanceEntry(paidBy, user, amount)
      end
   end

   class Builder
      attr_accessor :paidBy, :participants, :percentages, :amount, :splitType, :groupId, :splitStrategy

      def initialize()
         @paidBy = nil
         @participants = []
         @percentages = {} # only when splitType is PERCENTAGE
         @amount = 0
         @splitType = nil
         @groupId = nil
         @splitStrategy = nil
      end

      def paidBy(paidBy: User): Builder
         @paidBy = paidBy
         return self
      end

      def addParticipant(participant: User): Builder
         @participants.add(participant)
         return self
      end

      def addPercentage(user: User, percentage: Decimal): Builder
         @percentages[user] = percentage
         return self
      end

      def expenseAmount(amount: Double): Builder
         @amount = amount
         return self
      end

      def splitType(splitType: SplitType): Builder
         @splitType = splitType
         return self
      end

      def groupId(groupId: Integer): Builder
         @groupId = groupId
         return self
      end

      def build(): Expense
         return Expense.new(self)
      end
   end
end

class SplitStrategyFactory
   def getSplitStrategy(splitType: SplitType): SplitStrategy
      case splitType
         when SplitType.EQUAL
            return EqualSplitStrategy()
         when SplitType.PERCENTAGE
            return PercentageSplitStrategy()
         else
            throw Exception("Invalid split type")
      end
   end
end

# ABC
class SplitStrategy
   def getSplit(expense: Expense): Map<User, Decimal>
      throw Exception("Not implemented")
   end
end

class EqualSplitStrategy < SplitStrategy
   def getSplit(expense: Expense): Map<User, Decimal>
      totalParticipants = expense.participants.size + 1 # paidBy is also participant
      individualAmount = expense.amount / totalParticipants

      splitDetails = {}

      expense.participants.each do |participant|
         splitDetails[participant] = individualAmount
      end

      return splitDetails
   end
end

class PercentageSplitStrategy < SplitStrategy
   def getSplit(expense: Expense): Map<User, Decimal>
      splitDetails = {}

      expense.participants.each do |participant|
         splitDetails[participant] = expense.amount * (expense.percentages[participant] / 100)
      end

      return splitDetails
   end
end

class Group
   attr_reader :users, :expenses

   def initialize()
      @users = []
      @expenses = []
   end

   def addMember(user: User): void
      @users.add(user)
   end

   def removeMember(user: User): void
      @users.reject! { |u| u == user }
   end

   def simplifyDebts(): void
      =begin
         Each user has their balancesheets
         where they know userTo and amount - if amount > 0 - user need to give, else need to receive
         so in a group
         each user will have a net balance - sum of all balance amounts

         lets say
         group has 3 members, A, B and C
         A paid 150 for equal split among A, B and C
         A owes money from B -> userFrom=A, userTo=B, amount=-50
         A owed money from C -> userFrom=A, userTo=C, amount=-50
         A net balance = -100

         userFrom=B, userTo=A, amount=50
         B net balance = 50
         userFrom=C, userTo=A, amount=50
         C net balance = 50

         B pays 100, split with A
         userFrom=B, userTo=A, amount=-50
         userFrom=A, userTo=B, amount=50
         A net balance = -50
         B net balance = 0
         C net balance = 50

         so in this case C can give 50 to A, and B dont give anything

         so we calculate net balances

         A -> 100 -> C
         C -> 150 -> B
         B -> 50 -> A
         B -> 100 -> C

         A net = -100 + 50 = -50
         B net = 150 - 50 - 100 = 0
         C net = 100 - 150 + 100 = 50

         so we can simply the debts

         Users who need to give money -> negative net balance
         Users who need to receive money -> positive net balance

         A: -50, B: 0, C: 50

         A can give 50 directly to C - this is the simplest way to settle the debts

         We can use priority queue to settle the debts
         The approach is like this, step by step

         1. create a map of all users and their net balances
         2. create a priority queue of users who need to give money (negative net balance)
         3. create a priority queue of users who need to receive money (positive net balance)
         4. while there are users in both priority queues
            a. take the user with the highest negative balance
            b. take the user with the highest positive balance
            c. settle the amount
            d. update the balances
            e. if the balance becomes 0, remove the user from the priority queue

         Example
         A: -50, B: 0, C: 50
         1. take A from negative priority queue
         2. take C from positive priority queue
         3. A gives 50 to C
         4. A balance = 0, C balance = 0
         5. A and C are removed from priority queues
         6. Now priority queues are empty, stop

         Note: priority queue should be implemented as min heap for negative numbers and max heap for positive numbers
      =end

      def simplifyDebts(): void
         netBalances = {}
         users.each do |user|
            netBalances[user] = user.getIncomings() - user.getOutstandings()
         end

         # split them in two priority queues
         usersWhoNeedToGive = netBalances.filter { |user, balance| balance < 0 }
         usersWhoNeedToReceive = netBalances.filter { |user, balance| balance > 0 }

         usersWhoNeedToGive.sort_by! { |user, balance| balance } # min heap
         usersWhoNeedToReceive.sort_by! { |user, balance| -balance } # max heap

         # two pointers for iterating through priority queues
         i = 0
         j = 0
         while i < usersWhoNeedToGive.size && j < usersWhoNeedToReceive.size
            giver, giverBalance = usersWhoNeedToGive[i]
            receiver, receiverBalance = usersWhoNeedToReceive[j]

            giverBalance = -giverBalance

            if giverBalance > receiverBalance
               j += 1
               userWhoNeedToGive[i][1] -= receiverBalance
            elsif giverBalance < receiverBalance
               i += 1
               userWhoNeedToReceive[j][1] -= giverBalance
            else # giverBalance == receiverBalance
               i += 1
               j += 1
            end



         end


      end
   end
end
```
