"""
Funções Auxiliares para o Projeto de Churn

Este módulo contém funções utilitárias para análise e predição de churn.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import joblib


def carregar_e_limpar_dados(url=None, caminho_csv=None):
    """
    Carrega e limpa o dataset de churn.
    
    Parâmetros:
    -----------
    url : str, opcional
        URL para baixar o dataset
    caminho_csv : str, opcional
        Caminho local do CSV
    
    Retorna:
    --------
    DataFrame com dados limpos
    """
    # Definir URL padrão
    if url is None and caminho_csv is None:
        url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    
    # Carregar dados
    if caminho_csv:
        df = pd.read_csv(caminho_csv)
    else:
        try:
            df = pd.read_csv(url)
        except:
            url_alt = "https://raw.githubusercontent.com/marvin-rubia/Churn-Analysis-Prediction/main/WA_Fn-UseC_-Telco-Customer-Churn.csv"
            df = pd.read_csv(url_alt)
    
    # Limpeza
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df_clean = df.dropna(subset=['TotalCharges']).copy()
    
    return df_clean


def preparar_features(df, features_selecionadas=None):
    """
    Prepara features para modelagem.
    
    Parâmetros:
    -----------
    df : DataFrame
        Dataset completo
    features_selecionadas : list, opcional
        Lista de features a usar
    
    Retorna:
    --------
    X, y : DataFrames
        Features e target preparados
    """
    if features_selecionadas is None:
        features_selecionadas = [
            'tenure', 'MonthlyCharges', 'TotalCharges',
            'Contract', 'InternetService', 'PaymentMethod',
            'OnlineSecurity', 'TechSupport', 'PaperlessBilling',
            'SeniorCitizen'
        ]
    
    X = df[features_selecionadas].copy()
    y = df['Churn'].copy()
    
    return X, y


def plotar_matriz_confusao(y_true, y_pred, labels=['Não Churn', 'Churn'], 
                           titulo='Matriz de Confusão', salvar=None):
    """
    Plota matriz de confusão formatada.
    
    Parâmetros:
    -----------
    y_true : array-like
        Valores reais
    y_pred : array-like
        Valores preditos
    labels : list
        Rótulos das classes
    titulo : str
        Título do gráfico
    salvar : str, opcional
        Caminho para salvar o gráfico
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Contagem'})
    plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('Valor Real', fontsize=12)
    plt.xlabel('Valor Predito', fontsize=12)
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
    
    plt.show()


