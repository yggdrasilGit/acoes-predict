import streamlit as st
import pandas as pd
from src.models.arima import fit_forecast

def show_ml_arima_and_get_outputs(df_close: pd.DataFrame):
    st.divider()
    st.header("Aprendizado de Máquina (ARIMA)")

    ativar = st.checkbox("Ativar ARIMA", value=False)
    if not ativar:
        return None, None

    # parâmetros
    passos = st.slider("Dias para prever", 1, 60, 7)
    c1, c2, c3 = st.columns(3)
    with c1:
        p = st.number_input("p", 0, 10, 1)
    with c2:
        d = st.number_input("d", 0, 2, 1)
    with c3:
        q = st.number_input("q", 0, 10, 1)

    # escolher ticker para o gráfico (se tiver vários)
    if df_close.shape[1] > 1:
        ticker_plot = st.selectbox("Ticker para mostrar no gráfico", list(df_close.columns))
    else:
        ticker_plot = df_close.columns[0]

    # validação rápida
    serie_plot = df_close[ticker_plot].dropna()
    min_len = max(30, int((p + d + q) * 5))
    if len(serie_plot) < min_len:
        st.warning(
            f"Poucos dados p/ ARIMA({p},{d},{q}). Tenho {len(serie_plot)}; recomendo {min_len}. "
            "Aumente o período ou reduza p/d/q."
        )
        return None, None

    treinar = st.button("Treinar e prever (todas as ações)", type="primary")
    if not treinar:
        return None, None

    # ---- Treina ARIMA para cada ticker e monta pred_df
    pred_cols = {}
    fit_info = {}
    with st.spinner("Treinando ARIMA para todas as ações..."):
        for col in df_close.columns:
            serie = df_close[col].dropna()
            if len(serie) < min_len:
                continue
            forecast, fit = fit_forecast(serie, (int(p), int(d), int(q)), int(passos))
            pred_cols[col] = forecast
            fit_info[col] = (fit.aic, fit.bic)

    if not pred_cols:
        st.error("Não consegui treinar ARIMA para nenhum ticker (dados insuficientes).")
        return None, None

    pred_df = pd.DataFrame(pred_cols)  # index = datas futuras

    # ---- plot_df só do ticker selecionado (Close + Forecast)
    plot_df = pd.DataFrame({
        f"{ticker_plot}_Close": df_close[ticker_plot].dropna(),
        "ARIMA_Forecast": pred_df[ticker_plot] if ticker_plot in pred_df.columns else None
    }).dropna(how="all")

    st.success("Previsões geradas")
    return plot_df, pred_df