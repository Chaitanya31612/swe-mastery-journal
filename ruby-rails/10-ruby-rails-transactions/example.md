# A small example

```ruby
class ReserveStock
  def call(stock_id)
    Stock.transaction do
      stock = Stock.lock.find(stock_id)
      raise "out of stock" unless stock.quantity > 0
      stock.update!(quantity: stock.quantity - 1)
      Reservation.create!(stock_id: stock.id)
      # Optional outbox row belongs in this same transaction.
    end
  end
end
```
The lock serializes competing writes to that row while the transaction runs. It does not serialize all inventory worldwide.

Keep slow network calls outside the row-lock window.