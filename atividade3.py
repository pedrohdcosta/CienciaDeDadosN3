import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('online_gaming_behavior_dataset(in).csv')

print("Primeiras 5 linhas do dataset:")
display(df.head())

print("Informações gerais do dataset:")
df.info()

print("\nEstatísticas descritivas:")
display(df.describe())

print(f"\nDimensões do dataset: {df.shape[0]} linhas e {df.shape[1]} colunas")

print("Verificando valores ausentes por coluna:")
valores_ausentes = df.isnull().sum()
print(valores_ausentes)

if valores_ausentes.sum() == 0:
    print("\nPerfeito! Nosso dataset não tem valores ausentes.")
else:
    print("\nEncontrados valores ausentes. Vamos corrigi-los...")

    if valores_ausentes.sum() > 0:
    print("Aplicando correções...")

    colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    for coluna in colunas_numericas:
        if df[coluna].isnull().any():
            mediana = df[coluna].median()
            df[coluna].fillna(mediana, inplace=True)
            print(f"Coluna '{coluna}' preenchida com mediana: {mediana}")

    colunas_categoricas = df.select_dtypes(include=['object']).columns
    for coluna in colunas_categoricas:
        if df[coluna].isnull().any():
            moda = df[coluna].mode()[0]
            df[coluna].fillna(moda, inplace=True)
            print(f"Coluna '{coluna}' preenchida com moda: {moda}")
else:
    print("Nenhuma correção necessária para valores ausentes.")
    
duplicatas = df.duplicated().sum()
print(f"Número de linhas duplicadas encontradas: {duplicatas}")

if duplicatas > 0:
    print("Removendo linhas duplicadas...")
    formato_original = df.shape
    df.drop_duplicates(inplace=True)
    print(f"Dataset original: {formato_original}")
    print(f"Dataset após remoção: {df.shape}")
    print(f"Linhas removidas: {formato_original[0] - df.shape[0]}")
else:
    print("Excelente! Não há linhas duplicadas no dataset.")

print("Status final após limpeza:")
print(f"Valores ausentes total: {df.isnull().sum().sum()}")
print(f"Linhas duplicadas: {df.duplicated().sum()}")
print(f"Formato final do dataset: {df.shape}")

playtime_column = "PlayTimeHours"

if playtime_column in df.columns and pd.api.types.is_numeric_dtype(df[playtime_column]):
    print(f"Analisando outliers na coluna '{playtime_column}'")

    print(f"\nEstatísticas da coluna {playtime_column}:")
    print(f"Mínimo: {df[playtime_column].min():.2f} horas")
    print(f"Máximo: {df[playtime_column].max():.2f} horas")
    print(f"Média: {df[playtime_column].mean():.2f} horas")
    print(f"Mediana: {df[playtime_column].median():.2f} horas")

else:
    print(f"Coluna '{playtime_column}' não encontrada ou não é numérica")

if playtime_column in df.columns and pd.api.types.is_numeric_dtype(df[playtime_column]):

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    sns.boxplot(x=df[playtime_column])
    plt.title(f'Boxplot - {playtime_column}')
    plt.xlabel('Horas de Jogo')

    plt.subplot(1, 3, 2)
    plt.hist(df[playtime_column], bins=50, edgecolor='black', alpha=0.7)
    plt.title(f'Histograma - {playtime_column}')
    plt.xlabel('Horas de Jogo')
    plt.ylabel('Frequência')

    if 'Gender' in df.columns:
        plt.subplot(1, 3, 3)
        sns.boxplot(data=df, x='Gender', y=playtime_column)
        plt.title(f'Tempo de Jogo por Gênero')
        plt.ylabel('Horas de Jogo')

    plt.tight_layout()
    plt.show()

if playtime_column in df.columns and pd.api.types.is_numeric_dtype(df[playtime_column]):

    Q1 = df[playtime_column].quantile(0.25)
    Q3 = df[playtime_column].quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    print(f"Análise de Outliers usando método IQR:")
    print(f"Q1 (25%): {Q1:.2f}")
    print(f"Q3 (75%): {Q3:.2f}")
    print(f"IQR: {IQR:.2f}")
    print(f"Limite inferior: {limite_inferior:.2f}")
    print(f"Limite superior: {limite_superior:.2f}")

    outliers_mask = (df[playtime_column] < limite_inferior) | (df[playtime_column] > limite_superior)
    num_outliers = outliers_mask.sum()

    print(f"\nOutliers encontrados: {num_outliers} ({num_outliers/len(df)*100:.1f}% dos dados)")

    if num_outliers > 0:
        print(f"\nExemplos de valores outliers:")
        outliers_sample = df[outliers_mask][playtime_column].head(10)
        print(outliers_sample.tolist())

if playtime_column in df.columns and pd.api.types.is_numeric_dtype(df[playtime_column]):

    outliers_mask = (df[playtime_column] < limite_inferior) | (df[playtime_column] > limite_superior)
    df_sem_outliers = df[~outliers_mask].copy()

    print(f"Comparação de datasets:")
    print(f"Dataset original: {df.shape[0]} registros")
    print(f"Dataset sem outliers: {df_sem_outliers.shape[0]} registros")
    print(f"Registros que seriam perdidos: {df.shape[0] - df_sem_outliers.shape[0]}")

    print(f"\nComparação de estatísticas:")
    print(f"Média original: {df[playtime_column].mean():.2f} horas")
    print(f"Média sem outliers: {df_sem_outliers[playtime_column].mean():.2f} horas")
    print(f"Desvio padrão original: {df[playtime_column].std():.2f} horas")
    print(f"Desvio padrão sem outliers: {df_sem_outliers[playtime_column].std():.2f} horas")

    print(f"\nDECISÃO FINAL: Manter todos os registros incluindo outliers")
    print(f"Justificativa: Os valores extremos representam comportamentos válidos de diferentes tipos de jogadores")

print("RESUMO FINAL DO DATASET LIMPO")
print("=" * 50)
print(f"Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
print(f"Valores ausentes: {df.isnull().sum().sum()}")
print(f"Linhas duplicadas: {df.duplicated().sum()}")
print(f"Colunas numéricas: {len(df.select_dtypes(include=['int64', 'float64']).columns)}")
print(f"Colunas categóricas: {len(df.select_dtypes(include=['object']).columns)}")

print("\nColunas disponíveis para análise:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col} ({df[col].dtype})")

print("\nDataset pronto para análise exploratória!")