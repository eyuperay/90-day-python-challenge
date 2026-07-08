def validate_positive_int(value: int, field_name: str = "value") -> int:
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value