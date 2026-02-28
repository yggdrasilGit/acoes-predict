# Acoes Predict

Projeto para analise, modelagem e previsao de acoes utilizando machine learning e series temporais.  
O foco atual e o mercado brasileiro, com exemplos usando PETR4.

O repositorio contem pipeline completo desde coleta de dados ate avaliacao e salvamento de modelos.

---

## Estrutura do projeto

```

acoes-predict/
│
├── src/
│   ├── api/
│   ├── components/
│   ├── core/
│   ├── data/
│   ├── models/
│   └── ui/
│
├── cache_csv/
├── outputs/
│   ├── graficos/
│   └── resultados/
│
├── analise_acoes.ipynb
├── app.py
├── deploy.sh
├── acao.pem
├── .gitignore
└── pyvenv.cfg

```

### Descricao das pastas

- `src/`: codigo principal do projeto organizado em modulos.
- `cache_csv/`: cache local para dados baixados.
- `outputs/`: resultados gerados automaticamente.
  - `graficos/`: visualizacoes.
  - `resultados/`: rankings e modelos.
- `analise_acoes.ipynb`: notebook principal de analise e treinamento.
- `app.py`: possivel API ou interface de execucao.
- `deploy.sh`: script de deploy.
- `acao.pem`: chave para acesso a servidor (nao deve ser versionada).

---

## Funcionalidades

- Download de dados financeiros via Yahoo Finance.
- Criacao de features para previsao de retornos.
- Analise exploratoria de dados (EDA).
- Validacao com TimeSeriesSplit.
- Comparacao de varios modelos:
  - Regressao Linear
  - ElasticNet e LASSO
  - Random Forest
  - Gradient Boosting
  - SVR
  - MLP
  - KNN
- Avaliacao multi-horizonte (curto, medio e longo prazo).
- Salvamento de modelos e resultados.

---

## Requisitos

Python 3.10 ou superior.

Bibliotecas principais:

```

pandas
numpy
matplotlib
seaborn
scikit-learn
statsmodels
yfinance
tensorflow
keras
joblib
requests

````

---

## Instalacao

Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
````

Instale as dependencias:

```bash
pip install -U pip
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels yfinance tensorflow joblib requests
```

---

## Como executar

### Notebook

```bash
jupyter lab
```

Abra `analise_acoes.ipynb` e execute todas as celulas.

Os resultados serao salvos automaticamente em `outputs/`.

---

### Execucao por script

Se configurado no notebook:

```python
if __name__ == "__main__":
    run()
```

Execute as celulas correspondentes.

---

## Configuracoes

O projeto permite configuracoes como:

* Horizonte de previsao.
* Periodo historico.
* Divisao treino/teste.
* Numero de folds na validacao.
* Pastas de saida.

Esses parametros podem ser ajustados diretamente no notebook.

---

## Exemplo de uso

Treinar e salvar modelos:

1. Execute o notebook.
2. Os rankings serao salvos em:

   ```
   outputs/resultados/
   ```

Carregar modelo salvo:

```python
import joblib

model = joblib.load("outputs/resultados/model.pkl")
```

---

## Observacoes

Este projeto possui objetivo educacional e experimental.
Nao constitui recomendacao de investimento.

Resultados passados nao garantem performance futura.

---

## Seguranca

Nunca envie arquivos sensiveis como:

* chaves `.pem`
* credenciais
* tokens

Adicione esses arquivos ao `.gitignore`.

---

## Licenca

Escolha uma licenca como MIT ou Apache 2.0.


