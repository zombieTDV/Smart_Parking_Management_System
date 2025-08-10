from config.setting import settings

def fee_calculator(second: int) -> float:
    """
    Tính phí đỗ xe dựa trên thời gian đỗ.
    Args:
        second (int): Số giây xe đỗ.
    Returns: float
    """
    if second <= 0:
        return 0.0

    hourly_rate = settings.cfg["parking_slot"]["hourly_rates"]

    # Convert seconds to hours and round to the nearest whole hour
    hours = round(second / 3600)

    fee = hours * hourly_rate
    return float(fee)
