"""
Deploy Script - Modelo de Predição de Churn Telco
===================================================

Este script fornece funções para carregar e utilizar o modelo treinado
para predição de churn de clientes de telecomunicações.

Autor: Pedro Henrique Costa
Projeto: Ciência de Dados N3
"""

import joblib
import pandas as pd
import numpy as np
import os

# Constantes
RANDOM_STATE = 42

# Lista de features originais (antes do encoding)
ORIGINAL_FEATURES = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

# Features após One-Hot Encoding (geradas pelo treino)
ENCODED_FEATURE_NAMES = [
    'SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
    'gender_Male', 'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaperlessBilling_Yes',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]


def carregar_modelo(caminho_modelo: str = None):
    """
    Carrega o modelo treinado a partir do arquivo .pkl

    Args:
        caminho_modelo: Caminho para o arquivo do modelo. 
                       Se None, procura em locais padrão.

    Returns:
        Modelo carregado pronto para predições

    Raises:
        FileNotFoundError: Se o modelo não for encontrado
    """
    # Caminhos possíveis para o modelo
    caminhos_possiveis = [
        caminho_modelo,
        '../modelo_final.pkl',
        './modelo_final.pkl',
        'modelo_final.pkl',
        os.path.join(os.path.dirname(__file__), '..', 'modelo_final.pkl')
    ]

    for caminho in caminhos_possiveis:
        if caminho and os.path.exists(caminho):
            modelo = joblib.load(caminho)
            print(f"✅ Modelo carregado de: {caminho}")
            return modelo

    raise FileNotFoundError(
        "Modelo não encontrado. Verifique se o arquivo 'modelo_final.pkl' existe."
    )


def preprocessar_dados(dados_cliente: dict, feature_names: list = None):
    """
    Preprocessa os dados de um novo cliente para predição.
    Aplica One-Hot Encoding e garante compatibilidade com o modelo.

    Args:
        dados_cliente: Dicionário com os dados do cliente
        feature_names: Lista de nomes das features após encoding.
                      Se None, usa lista padrão ENCODED_FEATURE_NAMES.

    Returns:
        DataFrame preprocessado pronto para predição
    """
    if feature_names is None:
        feature_names = ENCODED_FEATURE_NAMES

    # Convertendo para DataFrame
    df = pd.DataFrame([dados_cliente])

    # Aplicando One-Hot Encoding
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Criar DataFrame com todas as colunas esperadas, inicialmente com zeros
    df_final = pd.DataFrame(0, index=[0], columns=feature_names)

    # Preencher com os valores do encoding
    for col in df_encoded.columns:
        if col in df_final.columns:
            df_final[col] = df_encoded[col].values

    return df_final


def fazer_predicao(modelo, dados_preprocessados):
    """
    Faz a predição de churn para os dados fornecidos.

    Args:
        modelo: Modelo carregado
        dados_preprocessados: DataFrame preprocessado

    Returns:
        Tuple contendo (predição, probabilidades)
    """
    predicao = modelo.predict(dados_preprocessados)
    probabilidades = modelo.predict_proba(dados_preprocessados)

    return predicao, probabilidades


def prever_churn(dados_cliente: dict, modelo=None, feature_names: list = None):
    """
    Função principal que realiza todo o fluxo de predição.

    Args:
        dados_cliente: Dicionário com os dados do cliente
        modelo: Modelo já carregado (opcional, carrega automaticamente se None)
        feature_names: Lista de features do modelo

    Returns:
        Dicionário com resultado da predição
    """
    # Carregar modelo se não fornecido
    if modelo is None:
        modelo = carregar_modelo()

    # Preprocessar dados
    dados_prep = preprocessar_dados(dados_cliente, feature_names)

    # Fazer predição
    predicao, probabilidades = fazer_predicao(modelo, dados_prep)

    # Preparar resultado
    resultado = {
        'predicao': 'CHURN' if predicao[0] == 1 else 'NÃO CHURN',
        'codigo_predicao': int(predicao[0]),
        'probabilidade_nao_churn': float(probabilidades[0][0]),
        'probabilidade_churn': float(probabilidades[0][1]),
        'risco': 'ALTO' if probabilidades[0][1] > 0.7 else 
                 'MÉDIO' if probabilidades[0][1] > 0.4 else 'BAIXO'
    }

    return resultado


def exibir_resultado(resultado: dict):
    """
    Exibe o resultado da predição de forma formatada.

    Args:
        resultado: Dicionário com resultado da predição
    """
    print("\n" + "=" * 60)
    print("RESULTADO DA PREDIÇÃO DE CHURN")
    print("=" * 60)
    print(f"\n🎯 Predição: {resultado['predicao']}")
    print(f"⚠️  Nível de Risco: {resultado['risco']}")
    print(f"\n📊 Probabilidades:")
    print(f"   - Não Churn: {resultado['probabilidade_nao_churn']:.2%}")
    print(f"   - Churn:     {resultado['probabilidade_churn']:.2%}")

    if resultado['codigo_predicao'] == 1:
        print("\n⚠️  ALERTA: Este cliente tem alta probabilidade de cancelar!")
        print("   Recomendação: Contatar para oferecer benefícios de retenção.")
    else:
        print("\n✅ Este cliente tem baixa probabilidade de cancelar.")
    print("=" * 60)


# ============================================================
# EXEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMONSTRAÇÃO DO SCRIPT DE DEPLOY")
    print("=" * 60)

    # Exemplo de cliente de alto risco
    cliente_alto_risco = {
        'SeniorCitizen': 0,
        'tenure': 2,
        'MonthlyCharges': 89.90,
        'TotalCharges': 179.80,
        'gender': 'Male',
        'Partner': 'No',
        'Dependents': 'No',
        'PhoneService': 'Yes',
        'MultipleLines': 'Yes',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check'
    }

    # Exemplo de cliente de baixo risco
    cliente_baixo_risco = {
        'SeniorCitizen': 0,
        'tenure': 48,
        'MonthlyCharges': 45.50,
        'TotalCharges': 2184.00,
        'gender': 'Female',
        'Partner': 'Yes',
        'Dependents': 'Yes',
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Two year',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Bank transfer (automatic)'
    }

    print("\n📋 Testando com Cliente de ALTO RISCO:")
    print("-" * 40)
    try:
        resultado_alto = prever_churn(cliente_alto_risco)
        exibir_resultado(resultado_alto)
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("Execute primeiro o notebook para gerar o modelo.")

    print("\n📋 Testando com Cliente de BAIXO RISCO:")
    print("-" * 40)
    try:
        resultado_baixo = prever_churn(cliente_baixo_risco)
        exibir_resultado(resultado_baixo)
    except FileNotFoundError as e:
        print(f"⚠️  {e}")
        print("Execute primeiro o notebook para gerar o modelo.")
