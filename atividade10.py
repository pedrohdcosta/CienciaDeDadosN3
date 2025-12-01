import os, sys, textwrap, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


def h2(txt): display(Markdown(f"## {txt}"))
def h3(txt): display(Markdown(f"### {txt}"))
def p(txt):  display(Markdown(txt))

RANDOM_STATE = 42
np.set_printoptions(suppress=True, linewidth=120)
pd.set_option("display.max_columns", 100)

# Procurar automaticamente o CSV do Telco Churn
CANDIDATES = [
    "WA_Fn-UseC_-Telco-Customer-Churn.csv",                 # nome padrão
    "/content/WA_Fn-UseC_-Telco-Customer-Churn.csv",        # Colab comum
    "telco_churn.csv"                                       # alternativo
]

DATA_PATH = next((p for p in CANDIDATES if os.path.exists(p)), None)

if DATA_PATH is None:
    from google.colab import files  # type: ignore
    print("Arquivo de Churn não encontrado. Faça upload do CSV (ex.: WA_Fn-UseC_-Telco-Customer-Churn.csv).")
    uploaded = files.upload()
    DATA_PATH = list(uploaded.keys())[0]

df_churn = pd.read_csv(DATA_PATH)
h2("Amostra do dataset de Churn")
df_churn.head(3)

# Limpeza coerente com a Aula 08
df = df_churn.copy()

# TotalCharges como numérico (há strings vazias); coagir e remover NaN resultantes
if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges"]).reset_index(drop=True)

# Target
target_col = "Churn"
y = (df[target_col].astype(str).str.strip().str.lower() == "yes").astype(int)

# Drop ID e target
drop_cols = [c for c in ["customerID", target_col] if c in df.columns]
X = df.drop(columns=drop_cols)

# Detectar tipos
cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
num_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()

preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ],
    remainder="drop"
)

modelo_arvore = DecisionTreeClassifier(max_depth=4, random_state=RANDOM_STATE)

pipe_cls = Pipeline([
    ("prep", preprocess),
    ("clf", modelo_arvore)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

pipe_cls.fit(X_train, y_train)
y_pred = pipe_cls.predict(X_test)

h2("Treino concluído — Classificação (Churn)")
p(f"- Linhas treino: {len(X_train)} | teste: {len(X_test)}")

cm = confusion_matrix(y_test, y_pred)
report_text = classification_report(y_test, y_pred, target_names=["Não Churn", "Churn"])

fig = plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Não Churn","Churn"], yticklabels=["Não Churn","Churn"])
plt.xlabel("Previsto")
plt.ylabel("Real")
plt.title("Matriz de Confusão — Churn")
plt.show()

h3("Relatório de Classificação")
print(report_text)

scores_acc = cross_val_score(pipe_cls, X, y, cv=5, scoring="accuracy")
h3("Resultados da Validação Cruzada (cv=5) — Acurácia")
print("Acurácias por fold:", np.round(scores_acc, 3))
print(f"Acurácia Média: {scores_acc.mean():.2%}")
print(f"Desvio Padrão: {scores_acc.std():.4f}")
acc_mean_cls = scores_acc.mean()
acc_std_cls = scores_acc.std()

# Procurar dataset de carros (ajuste o nome se necessário)
CAR_CANDIDATES = [
    "CarPrice_Assignment.csv",       # muito usado em aulas
    "car_prices.csv",
    "/content/CarPrice_Assignment.csv"
]
CAR_PATH = next((p for p in CAR_CANDIDATES if os.path.exists(p)), None)

if CAR_PATH is None:
    try:
        from google.colab import files  # type: ignore
        print("Dataset de carros não encontrado. Faça upload (ex.: CarPrice_Assignment.csv).")
        uploaded = files.upload()
        CAR_PATH = list(uploaded.keys())[0]
    except Exception as e:
        raise FileNotFoundError("Faça upload do dataset de carros para prosseguir.")

df_car = pd.read_csv(CAR_PATH)

# Heurística para detectar a coluna alvo (price/preco)
candidate_targets = [c for c in df_car.columns if c.lower() in ["price","preco","selling_price","saleprice"]]
if not candidate_targets:
    raise ValueError("Não encontrei a coluna de preço. Renomeie a coluna alvo para 'price' (ou 'preco').")

y_car = df_car[candidate_targets[0]].astype(float)
X_car = df_car.drop(columns=[candidate_targets[0]])

cat_cols_car = X_car.select_dtypes(include=["object", "category"]).columns.tolist()
num_cols_car = X_car.select_dtypes(include=["number", "bool"]).columns.tolist()

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

prep_car = ColumnTransformer(
    transformers=[
        ("num", "passthrough", num_cols_car),
        ("cat", OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols_car),
    ],
    remainder="drop"
)

pipe_reg = Pipeline([
    ("prep", prep_car),
    ("reg", LinearRegression())
])

from sklearn.model_selection import cross_val_score
scores_rmse = cross_val_score(pipe_reg, X_car, y_car, cv=5, scoring="neg_root_mean_squared_error")
rmse_per_fold = -scores_rmse
rmse_mean = rmse_per_fold.mean()
rmse_std  = rmse_per_fold.std()

h3("Resultados da Validação Cruzada (cv=5) — RMSE")
print("RMSE por fold:", np.round(rmse_per_fold, 2))
print(f"RMSE Médio: {rmse_mean:.2f}")
print(f"Desvio Padrão do RMSE: {rmse_std:.2f}")

summary_lines = []

summary_lines.append("### Conclusões Gerais")
summary_lines.append(
    f"- **Classificação (Churn)** — A validação cruzada indicou **acurácia média ≈ {acc_mean_cls:.2%}** "
    f"com **desvio padrão ≈ {acc_std_cls:.4f}**. Um desvio padrão baixo sugere desempenho **estável** entre folds."
)

summary_lines.append(
    "- **Matriz de Confusão/Relatório:** Avaliamos **Precisão** (qualidade das previsões positivas) e **Recall** "
    "(capacidade de capturar os positivos). Em churn, geralmente **Falso Negativo** é mais caro: perder um cliente "
    "sem agir tende a custar mais do que ofertar retenção a quem não sairia (Falso Positivo)."
)

summary_lines.append(
    "- **Regressão (Carros)** — O **RMSE médio** em validação cruzada representa um erro típico esperado em dados novos. "
    "Por se tratar de média em 5 experimentos, é mais **confiável** que uma única medição."
)

display(Markdown("\\n".join(summary_lines)))