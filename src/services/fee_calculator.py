from config.setting import settings
import math

def fee_calculator(second: int) -> float:
    """
    Tính phí đỗ xe dựa trên thời gian đỗ.
    """
    if second <= 0:
        return 0.0

    hourly_rate = settings.cfg["parking_slot"]["hourly_rates"]

    # Convert seconds to hours and always round up
    hours = math.ceil(second / 3600) if second > 0 else 0

    fee = hours * hourly_rate
    return float(fee)