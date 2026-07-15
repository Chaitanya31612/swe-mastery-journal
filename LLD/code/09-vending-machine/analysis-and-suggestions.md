# Vending Machine LLD: Analysis & Roadmap

This guide provides a structured review of your Vending Machine LLD approach. Since you are in the learning phase, the focus here is on **architectural thinking**, **steering your design process**, and showing you how to **lock down** a design *before* writing code.

---

## 1. High-Level Approach Analysis

### **Strengths of Your Design**
- **Correct Core Pattern**: The **State Pattern** is the absolute industry-standard for a Vending Machine LLD because the machine’s behavior depends directly on its internal status (Idle vs. Payment Awaited vs. Dispensing).
- **Practical Simplification**: Mapping items by a flat ID (`index + 1` or slot code) is a great simplification. In real life, most vending machines use alphanumeric codes (e.g., `A1`, `B2`, `01`, `02`) rather than coordinates. A flat key-value map is clean, highly readable, and perfectly acceptable in an LLD interview.

### **Areas for Improvement**
- **State Object Instantiation**: In your code, you write `vendingMachine.setState(State.ITEM_SELECTED)`. In the State Pattern, states are objects. A clean way is to pre-instantiate the state objects in the `VendingMachine` context class and switch between them. This prevents garbage collection overhead from creating new state objects constantly.
- **Context Encapsulation**: Concrete states (like `IdleState`) need to access data inside the `VendingMachine` context (like `inventory` and `totalAmount`). Instead of making the context's internal fields public or package-private, expose public getter and helper methods (e.g., `getInventory()`, `addAmount()`).

---

## 2. The 10-Minute LLD "Lockdown" Strategy

To avoid changing variables, parameters, or class structures mid-interview, use this **4-Step Lockdown Checklist** in the first 10 minutes:

```
Step 1: Write down the Nouns (Models)
  └─ What are the entities? (Item, Slot, VendingMachine)
  
Step 2: Draw the State Transitions (Lifecycle)
  └─ IDLE -> ITEM_SELECTED -> HAS_MONEY -> DISPENSING -> IDLE
  
Step 3: Define the State Contract (Interface Methods)
  └─ selectItem(), insertMoney(), confirmOrder(), cancel()
  
Step 4: Confirm API Signatures with Interviewer
  └─ Once signatures are locked, coding is just filling in the blanks.
```

### **Why Lockdown Works**
By agreeing with the interviewer on the method signatures of the `State` interface first, you build a contract. Once that contract is written down, you don't need to think about *how* classes communicate while writing the body logic.

---

## 3. "Good Enough" vs. "Ideal" Reference Designs

Below are two clean reference implementations based on your design.

### **Option A: The Flat Slot Approach (Your simplifed choice - Recommended)**
This code maps inventory directly to numeric slot IDs, matching your preferred simplified model.

