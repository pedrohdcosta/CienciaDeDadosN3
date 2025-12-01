import os, sys, io
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Versões:")
import sklearn, pandas
print("sklearn:", sklearn.__version__, " | pandas:", pandas.__version__)

try:
    url_a = "https://raw.githubusercontent.com/marvin-rubia/Churn-Analysis-Prediction/main/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(url_a, encoding="utf-8")
    source = "URL A (WA_Fn-UseC_)"
except Exception as e_a:
    print("Falha na URL A:", e_a)
    df = None

# ====== Opção 3 — URL alternativa (GitHub - opção B) ======
if df is None:
    try:
        url_b = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
        df = pd.read_csv(url_b, encoding="utf-8")
        source = "URL B (IBM)"
    except Exception as e_b:
        print("Falha na URL B:", e_b)

if df is None:
    raise RuntimeError("Não foi possível carregar o dataset pelas URLs. Tente a Opção 1 (upload manual).")

print("Fonte carregada:", source)
print("Dimensão bruta:", df.shape)
df.head(3)


# ====== Limpeza coerente com EDA (Aula 07) ======
# 1) Converter TotalCharges para numérico (algumas linhas vêm como string vazia ou espaços)
if 'TotalCharges' in df.columns:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# 2) Remover linhas com NA (alternativamente, poderíamos imputar)
df_clean = df.dropna(axis=0).copy()

# 3) Garantir target como Série simples e consistente
target_col = 'Churn'
if target_col not in df_clean.columns:
    raise KeyError(f"Coluna alvo '{target_col}' não encontrada no dataset. Verifique os nomes das colunas.")

# ====== Seleção de features (edite com base na SUA EDA) ======
features_selecionadas = [
    # Quantitativas
    'tenure', 'MonthlyCharges', 'TotalCharges',
    # Categóricas relevantes vistas comumente no churn
    'Contract', 'InternetService', 'PaymentMethod', 'OnlineSecurity',
    'TechSupport', 'PaperlessBilling', 'SeniorCitizen'
]

# Filtrar para colunas existentes (algumas variantes do dataset podem ter nomes diferentes)
features_existentes = [c for c in features_selecionadas if c in df_clean.columns]
if len(features_existentes) == 0:
    raise ValueError("Nenhuma das features selecionadas foi encontrada. Ajuste a lista conforme o seu CSV.")

X = df_clean[features_existentes].copy()
y = df_clean[target_col].copy()

print("Features usadas:", features_existentes)
print("Formato X:", X.shape, "| Formato y:", y.shape)

# ====== Codificação de categóricas ======
X_encoded = pd.get_dummies(X, drop_first=True)

print("--- Dimensões de X antes/depois ---")
print("X original:", X.shape, "| X codificado:", X_encoded.shape)
X_encoded.head(3)

# ====== Divisão treino/teste ======
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.30, random_state=42, stratify=y
)

print(f"Tamanho treino: {X_train.shape[0]} | teste: {X_test.shape[0]}")
print("\nProporção no y_train:")
print(y_train.value_counts(normalize=True).round(3))
print("\nProporção no y_test:")
print(y_test.value_counts(normalize=True).round(3))

# ====== Treino do modelo (Decision Tree) ======
modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
modelo.fit(X_train, y_train)

# ====== Predição e métricas ======
y_pred = modelo.predict(X_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=np.unique(y_test))
report = classification_report(y_test, y_pred, digits=4)

print(f"Acurácia no teste: {acc:.2%}\n")
print("Matriz de Confusão (linhas = verdade, colunas = predição):")
print(pd.DataFrame(cm, index=[f"true_{c}" for c in np.unique(y_test)],
                      columns=[f"pred_{c}" for c in np.unique(y_test)]))
print("\nClassification Report:")
print(report)

# Visualização textual simples da árvore (opcional)
try:
    tree_txt = export_text(modelo, feature_names=list(X_train.columns))
    print("\nÁrvore (resumo textual):\n")
    print(tree_txt[:2000])
except Exception as _:
    pass

