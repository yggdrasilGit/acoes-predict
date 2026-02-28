from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    cache_dir: str = "cache_csv"
    max_tickers: int = 8
    default_tickers: str = "PETR4.SA, VALE3.SA"
    default_period_qty: int = 30
    default_period_unit: str = "Dias"  # Dias | Meses | Anos