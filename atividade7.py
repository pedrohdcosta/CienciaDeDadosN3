import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 100)
plt.rcParams["figure.figsize"] = (8, 5)

# Carregamento — Telco (link estável)
# Fonte alternativa pública: datasciencedojo/datasets
telco_url = "/content/WA_Fn-UseC_-Telco-Customer-Churn.csv"
df_churn = pd.read_csv(telco_url)

print("Dimensão:", df_churn.shape)
df_churn.head()

buffer = io.StringIO()
df_churn.info(buf=buffer)
print(buffer.getvalue())

display(df_churn.describe(include="all").T.head(20))

# Limpeza TotalCharges
df_churn["TotalCharges"] = pd.to_numeric(df_churn["TotalCharges"], errors="coerce")
na_before = df_churn.isna().sum()
df_churn = df_churn.dropna(subset=["TotalCharges"]).copy()
na_after = df_churn.isna().sum()

print("\nAusentes antes (TotalCharges pode conter espaços):\n", na_before[na_before>0])
print("\nAusentes após tratamento:\n", na_after[na_after>0])

churn_counts = df_churn["Churn"].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(churn_counts.index, churn_counts.values)
ax.set_title("Distribuição de Churn")
ax.set_xlabel("Churn")
ax.set_ylabel("Contagem")
for i, v in enumerate(churn_counts.values):
    ax.text(i, v + max(churn_counts.values)*0.01, str(v), ha='center', va='bottom', fontsize=9)
plt.show()

(churn_counts / churn_counts.sum()).rename("proporcao")

def stacked_bar_by_target(df, cat_col, target="Churn"):
    ctab = pd.crosstab(df[cat_col], df[target], normalize="index")
    fig, ax = plt.subplots()
    bottom = np.zeros(ctab.shape[0])
    for cls in ctab.columns:
        ax.bar(ctab.index, ctab[cls].values, bottom=bottom, label=str(cls))
        bottom += ctab[cls].values
    ax.set_title(f"Proporção de {target} por {cat_col}")
    ax.set_xlabel(cat_col); ax.set_ylabel("Proporção")
    ax.legend(title=target); plt.xticks(rotation=0); plt.show()
    return ctab

ctab_contract = stacked_bar_by_target(df_churn, "Contract")
ctab_internet = stacked_bar_by_target(df_churn, "InternetService")
ctab_partner  = stacked_bar_by_target(df_churn, "Partner")

ctab_contract, ctab_internet, ctab_partner

def boxplot_by_target(df, target, num_col):
    groups = [df[df[target]==cls][num_col].dropna().values for cls in df[target].unique()]
    labels = list(df[target].unique())
    fig, ax = plt.subplots()
    ax.boxplot(groups, labels=labels, showmeans=True)
    ax.set_title(f"Distribuição de {num_col} por {target}")
    ax.set_xlabel(target); ax.set_ylabel(num_col); plt.show()

boxplot_by_target(df_churn, "Churn", "tenure")
boxplot_by_target(df_churn, "Churn", "MonthlyCharges")

auto_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
colnames = [
    "symboling","normalized-losses","make","fuel-type","aspiration","num-of-doors",
    "body-style","drive-wheels","engine-location","wheel-base","length","width",
    "height","curb-weight","engine-type","num-of-cylinders","engine-size","fuel-system",
    "bore","stroke","compression-ratio","horsepower","peak-rpm","city-mpg","highway-mpg",
    "price"
]
df_cars = pd.read_csv(auto_url, header=None, names=colnames, na_values="?")
print("Dimensão:", df_cars.shape)
df_cars.head()

numeric_cols = [
    "normalized-losses","wheel-base","length","width","height","curb-weight",
    "engine-size","bore","stroke","compression-ratio","horsepower","peak-rpm",
    "city-mpg","highway-mpg","price"
]
for c in numeric_cols:
    df_cars[c] = pd.to_numeric(df_cars[c], errors="coerce")

na_before = df_cars.isna().sum()
df_cars = df_cars.dropna(subset=["price"]).copy()
na_after = df_cars.isna().sum()

buffer = io.StringIO()
df_cars.info(buf=buffer)
print(buffer.getvalue())

display(df_cars.describe(include="all").T.head(20))
print("\nAusentes antes:\n", na_before[na_before>0])
print("\nAusentes após drop price:\n", na_after[na_after>0])

fig, ax = plt.subplots()
ax.hist(df_cars["price"].dropna(), bins=30, edgecolor="black")
ax.set_title("Distribuição de Preços (Automobile)")
ax.set_xlabel("price"); ax.set_ylabel("freq")
plt.show()

def boxplot_cat_y(df, cat_col, y="price"):
    groups = [df[df[cat_col]==val][y].dropna().values for val in df[cat_col].dropna().unique()]
    labels = list(df[cat_col].dropna().unique())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(groups, labels=labels, showmeans=True)
    ax.set_title(f"{y} por {cat_col}")
    ax.set_xlabel(cat_col); ax.set_ylabel(y)
    plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()

boxplot_cat_y(df_cars, "make", "price")
boxplot_cat_y(df_cars, "body-style", "price")

numdf = df_cars.select_dtypes(include=[np.number]).dropna(axis=1, how="all").copy()
corr = numdf.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(8,6))
cax = ax.imshow(corr, interpolation="nearest")
ax.set_title("Correlação entre Variáveis Numéricas")
fig.colorbar(cax)
ax.set_xticks(range(len(numdf.columns)))
ax.set_yticks(range(len(numdf.columns)))
ax.set_xticklabels(numdf.columns, rotation=90)
ax.set_yticklabels(numdf.columns)
plt.tight_layout(); plt.show()

corr["price"].sort_values(ascending=False).head(10)