```java
import java.util.HashMap;
import java.util.Map;

// ==========================================
// 1. STATE INTERFACE CONTRACT (The Verbs)
// ==========================================
interface State {
  void selectItem(int slotId, int quantity);
  void insertMoney(int amount);
  int dispenseAndReturnChange();
  void cancel();
  String getName();
}

// ==========================================
// 2. DOMAIN MODELS (The Nouns)
// ==========================================
class Item {
  private final String name;
  private final int price;

  public Item(String name, int price) {
    this.name = name;
    this.price = price;
  }

  public String getName() { return name; }
  public int getPrice() { return price; }
}

class Slot {
  private Item item;
  private int quantity;

  public Slot(Item item, int quantity) {
    this.item = item;
    this.quantity = quantity;
  }

  public Item getItem() { return item; }
  public int getQuantity() { return quantity; }
  public void setQuantity(int quantity) { this.quantity = quantity; }
}

// ==========================================
// 3. CONCRETE STATE IMPLEMENTATIONS
// ==========================================
class IdleState implements State {
  private final VendingMachine vm;

  public IdleState(VendingMachine vm) { this.vm = vm; }

  @Override
  public void selectItem(int slotId, int quantity) {
    Slot slot = vm.getInventory().get(slotId);
    if (slot == null || slot.getItem() == null) {
      System.out.println("Invalid slot.");
      return;
    }
    if (slot.getQuantity() < quantity) {
      System.out.println("Out of stock.");
      return;
    }

    vm.setSelectedItem(slotId, quantity);
    vm.setTotalAmount(slot.getItem().getPrice() * quantity);
    vm.setCurrentState(vm.getItemSelectedState());
    System.out.println("Selected " + slot.getItem().getName() + ". Total: " + vm.getTotalAmount() + " Rs.");
  }

  @Override
  public void insertMoney(int amount) { System.out.println("Select item first."); }

  @Override
  public int dispenseAndReturnChange() { return 0; }

  @Override
  public void cancel() { System.out.println("Nothing to cancel."); }

  @Override
  public String getName() { return "IDLE"; }
}

class ItemSelectedState implements State {
  private final VendingMachine vm;

  public ItemSelectedState(VendingMachine vm) { this.vm = vm; }

  @Override
  public void selectItem(int slotId, int quantity) { System.out.println("Complete current order or cancel first."); }

  @Override
  public void insertMoney(int amount) {
    if (amount < vm.getTotalAmount()) {
      System.out.println("Insufficient payment. Required: " + vm.getTotalAmount() + " Rs.");
      return;
    }
    vm.setInsertedMoney(amount);
    vm.setCurrentState(vm.getHasMoneyState());
    System.out.println("Accepted: " + amount + " Rs.");
  }

  @Override
  public int dispenseAndReturnChange() { return 0; }

  @Override
  public void cancel() {
    System.out.println("Order cancelled.");
    vm.resetOrder();
    vm.setCurrentState(vm.getIdleState());
  }

  @Override
  public String getName() { return "ITEM_SELECTED"; }
}

class HasMoneyState implements State {
  private final VendingMachine vm;

  public HasMoneyState(VendingMachine vm) { this.vm = vm; }

  @Override
  public void selectItem(int slotId, int quantity) {}

  @Override
  public void insertMoney(int amount) {}

  @Override
  public int dispenseAndReturnChange() {
    vm.setCurrentState(vm.getDispensingState());
    return vm.getCurrentState().dispenseAndReturnChange();
  }

  @Override
  public void cancel() {
    System.out.println("Refunding money: " + vm.getInsertedMoney() + " Rs.");
    vm.resetOrder();
    vm.setCurrentState(vm.getIdleState());
  }

  @Override
  public String getName() { return "HAS_MONEY"; }
}

class DispensingState implements State {
  private final VendingMachine vm;

  public DispensingState(VendingMachine vm) { this.vm = vm; }

  @Override
  public void selectItem(int slotId, int quantity) {}

  @Override
  public void insertMoney(int amount) {}

  @Override
  public int dispenseAndReturnChange() {
    int slotId = vm.getSelectedSlotId();
    int qty = vm.getSelectedQuantity();
    Slot slot = vm.getInventory().get(slotId);

    // Deduct stock
    slot.setQuantity(slot.getQuantity() - qty);
    System.out.println("Dispensing: " + slot.getItem().getName() + " x" + qty);

    int change = vm.getInsertedMoney() - vm.getTotalAmount();
    vm.resetOrder();
    vm.setCurrentState(vm.getIdleState());
    return change;
  }

  @Override
  public void cancel() {}

  @Override
  public String getName() { return "DISPENSING"; }
}

// ==========================================
// 4. VENDING MACHINE CONTEXT (Coordinates Everything)
// ==========================================
class VendingMachine {
  private final Map<Integer, Slot> inventory = new HashMap<>();
  
  // State variables
  private final State idleState = new IdleState(this);
  private final State itemSelectedState = new ItemSelectedState(this);
  private final State hasMoneyState = new HasMoneyState(this);
  private final State dispensingState = new DispensingState(this);
  private State currentState = idleState;

  // Transaction variables
  private int selectedSlotId;
  private int selectedQuantity;
  private int totalAmount;
  private int insertedMoney;

  public void addSlot(int slotId, Item item, int quantity) {
    inventory.put(slotId, new Slot(item, quantity));
  }

  // Public interfaces delegating to active state
  public void selectItem(int slotId, int quantity) { currentState.selectItem(slotId, quantity); }
  public void insertMoney(int amount) { currentState.insertMoney(amount); }
  public int dispenseAndReturnChange() { return currentState.dispenseAndReturnChange(); }
  public void cancel() { currentState.cancel(); }

  // Getters & Setters for States to manipulate Context safely
  public Map<Integer, Slot> getInventory() { return inventory; }
  
  public void setSelectedItem(int slotId, int quantity) {
    this.selectedSlotId = slotId;
    this.selectedQuantity = quantity;
  }
  
  public int getSelectedSlotId() { return selectedSlotId; }
  public int getSelectedQuantity() { return selectedQuantity; }
  
  public int getTotalAmount() { return totalAmount; }
  public void setTotalAmount(int amount) { this.totalAmount = amount; }
  
  public int getInsertedMoney() { return insertedMoney; }
  public void setInsertedMoney(int amount) { this.insertedMoney = amount; }

  public void setCurrentState(State state) { this.currentState = state; }
  public String getStateName() { return currentState.getName(); }

  public State getIdleState() { return idleState; }
  public State getItemSelectedState() { return itemSelectedState; }
  public State getHasMoneyState() { return hasMoneyState; }
  public State getDispensingState() { return dispensingState; }

  public void resetOrder() {
    this.selectedSlotId = 0;
    this.selectedQuantity = 0;
    this.totalAmount = 0;
    this.insertedMoney = 0;
  }
}
```

---

### **Option B: The 2D Grid Approach (Optional)**
If an interviewer explicitly asks for a physical 2D grid structure, the change is simple:
- Instead of using a `Map<Integer, Slot>`, define an `Inventory` class containing a 2D array of slots: `Slot[][] grid`.
- Modify `selectItem(int slotId, int quantity)` to `selectItem(int row, int col, int quantity)`.
- Rest of the state machine remains exactly the same!

This demonstrates the power of the State Pattern: **your state machine logic is independent of how you organize your inventory data structure.**
