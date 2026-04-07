"""
This script analyzes customer transactions.

Behavior:
- Skips invalid transactions (<= 0)
- Stops execution completely if a suspicious transaction (999.99) is found
- Identifies premium transactions (> 1000)
- Calculates total and average ONLY until the system stops

Note:
Stops execution immediately when a suspicious transaction is detected.
"""

transactions = [
    150.75, -20.0, 999.99, 1200.50, 85.30,
    0.0, 450.00, 1300.99, -5.5,
    720.40, 60.0, 2000.00
]

premium_transactions = []

total = 0
count = 0

for index, amount in enumerate(transactions, start=1):

    if amount <= 0:
        print(f"Transaction {index}: Invalid transaction skipped ({amount} TL)")
        continue

    if amount == 999.99:
        print(f"Transaction {index}: System stopped (suspicious: {amount} TL)")
        break

    if amount > 1000:
        print(f"Transaction {index}: {amount} TL - Premium")
        premium_transactions.append(amount)
    else:
        print(f"Transaction {index}: {amount} TL")

    total += amount
    count += 1

if count > 0:
    average = total / count
    print("\nSummary:")
    print(f"Total: {total} TL")
    print(f"Average: {average:.2f} TL")
else:
    print("\nNo valid transactions.")

print(f"\nPremium Transactions: {premium_transactions}")