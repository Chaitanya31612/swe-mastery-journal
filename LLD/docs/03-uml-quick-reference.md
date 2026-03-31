# 📐 UML Quick Reference — Class Diagrams for LLD Rounds

> You don't need to master UML. You need to **sketch class diagrams fast** on a
> whiteboard or in comments. This is the bare minimum that impresses interviewers.

---

## Class Notation

```
┌──────────────────────────┐
│      <<interface>>       │   ← Stereotype (optional)
│     ParkingStrategy      │   ← Class/Interface Name
├──────────────────────────┤
│ (no fields for interface)│   ← Attributes Section
├──────────────────────────┤
│ + findSpot(v: Vehicle)   │   ← Methods Section
│   : ParkingSpot          │
└──────────────────────────┘

Visibility:
  + public
  - private
  # protected
  ~ package-private
```

---

## Relationship Types (Only 4 Matter)

### 1. Association → "uses-a" (solid line with arrow)
```
┌──────────┐          ┌──────────┐
│  Driver   │ -------> │   Car    │
└──────────┘          └──────────┘
Driver HAS a reference to Car (but Car can exist without Driver)
```

### 2. Composition → "part-of" (solid diamond)
```
┌──────────┐ ◆───────> ┌──────────┐
│  House   │           │   Room   │
└──────────┘           └──────────┘
Room CANNOT exist without House (dies with it)
```

### 3. Aggregation → "has-a" (hollow diamond)
```
┌──────────┐ ◇───────> ┌──────────┐
│Department│           │ Employee │
└──────────┘           └──────────┘
Employee CAN exist without Department
```

### 4. Inheritance → "is-a" (hollow triangle arrow)
```
        ┌──────────┐
        │  Vehicle  │
        └─────▲────┘
              │
     ┌────────┼────────┐
     │        │        │
┌────┴───┐ ┌──┴───┐ ┌──┴──┐
│  Car   │ │ Truck│ │ Bike│
└────────┘ └──────┘ └─────┘
```

### 5. Interface Implementation (dashed arrow with hollow triangle)
```
        ┌─────────────────┐
        │ <<interface>>   │
        │ ParkingStrategy │
        └───────▲─────────┘
                ┊ (dashed)
       ┌────────┼──────────┐
       ┊                   ┊
┌──────┴────────┐  ┌───────┴───────┐
│NearestFirst   │  │SpreadEvenly   │
│Strategy       │  │Strategy       │
└───────────────┘  └───────────────┘
```

---

## Multiplicity

```
1      → Exactly one
0..1   → Zero or one
*      → Zero or more (same as 0..*)
1..*   → One or more

Example:
┌──────────┐ 1     * ┌──────────┐
│  Floor   │────────│   Spot   │
└──────────┘        └──────────┘
"One Floor has many Spots"
```

---

## Example: Parking Lot Class Diagram

```
                        ┌──────────────────┐
                        │   ParkingLot     │
                        ├──────────────────┤
                        │ - name: String   │
                        │ - floors: List   │
                        ├──────────────────┤
                        │ + park(v): Ticket│
                        │ + unpark(t): Veh │
                        └────────┬─────────┘
                                 │ 1
                                 │
                                 │ *
                        ┌────────┴─────────┐
                        │      Floor       │
                        ├──────────────────┤
                        │ - floorNumber    │
                        │ - spots: List    │
                        ├──────────────────┤
                        │ + getAvailable() │
                        └────────┬─────────┘
                                 │ 1
                                 │
                                 │ *
                        ┌────────┴─────────┐
                        │   ParkingSpot    │
                        ├──────────────────┤
        ┌─ ─ ─ ─ ─ ─ ─>│ - type: SpotType │
        ┊               │ - vehicle: Veh   │
        ┊               │ - isAvailable    │
  ┌─────┴──────────┐    ├──────────────────┤
  │ <<interface>>  │    │ + canFit(v): bool│
  │ParkingStrategy │    │ + occupy(v): void│
  ├────────────────┤    │ + vacate(): Veh  │
  │+ findSpot()    │    └──────────────────┘
  └────────────────┘
        ▲ ┊
        ┊ ┊
  ┌─────┴───────┐
  │NearestFirst │
  │Strategy     │
  └─────────────┘

  ┌──────────────┐
  │   Vehicle    │ (abstract)
  ├──────────────┤
  │ - plate      │
  │ - type       │
  └──────▲───────┘
         │
    ┌────┼────┐
    │    │    │
  ┌─┴─┐┌┴──┐┌┴──┐
  │Car││Trk││Bke│
  └───┘└───┘└───┘
```

---

## 🏃 Speed Tips for Interviews

1. **Don't draw perfect UML** — a sketch with boxes, lines, and labels is enough
2. **Focus on:**
   - Key entities (boxes)
   - Has-a relationships (lines with `1` and `*`)
   - Is-a relationships (inheritance arrows)
   - Interface implementations (dashed arrows)
3. **Label the relationships** when it's not obvious
4. **Use comments in code** if no whiteboard:
   ```java
   // ParkingLot 1──* Floor 1──* ParkingSpot
   // Vehicle <|── Car, Truck, Bike
   // ParkingLot --> ParkingStrategy (interface)
   ```

---

## 🚫 Don't Bother With
- Sequence diagrams (unless specifically asked)
- Activity diagrams
- Use case diagrams
- Deployment diagrams
- Component diagrams

Class diagrams are **the only UML** that matters in machine coding rounds.
