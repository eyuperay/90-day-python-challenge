#!/usr/bin/env python3
"""
Day 55 - Enum Usage
Demonstrates Python Enum for constants management
"""

from enum_demo import *
import json


def print_section(title: str):
    """Print section header"""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    print("=" * 60)
    print("DAY 55 - ENUM USAGE")
    print("=" * 60 + "\n")
    
    # ==================== 1. BASIC ENUM ====================
    print_section("1. BASIC ENUM")
    
    print("Colors:")
    for color in Color:
        print(f"  {color.name}: {color.value}")
    
    print(f"\nColor.RED: {Color.RED}")
    print(f"Color.RED.value: {Color.RED.value}")
    print(f"Color.RED.name: {Color.RED.name}")
    print(f"Color.RED.describe(): {Color.RED.describe()}")
    
    # Access by value
    print(f"\nColor(1): {Color(1)}")
    print(f"Color['RED']: {Color['RED']}")
    
    # ==================== 2. AUTO-VALUE ENUM ====================
    print_section("2. AUTO-VALUE ENUM")
    
    print("Priority (auto values):")
    for priority in Priority:
        print(f"  {priority.name}: {priority.value}")
    
    # ==================== 3. ENUM WITH METHODS ====================
    print_section("3. ENUM WITH METHODS")
    
    print("Status workflow:")
    statuses = [Status.PENDING, Status.PROCESSING, Status.SHIPPED, Status.DELIVERED]
    for status in statuses:
        next_s = status.next_status()
        print(f"  {status.value} -> {next_s.value if next_s else 'END'}")
    
    print(f"\nStatus.PENDING.is_active(): {Status.PENDING.is_active()}")
    print(f"Status.DELIVERED.is_active(): {Status.DELIVERED.is_active()}")
    
    # ==================== 4. INTEGER ENUM ====================
    print_section("4. INTEGER ENUM")
    
    print("HTTP Status Codes:")
    for status in HttpStatus:
        print(f"  {status.name}: {status.value}")
    
    print(f"\nHttpStatus.OK: {HttpStatus.OK}")
    print(f"HttpStatus.OK == 200: {HttpStatus.OK == 200}")
    print(f"HttpStatus.OK.value == 200: {HttpStatus.OK.value == 200}")
    
    # ==================== 5. DAYS WITH METHODS ====================
    print_section("5. DAYS OF WEEK WITH METHODS")
    
    today = Day.MONDAY
    print(f"Today: {today.name}")
    print(f"Is weekend? {today.is_weekend()}")
    print(f"Is weekday? {today.is_weekday()}")
    print(f"Next day: {today.next_day().name}")
    print(f"Previous day: {today.previous_day().name}")
    
    print("\nAll days:")
    for day in Day:
        print(f"  {day.name}: {'Weekend' if day.is_weekend() else 'Weekday'}")
    
    # ==================== 6. CURRENCY WITH PROPERTIES ====================
    print_section("6. CURRENCY WITH CUSTOM PROPERTIES")
    
    usd = Currency.USD
    turkish_lira = Currency.TRY
    
    print(f"USD: {usd.code} ({usd.symbol}) - Rate: {usd.rate_to_usd}")
    print(f"TRY: {turkish_lira.code} ({turkish_lira.symbol}) - Rate: {turkish_lira.rate_to_usd}")
    
    amount_usd = 100
    print(f"\n{amount_usd} USD = {turkish_lira.convert_from_usd(amount_usd):.2f} TRY")
    print(f"{amount_usd} USD = {Currency.EUR.convert_from_usd(amount_usd):.2f} EUR")
    print(f"Formatted: {turkish_lira.format(turkish_lira.convert_from_usd(amount_usd))}")
    
    # ==================== 7. FUNCTIONAL CREATION ====================
    print_section("7. FUNCTIONAL CREATION")
    
    print(f"Animal.DOG: {Animal.DOG}")
    print(f"Animal.CAT: {Animal.CAT}")
    print(f"Animal.BIRD: {Animal.BIRD}")
    print(f"Animal.FISH: {Animal.FISH}")
    
    for animal in Animal:
        print(f"  {animal.name}: {animal.value}")
    
    # ==================== 8. REAL-WORLD EXAMPLES ====================
    print_section("8. REAL-WORLD EXAMPLES")
    
    # Order Status
    print("--- Order Status ---")
    order_statuses = [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.DELIVERED]
    for status in order_statuses:
        print(f"  {status.value}: can_cancel={status.can_cancel()}, can_refund={status.can_refund()}, completed={status.is_completed()}")
    
    # Payment Methods
    print("\n--- Payment Methods ---")
    payment = PaymentMethod.CREDIT_CARD
    print(f"  {payment.value}: online={payment.is_online()}, approval={payment.requires_approval()}")
    
    payment = PaymentMethod.BANK_TRANSFER
    print(f"  {payment.value}: online={payment.is_online()}, approval={payment.requires_approval()}")
    
    # Log Levels
    print("\n--- Log Levels ---")
    log_level = LogLevel.WARNING
    print(f"  {log_level}: {log_level.value}")
    print(f"  Is WARNING higher than INFO? {log_level.is_higher_than(LogLevel.INFO)}")
    print(f"  Is WARNING higher than ERROR? {log_level.is_higher_than(LogLevel.ERROR)}")
    
    # ==================== 9. UTILITY FUNCTIONS ====================
    print_section("9. UTILITY FUNCTIONS")
    
    print(f"Enum to dict (Priority): {enum_to_dict(Priority)}")
    print(f"Enum to list (Priority): {enum_to_list(Priority)}")
    print(f"Enum values (Priority): {enum_values(Priority)}")
    print(f"Find by value: {find_enum_by_value(Color, 2)}")
    print(f"Find by value (not found): {find_enum_by_value(Color, 99)}")
    
    # ==================== 10. SUMMARY ====================
    print_section("SUMMARY")
    print("""
Enum - Key Concepts:

1. What is Enum?
   - Set of named constants
   - Type-safe
   - More readable than integers/strings

2. Features:
   - Auto values (auto())
   - Methods inside enum
   - Custom properties
   - Inheritance support
   - Value checking

3. Benefits:
   - Code completion support
   - Type safety
   - Better readability
   - Easy to maintain
   - Prevents typos

4. When to Use:
   - Status codes
   - Constants
   - Configuration values
   - Domain values
   - Lookup tables

5. Enum Methods:
   - .name - Get name
   - .value - Get value
   - Enum['NAME'] - Get by name
   - Enum(value) - Get by value
    
6. Comparison:
   - Basic Enum: Simple constants
   - IntEnum: Works with integers
   - auto(): Auto-generated values
   - @unique: Prevent duplicates
    """)
    
    print("="*60)
    print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