def calcular_metricas_detalhadas(y_true, y_pred, modelo_nome='Modelo'):
    """
    Calcula e exibe métricas detalhadas do modelo.
    
    Parâmetros:
    -----------
    y_true : array-like
        Valores reais
    y_pred : array-like
        Valores preditos
    modelo_nome : str
        Nome do modelo para exibição
    
    Retorna:
    --------
    dict com métricas
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label='Yes')
    rec = recall_score(y_true, y_pred, pos_label='Yes')
    f1 = f1_score(y_true, y_pred, pos_label='Yes')
    
    print(f"{'='*60}")
    print(f"MÉTRICAS - {modelo_nome}")
    print(f"{'='*60}")
    print(f"Acurácia:  {acc:.2%}")
    print(f"Precisão:  {prec:.2%}")
    print(f"Recall:    {rec:.2%}")
    print(f"F1-Score:  {f1:.2%}")
    print(f"{'='*60}\n")
    
    print("Classification Report:")
    print(classification_report(y_true, y_pred, target_names=['Não Churn', 'Churn']))
    
    return {
        'acuracia': acc,
        'precisao': prec,
        'recall': rec,
        'f1_score': f1
    }


def comparar_modelos(resultados_dict):
    """
    Compara múltiplos modelos visualmente.
    
    Parâmetros:
    -----------
    resultados_dict : dict
        Dicionário com {nome_modelo: {metricas}}
    """
    df = pd.DataFrame(resultados_dict).T
    
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    metricas = ['acuracia', 'precisao', 'recall', 'f1_score']
    titulos = ['Acurácia', 'Precisão', 'Recall', 'F1-Score']
    cores = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
    
    for idx, (metrica, titulo, cor) in enumerate(zip(metricas, titulos, cores)):
        ax = axes[idx]
        df[metrica].sort_values().plot(kind='barh', ax=ax, color=cor, alpha=0.7)
        ax.set_xlabel(titulo, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def analise_feature_importance(modelo, feature_names, top_n=10, salvar=None):
    """
    Analisa e plota feature importance de modelos baseados em árvore.
    
    Parâmetros:
    -----------
    modelo : modelo treinado
        Modelo com atributo feature_importances_
    feature_names : list
        Nomes das features
    top_n : int
        Número de features a exibir
    salvar : str, opcional
        Caminho para salvar o gráfico
    """
    if not hasattr(modelo, 'feature_importances_'):
        print("⚠️  Modelo não suporta feature_importances_")
        return
    
    importances = modelo.feature_importances_
    
    df_imp = pd.DataFrame({
        'Feature': feature_names,
        'Importância': importances
    }).sort_values('Importância', ascending=False).head(top_n)
    
    plt.figure(figsize=(12, 8))
    plt.barh(df_imp['Feature'], df_imp['Importância'], color='#3498db')
    plt.xlabel('Importância', fontsize=12, fontweight='bold')
    plt.title(f'Top {top_n} Features Mais Importantes', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    if salvar:
        plt.savefig(salvar, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return df_imp


def calcular_roi_retencao(VP, FP, FN, VN, ltv=2000, custo_retencao=300, taxa_sucesso=0.6):
    """
    Calcula o ROI de uma estratégia de retenção baseada no modelo.
    
    Parâmetros:
    -----------
    VP, FP, FN, VN : int
        Valores da matriz de confusão
    ltv : float
        Lifetime Value médio por cliente (R$)
    custo_retencao : float
        Custo médio de campanha de retenção (R$)
    taxa_sucesso : float
        Taxa de sucesso das campanhas (0-1)
    
    Retorna:
    --------
    dict com análise financeira
    """
    total_churns = VP + FN
    churns_identificados = VP
    churns_perdidos = FN
    falsos_alarmes = FP
    
    clientes_salvos = int(churns_identificados * taxa_sucesso)
    receita_retida = clientes_salvos * ltv
    custo_campanhas = (churns_identificados + falsos_alarmes) * custo_retencao
    roi = receita_retida - custo_campanhas
    
    resultado = {
        'total_churns_reais': total_churns,
        'churns_identificados': churns_identificados,
        'taxa_identificacao': churns_identificados / total_churns,
        'churns_perdidos': churns_perdidos,
        'falsos_alarmes': falsos_alarmes,
        'clientes_salvos': clientes_salvos,
        'receita_retida': receita_retida,
        'custo_campanhas': custo_campanhas,
        'roi': roi,
        'roi_percentual': (roi / custo_campanhas) * 100 if custo_campanhas > 0 else 0
    }
    
    print(f"{'='*60}")
    print("ANÁLISE DE ROI - ESTRATÉGIA DE RETENÇÃO")
    print(f"{'='*60}")
    print(f"\n📊 Cenário:")
    print(f"   Total de churns reais: {total_churns}")
    print(f"   Churns identificados: {churns_identificados} ({resultado['taxa_identificacao']:.1%})")
    print(f"   Churns perdidos: {churns_perdidos}")
    print(f"   Falsos alarmes: {falsos_alarmes}")
    
    print(f"\n💰 Análise Financeira:")
    print(f"   LTV médio: R$ {ltv:,.2f}")
    print(f"   Custo de retenção: R$ {custo_retencao:,.2f}")
    print(f"   Taxa de sucesso: {taxa_sucesso:.0%}")
    print(f"\n   Clientes salvos: {clientes_salvos}")
    print(f"   Receita retida: R$ {receita_retida:,.2f}")
    print(f"   Custo total: R$ {custo_campanhas:,.2f}")
    print(f"   ROI: R$ {roi:,.2f} ({resultado['roi_percentual']:.1f}%)")
    
    if roi > 0:
        print(f"\n✅ Estratégia viável! ROI positivo.")
    else:
        print(f"\n⚠️  ROI negativo. Revisar estratégia.")
    
    print(f"{'='*60}\n")
    
    return resultado


def salvar_modelo_completo(modelo, feature_columns, scaler=None, 
                           caminho_modelo='modelo_final.pkl',
                           caminho_features='feature_columns.pkl',
                           caminho_scaler='scaler.pkl'):
    """
    Salva modelo e artefatos necessários para deploy.
    
    Parâmetros:
    -----------
    modelo : modelo treinado
    feature_columns : list
        Lista de nomes das features
    scaler : objeto scaler, opcional
        Normalizador (se usado)
    caminho_* : str
        Caminhos para salvar os arquivos
    """
    joblib.dump(modelo, caminho_modelo)
    print(f"✅ Modelo salvo: {caminho_modelo}")
    
    joblib.dump(feature_columns, caminho_features)
    print(f"✅ Features salvas: {caminho_features}")
    
    if scaler is not None:
        joblib.dump(scaler, caminho_scaler)
        print(f"✅ Scaler salvo: {caminho_scaler}")
    
    print("\n📦 Deploy pronto!")


def carregar_modelo_completo(caminho_modelo='modelo_final.pkl',
                             caminho_features='feature_columns.pkl',
                             caminho_scaler='scaler.pkl'):
    """
    Carrega modelo e artefatos para uso.
    
    Retorna:
    --------
    tuple: (modelo, feature_columns, scaler)
    """
    modelo = joblib.load(caminho_modelo)
    feature_columns = joblib.load(caminho_features)
    
    try:
        scaler = joblib.load(caminho_scaler)
    except:
        scaler = None
    
    print("✅ Modelo carregado e pronto para uso!")
    
    return modelo, feature_columns, scaler


# Função de exemplo de uso
if __name__ == "__main__":
    print("="*60)
    print("MÓDULO DE FUNÇÕES AUXILIARES")
    print("="*60)
    print("\nFunções disponíveis:")
    print("  • carregar_e_limpar_dados()")
    print("  • preparar_features()")
    print("  • plotar_matriz_confusao()")
    print("  • calcular_metricas_detalhadas()")
    print("  • comparar_modelos()")
    print("  • analise_feature_importance()")
    print("  • calcular_roi_retencao()")
    print("  • salvar_modelo_completo()")
    print("  • carregar_modelo_completo()")
    print("\nImporte com: from funcoes_auxiliares import *")
    print("="*60)
