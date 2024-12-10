def is_valid_pin(pin: str) -> bool:
    """Validates that the PIN is a 4-digit numeric string."""
    return pin.isdigit() and len(pin) == 4

def is_valid_name(name: str) -> bool:
    """Validates that the name is non-empty and contains only alphabets."""
    return name.isalpha() and len(name.strip()) > 0

def is_valid_amount(amount: str) -> bool:
    """Validates that the amount is a positive number with up to 2 decimal places."""
    try:
        value = float(amount)
        return value > 0 and round(value, 2) == value
    except ValueError:
        return False
