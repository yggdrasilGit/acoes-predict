import streamlit as st

def top_bar(default_tickers: str, default_qty: int, default_unit: str):
    """
    Cria a barra superior de entrada de dados do dashboard.

    Essa função organiza os inputs do usuário em 4 colunas:
    1. Campo de texto para inserir os tickers (ações)
    2. Quantidade do período (ex: 30)
    3. Unidade de tempo (Dias, Meses ou Anos)
    4. Botão para iniciar a busca dos dados

    Parâmetros
    ----------
    default_tickers : str
        Lista padrão de tickers exibida no campo de texto.
        Exemplo: "PETR4.SA, VALE3.SA"

    default_qty : int
        Quantidade padrão do período a ser analisado.

    default_unit : str
        Unidade de tempo padrão.
        Deve ser uma das opções:
        ["Dias", "Meses", "Anos"]

    Retorno
    -------
    tuple
        (tickers_input, qty, unit, buscar)

        tickers_input : str
            Texto digitado pelo usuário com os tickers.

        qty : int
            Quantidade do período selecionado.

        unit : str
            Unidade de tempo escolhida.

        buscar : bool
            Indica se o botão de busca foi pressionado.
    """

    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

    with col1:
        tickers_input = st.text_input(
            "Tickers (até 8) separados por vírgula",
            default_tickers
        )

    with col2:
        qty = st.number_input(
            "Qtd",
            min_value=1,
            max_value=3650,
            value=default_qty,
            step=1
        )

    with col3:
        unit = st.selectbox(
            "Unidade",
            ["Dias", "Meses", "Anos"],
            index=["Dias", "Meses", "Anos"].index(default_unit)
        )

    with col4:
        buscar = st.button(
            "Buscar",
            use_container_width=True
        )

    return tickers_input, int(qty), unit, buscar