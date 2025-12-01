# 📊 Projeto N3 - Predição de Churn de Clientes Telco

## 🎯 Sobre o Projeto

Este projeto apresenta uma solução completa de **Machine Learning para predição de Churn** (cancelamento de serviços) em uma empresa de telecomunicações. O objetivo é identificar clientes com alta probabilidade de cancelar seus serviços, permitindo ações preventivas de retenção.

### Problema de Negócio

> **"Quais fatores têm maior impacto na decisão de um cliente cancelar o serviço de telecomunicações?"**

O setor de telecomunicações é altamente competitivo, e a retenção de clientes é fundamental:
- Conquistar um novo cliente custa **5 a 25 vezes mais** do que manter um existente
- O **churn** impacta diretamente a receita recorrente da empresa
- Identificar clientes em risco permite **ações proativas de retenção**

---

## 📁 Estrutura do Repositório

```
📦 CienciaDeDadosN3/
├── 📄 README.md                    # Documentação do projeto
├── 📄 requirements.txt             # Dependências Python
├── 📄 modelo_final.pkl             # Modelo treinado e salvo
├── 📁 notebooks/
│   └── 01_projeto_telco_churn.ipynb  # Notebook completo do projeto
├── 📁 data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Dataset
├── 📁 scripts/
│   └── deploy_model.py             # Script de deploy do modelo
├── 📁 datasets/                    # Dataset original (backup)
└── 📁 atividades/                  # Atividades de referência
```

---

## 📊 Resultados Obtidos

### Modelos Treinados

| Modelo | Accuracy | Precision | Recall |
|--------|----------|-----------|--------|
| Decision Tree | ~78% | ~65% | ~50% |
| Random Forest | ~80% | ~68% | ~48% |
| **Logistic Regression** | ~80% | ~66% | ~55% |

### Modelo Escolhido: Logistic Regression

Para o problema de **churn**, priorizamos o **Recall** porque:
- ❌ **Falso Negativo** (não prever churn de quem vai sair): Perda definitiva do cliente
- ✅ **Falso Positivo** (prever churn de quem ia ficar): Custo menor, cliente ainda retido

A Logistic Regression apresentou o melhor equilíbrio entre as métricas, com maior Recall.

---

## 🚀 Como Executar Este Projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/pedrohdcosta/CienciaDeDadosN3.git
cd CienciaDeDadosN3

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Executando o Notebook

```bash
# Inicie o Jupyter Notebook
jupyter notebook notebooks/01_projeto_telco_churn.ipynb
```

### Usando o Script de Deploy

```bash
# Execute o script de demonstração
cd scripts
python deploy_model.py
```

---

## 📈 Pipeline de Dados

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  INGESTÃO   │ => │   LIMPEZA   │ => │     EDA     │ => │ PREPARAÇÃO  │
│  CSV Load   │    │  Transform  │    │  Análise    │    │  Encoding   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

1. **Ingestão**: Carregamento do CSV do Telco Customer Churn
2. **Limpeza**: Conversão de TotalCharges para numérico, remoção de valores ausentes
3. **EDA**: Análise de distribuições, correlações e visualizações
4. **Preparação**: One-Hot Encoding e divisão treino/teste (80/20)

---

## 📋 Dataset

- **Nome**: Telco Customer Churn
- **Fonte**: IBM Sample Data Sets / Kaggle
- **Registros**: 7.043 clientes
- **Colunas**: 21 variáveis

### Variáveis Principais

| Tipo | Variáveis |
|------|-----------|
| **Demográficas** | gender, SeniorCitizen, Partner, Dependents |
| **Serviços** | PhoneService, InternetService, OnlineSecurity, TechSupport |
| **Conta** | Contract, PaperlessBilling, PaymentMethod |
| **Métricas** | tenure, MonthlyCharges, TotalCharges |
| **Target** | Churn (Yes/No) |

---

## 📌 Estrutura da Avaliação N3

| Parte | Descrição | Pontuação |
|-------|-----------|-----------|
| **Parte 1** | Problema de Negócio | 1,0 ponto |
| **Parte 2** | Pipeline e Arquitetura | 1,0 ponto |
| **Parte 3** | Modelagem e Avaliação | 6,0 pontos |
| **Parte 4** | Deploy do Modelo | 2,0 pontos |
| **TOTAL** | | **10,0 pontos** |

---

## 👥 Equipe

- Pedro Henrique Costa (@pedrohdcosta)

---

## 📚 Referências

- **Dataset**: [Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Documentação Scikit-learn**: https://scikit-learn.org/
- **Pandas Documentation**: https://pandas.pydata.org/
- **Seaborn Documentation**: https://seaborn.pydata.org/

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte da avaliação N3 de Ciência de Dados.