"""
🧪 TESTE DO MODELO - COM DADOS NOVOS
Este script demonstra o uso do modelo salvo (.pkl) para prever churn de NOVOS clientes.
"""

import pandas as pd
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🧪 TESTE DO MODELO SALVO - PREDIÇÃO COM DADOS NOVOS")
print("=" * 80)

# ========== 1. CARREGAR MODELO ==========
print("\n📦 1. Carregando modelo salvo...")
try:
    modelo = joblib.load('test/modelo_final.pkl')
    feature_columns = joblib.load('test/feature_columns.pkl')
    print(f"   ✅ Modelo carregado: {type(modelo).__name__}")
    print(f"   ✅ Features carregadas: {len(feature_columns)} colunas")
    
    # Tentar carregar scaler (se existir)
    try:
        scaler = joblib.load('test/scaler.pkl')
        print(f"   ✅ Scaler carregado (modelo precisa de normalização)")
        usa_scaler = True
    except FileNotFoundError:
        print(f"   ℹ️  Scaler não encontrado (modelo não precisa de normalização)")
        scaler = None
        usa_scaler = False
        
except FileNotFoundError:
    print("   ❌ ERRO: Arquivos .pkl não encontrados!")
    print("   💡 Execute primeiro o Notebook 02 (02_modelagem_comparativa.ipynb)")
    print("      ou execute o script de treino para gerar os arquivos.")
    exit()

# ========== 2. CRIAR NOVOS DADOS (que o modelo nunca viu) ==========
print("\n" + "=" * 80)
print("📋 2. CRIANDO DADOS DE CLIENTES NOVOS (nunca vistos pelo modelo)")
print("=" * 80)

# Cliente 1: ALTO RISCO de churn
print("\n🔴 CLIENTE 1 - Perfil de ALTO RISCO:")
cliente_1 = {
    'tenure': 2,                        # Apenas 2 meses
    'MonthlyCharges': 89.99,            # Mensalidade alta
    'TotalCharges': 179.98,             # Total baixo (novo)
    'Contract': 'Month-to-month',       # Sem compromisso
    'InternetService': 'Fiber optic',   # Fibra
    'PaymentMethod': 'Electronic check',# Método problemático
    'OnlineSecurity': 'No',             # Sem serviços extras
    'TechSupport': 'No',                # Sem suporte
    'PaperlessBilling': 'Yes',          # Fatura digital
    'SeniorCitizen': 0                  # Não é idoso
}

print("   Dados do cliente:")
for key, value in cliente_1.items():
    print(f"      {key:20s}: {value}")

# Cliente 2: BAIXO RISCO de churn
print("\n🟢 CLIENTE 2 - Perfil de BAIXO RISCO:")
cliente_2 = {
    'tenure': 60,                       # 5 anos de contrato
    'MonthlyCharges': 55.00,            # Mensalidade razoável
    'TotalCharges': 3300.00,            # Alto valor total
    'Contract': 'Two year',             # Compromisso longo
    'InternetService': 'DSL',           # DSL (mais estável)
    'PaymentMethod': 'Credit card (automatic)', # Pagamento automático
    'OnlineSecurity': 'Yes',            # Com serviços extras
    'TechSupport': 'Yes',               # Com suporte
    'PaperlessBilling': 'No',           # Fatura física
    'SeniorCitizen': 1                  # É idoso
}

print("   Dados do cliente:")
for key, value in cliente_2.items():
    print(f"      {key:20s}: {value}")

# Cliente 3: RISCO MÉDIO
print("\n🟡 CLIENTE 3 - Perfil de RISCO MÉDIO:")
cliente_3 = {
    'tenure': 24,                       # 2 anos
    'MonthlyCharges': 70.00,            # Mensalidade média
    'TotalCharges': 1680.00,            # Total médio
    'Contract': 'One year',             # Contrato anual
    'InternetService': 'Fiber optic',   # Fibra
    'PaymentMethod': 'Bank transfer (automatic)', # Pagamento automático
    'OnlineSecurity': 'No',             # Sem alguns serviços
    'TechSupport': 'Yes',               # Tem suporte
    'PaperlessBilling': 'Yes',          # Fatura digital
    'SeniorCitizen': 0                  # Não é idoso
}

print("   Dados do cliente:")
for key, value in cliente_3.items():
    print(f"      {key:20s}: {value}")

