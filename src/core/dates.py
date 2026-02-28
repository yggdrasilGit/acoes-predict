from datetime import datetime, timedelta

def compute_date_range(qty: int, unit: str):
    """
    Sempre retorna período até ontem (para não pegar o candle de hoje).
    Retorna: (start_str, end_str, end_exclusive_str)
    """
    today = datetime.today().date()
    end = today - timedelta(days=1)

    if unit == "Dias":
        start = end - timedelta(days=qty)
    elif unit == "Meses":
        start = end - timedelta(days=qty * 30)
    else:  # "Anos"
        start = end - timedelta(days=qty * 365)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    end_exclusive = (end + timedelta(days=1)).strftime("%Y-%m-%d")  # yfinance end é exclusivo
    return start_str, end_str, end_exclusive