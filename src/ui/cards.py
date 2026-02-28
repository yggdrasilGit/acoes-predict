import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data(ttl=60 * 60)  # 1 hora
def fetch_traditional_info(tickers: list[str]) -> pd.DataFrame:
    rows = []
    for t in tickers:
        row = {"Ticker": t, "Status": "OK"}

        try:
            tk = yf.Ticker(t)

            # 1) tenta fast_info (leve)
            fi = {}
            try:
                fi = tk.fast_info or {}
            except Exception:
                fi = {}

            # se fast_info veio vazio, tenta get_info/info (mais pesado)
            info = {}
            if not fi:
                try:
                    # versões mais novas têm get_info()
                    info = tk.get_info() if hasattr(tk, "get_info") else (tk.info or {})
                except Exception:
                    info = {}

            # preencher campos comuns (usa o que tiver)
            row.update({
                "Moeda": fi.get("currency") or info.get("currency"),
                "Preço": fi.get("last_price") or info.get("regularMarketPrice"),
                "Fech. Ant.": fi.get("previous_close") or info.get("regularMarketPreviousClose"),
                "Market Cap": fi.get("market_cap") or info.get("marketCap"),
                "Setor": info.get("sector"),
                "Indústria": info.get("industry"),
                "P/L (trailing)": info.get("trailingPE"),
                "DY (%)": (info.get("dividendYield") * 100) if isinstance(info.get("dividendYield"), (int, float)) else None,
                "52w High": info.get("fiftyTwoWeekHigh"),
                "52w Low": info.get("fiftyTwoWeekLow"),
                "Website": info.get("website"),
            })

            # se mesmo assim não veio nada útil, marca status
            useful = any(row.get(k) is not None for k in ["Preço", "Market Cap", "Setor", "P/L (trailing)"])
            if not useful:
                row["Status"] = "Sem dados (possível bloqueio/limite Yahoo)"

        except Exception as e:
            row["Status"] = f"Erro: {type(e).__name__}"

        rows.append(row)

    return pd.DataFrame(rows)


def show_bottom_cards(pred_df: pd.DataFrame | None, df_close_1y: pd.DataFrame, tickers: list[str]):
    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.subheader("Previsões (ARIMA)")
            if pred_df is None or pred_df.empty:
                st.info("Treine o ARIMA para ver as previsões.")
            else:
                st.dataframe(pred_df, width="stretch", height=260)

    with c2:
        with st.container(border=True):
            st.subheader("Retorno acumulado (1 ano)")
            if df_close_1y is None or df_close_1y.empty:
                st.info("Sem dados de 1 ano (Yahoo pode ter bloqueado).")
            else:
                first = df_close_1y.iloc[0]
                last = df_close_1y.iloc[-1]
                ret = (last / first - 1.0).sort_values(ascending=False)
                st.dataframe((ret * 100).round(2).rename("Return 1Y (%)").to_frame(),
                             width="stretch", height=260)

    with c3:
        with st.container(border=True):
            st.subheader("Dados tradicionais (Yahoo)")

            # botão pra forçar “pesquisar de novo” (limpa cache)
            col_a, col_b = st.columns([1, 1])
            with col_a:
                atualizar = st.button("Atualizar", use_container_width=True)
            with col_b:
                st.caption("Cache 1h")

            if atualizar:
                st.cache_data.clear()

            if not tickers:
                st.info("Carregue dados (Buscar) para ver os tradicionais.")
            else:
                info_df = fetch_traditional_info(tickers)
                st.dataframe(info_df, width="stretch", height=260)