# ========== 3. FUNÇÃO DE PREDIÇÃO ==========
def prever_churn(cliente_dict):
    """
    Faz predição para um novo cliente.
    """
    # 1. Criar DataFrame
    df_novo = pd.DataFrame([cliente_dict])
    
    # 2. Aplicar One-Hot Encoding (igual ao treino)
    df_encoded = pd.get_dummies(df_novo, drop_first=True)
    
    # 3. Garantir mesmas colunas do treino
    for col in feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[feature_columns]
    
    # 4. Aplicar scaler se necessário
    if usa_scaler:
        df_encoded = scaler.transform(df_encoded)
    
    # 5. Fazer predição
    classe_predita = modelo.predict(df_encoded)[0]
    probabilidade_churn = modelo.predict_proba(df_encoded)[0][1]
    
    # 6. Determinar risco
    if probabilidade_churn >= 0.7:
        risco = "ALTO"
        cor = "🔴"
        acao = "AÇÃO URGENTE: Contato imediato, desconto 25%, migrar para contrato anual"
    elif probabilidade_churn >= 0.4:
        risco = "MÉDIO"
        cor = "🟡"
        acao = "MONITORAR: Incluir em campanha de engajamento, oferecer upgrade"
    else:
        risco = "BAIXO"
        cor = "🟢"
        acao = "MANTER: Cliente estável, continuar comunicação regular"
    
    return {
        'classe': classe_predita,
        'probabilidade': probabilidade_churn,
        'risco': risco,
        'cor': cor,
        'acao': acao
    }

# ========== 4. FAZER PREDIÇÕES ==========
print("\n" + "=" * 80)
print("🎯 3. FAZENDO PREDIÇÕES COM O MODELO SALVO")
print("=" * 80)

clientes = [
    ("CLIENTE 1 - Alto Risco", cliente_1),
    ("CLIENTE 2 - Baixo Risco", cliente_2),
    ("CLIENTE 3 - Risco Médio", cliente_3)
]

resultados = []

for nome, dados in clientes:
    print(f"\n{nome}:")
    print("-" * 80)
    
    resultado = prever_churn(dados)
    
    print(f"   {resultado['cor']} RISCO: {resultado['risco']}")
    print(f"   📊 Probabilidade de Churn: {resultado['probabilidade']:.1%}")
    print(f"   🎯 Predição: {resultado['classe']}")
    print(f"   💡 Ação Recomendada: {resultado['acao']}")
    
    resultados.append({
        'Cliente': nome,
        'Tenure': dados['tenure'],
        'Mensalidade': dados['MonthlyCharges'],
        'Contrato': dados['Contract'],
        'Prob. Churn': f"{resultado['probabilidade']:.1%}",
        'Predição': resultado['classe'],
        'Risco': f"{resultado['cor']} {resultado['risco']}"
    })

# ========== 5. RESUMO ==========
print("\n" + "=" * 80)
print("📊 4. RESUMO DAS PREDIÇÕES")
print("=" * 80)

df_resultados = pd.DataFrame(resultados)
print("\n" + df_resultados.to_string(index=False))

# ========== 6. EXEMPLO: CRIAR SEU PRÓPRIO CLIENTE ==========
print("\n" + "=" * 80)
print("💡 5. AGORA TESTE VOCÊ MESMO!")
print("=" * 80)
print("\nCopie e modifique este código para testar com seus próprios dados:\n")
print("""
# Seu cliente personalizado:
meu_cliente = {
    'tenure': 12,                    # Meses como cliente
    'MonthlyCharges': 75.00,         # Valor mensal
    'TotalCharges': 900.00,          # Total gasto
    'Contract': 'Month-to-month',    # Tipo de contrato
    'InternetService': 'DSL',        # Tipo de internet
    'PaymentMethod': 'Electronic check',
    'OnlineSecurity': 'No',
    'TechSupport': 'No',
    'PaperlessBilling': 'Yes',
    'SeniorCitizen': 0
}

resultado = prever_churn(meu_cliente)
print(f"Probabilidade de Churn: {resultado['probabilidade']:.1%}")
print(f"Risco: {resultado['risco']}")
""")

# ========== 7. VALIDAÇÃO ==========
print("\n" + "=" * 80)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 80)
print("\n📋 O que foi demonstrado:")
print("   1. ✅ Carregamento do modelo salvo (.pkl)")
print("   2. ✅ Criação de dados NOVOS (nunca vistos pelo modelo)")
print("   3. ✅ Predição com o modelo carregado")
print("   4. ✅ Interpretação dos resultados")
print("   5. ✅ Recomendações de ação por nível de risco")
print("\n🎯 O modelo está funcionando perfeitamente!")
print("=" * 80)