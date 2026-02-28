import os
import streamlit as st

from src.core.config import AppConfig
from src.core.dates import compute_date_range
from src.data.yahoo import normalize_tickers, download_close
from src.data.cache import make_cache_key, cache_path, load_cache, save_cache
from src.ui.inputs import top_bar

# ML + cards
from src.ui.charts import show_ml_arima_and_get_outputs
from src.ui.cards import show_bottom_cards


cfg = AppConfig()

st.set_page_config(page_title="Fechamento - Cache CSV + ARIMA", layout="wide")
st.title("Fechamento (Close) com cache + ARIMA")

os.makedirs(cfg.cache_dir, exist_ok=True)

# =========================
# Inputs (top bar)
# =========================
tickers_input, qty, unit, buscar = top_bar(
    cfg.default_tickers,
    cfg.default_period_qty,
    cfg.default_period_unit
)

start_str, end_str, end_exclusive = compute_date_range(qty, unit)
st.caption(f"Período: {start_str} até {end_str} (sem incluir hoje)")

# =========================
# Session state
# =========================
if "df_close" not in st.session_state:
    st.session_state.df_close = None
if "tickers" not in st.session_state:
    st.session_state.tickers = []

# =========================
# Buscar (cache + download)
# =========================
if buscar:
    tickers = normalize_tickers(tickers_input)

    if not tickers:
        st.warning("Digite pelo menos 1 ticker.")
        st.stop()

    if len(tickers) > cfg.max_tickers:
        st.warning(f"Máximo de {cfg.max_tickers} tickers.")
        st.stop()

    # --- cache para o período selecionado
    key = make_cache_key(tickers, start_str, end_str)
    path = cache_path(cfg.cache_dir, key)

    cached = load_cache(path)
    if cached is not None:
        st.session_state.df_close = cached
        st.session_state.tickers = tickers
        st.success(f"Cache carregado ({os.path.basename(path)}) — sem chamar Yahoo")
    else:
        with st.spinner("Baixando do Yahoo..."):
            df_close = download_close(tickers, start_str, end_exclusive)

        if df_close is None or df_close.empty:
            st.error("Erro ao baixar (ticker errado, 429/bloqueio, feriado etc.).")
            st.stop()

        save_cache(df_close, path)
        st.session_state.df_close = df_close
        st.session_state.tickers = tickers
        st.success(f"💾 Cache salvo ({os.path.basename(path)})")

df_close = st.session_state.df_close
tickers = st.session_state.tickers

# =========================
# Layout do dashboard
# =========================
if df_close is None:
    st.info("Digite os tickers e clique em **Buscar**.")
    st.stop()

# 1) ML ENTRE inputs e tabela
plot_df, pred_df = show_ml_arima_and_get_outputs(df_close)

# 2) Tabela últimos 5 dias
st.subheader("Fechamento (Close) — últimos 5 dias")
st.dataframe(df_close.tail(5), width="stretch")

# 3) Gráfico (Close + previsão no mesmo gráfico)
st.subheader("Gráfico (Close + Previsão)")
if plot_df is not None and not plot_df.empty:
    st.line_chart(plot_df)
else:
    st.line_chart(df_close)

# 4) Dados de 1 ano (com cache e sem quebrar)
start_1y, end_1y, end_exc_1y = compute_date_range(365, "Dias")

key_1y = make_cache_key(tickers, start_1y, end_1y)
path_1y = cache_path(cfg.cache_dir, key_1y)

cached_1y = load_cache(path_1y)
if cached_1y is not None:
    df_close_1y = cached_1y
else:
    df_close_1y = download_close(tickers, start_1y, end_exc_1y)
    if df_close_1y is not None and not df_close_1y.empty:
        save_cache(df_close_1y, path_1y)

if df_close_1y is None or df_close_1y.empty:
    st.warning("Não consegui baixar dados de 1 ano agora (Yahoo pode estar bloqueando). O card de retorno 1 ano ficará vazio.")

# 5) 3 cards no final
show_bottom_cards(pred_df, df_close_1y, tickers)