from decimal import Decimal, getcontext

# Set precision for Decimal calculations
getcontext().prec = 10

# Base charge and charge per minute
base_charge = 25
charge_per_minute = Decimal("0.15")


def telephone(minute: int, fail_time: int) -> str:
    """
    Calculate the total telephone charge based on the duration of the call (in minutes)
    and the number of failure times. Applies discounts based on the duration of the call.

    Args:
        minute (int): The duration of the call in minutes.
        fail_time (int): The number of failure times during the call.

    Returns:
        str: The total charge as a string.
    """

    # Validate input
    if minute < 0:
        return "minute can't be negative"
    elif minute > 31 * 24 * 60:
        return "minute exceeded"

    if fail_time < 0:
        return "fail time can't be negative"

    # Initialize variables for maximum allowable fail time and discount rate
    max_fail_time = 0
    discount = Decimal("0.0")

    # Determine the discount and maximum fail time based on call duration
    if 0 < minute <= 60:
        max_fail_time = 1
        discount = Decimal("0.01")
    elif 60 < minute <= 120:
        max_fail_time = 2
        discount = Decimal("0.015")
    elif 120 < minute <= 180:
        max_fail_time = 3
        discount = Decimal("0.02")
    elif 180 < minute <= 300:
        max_fail_time = 3
        discount = Decimal("0.025")
    elif minute > 300:
        max_fail_time = 6
        discount = Decimal("0.03")

    # Calculate the total charge
    effective_discount = discount if fail_time <= max_fail_time else Decimal(
        "0.0")
    total_charge = base_charge + minute * \
        charge_per_minute * (1 - effective_discount)

    return str(total_charge.normalize())


if __name__ == "__main__":
    # Example usage
    print(telephone(3000, 1))
