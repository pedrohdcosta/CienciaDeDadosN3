# 📊 Trabalho Final - Ciência de Dados N3

## 📋 Informações Gerais

- **Modalidade**: Avaliação em dupla ou trio
- **Entrega**: Via MS Teams
- **Data Limite**: 01 de dezembro de 2025, até 23h59min
- ⚠️ **Penalidade**: 1,0 ponto de desconto a cada hora de atraso

---

## 🎯 Objetivo do Trabalho

Consolidar o aprendizado aplicando o **ciclo completo de um projeto de dados**, desde a concepção do problema até a "entrega" de um modelo funcional.

Este trabalho retoma o projeto original iniciado no começo do semestre (avaliação N1), onde cada grupo definiu um domínio de problema e escolheu um dataset. O foco desta avaliação será demonstrar a **construção de um modelo preditivo** (classificação ou regressão), justificando cada etapa do processo.

### 💡 Dica Importante
Compare os trabalhos da N1 com o trabalho guiado da N2. É possível que a pergunta de negócio original não seja adequada para Ciência de Dados e precise ser ajustada ou até completamente alterada.

---

## 📁 Estrutura do Repositório

O trabalho deve ser entregue como um **link para repositório no GitHub** com a seguinte estrutura:

```
📦 CienciaDeDadosN3/
├── 📄 README.md                # O "rosto" do projeto - explica problema, estrutura e execução
├── 📁 atividades/              # Conjunto das atividades anteriores
├── 📁 dataset/                 # Dataset(s) utilizado(s)
├── 📁 doc/                     # Documentos com explicação
├── 📁 notebooks/               # Jupyter Notebooks de exploração e modelagem
├── 📁 scripts/                 # Scripts de deploy ou funções auxiliares
├── 📁 test/                    # Repositorio com os arquivos de teste
    └── 📄 modelo_final.pkl     # Modelo treinado e salvo
└── 📄 requirements.txt         # Arquivo de dependências Python
```

---

## 📊 Estrutura do Trabalho e Critérios de Avaliação

### **Parte 1: A Fundação do Projeto - O Problema de Negócio** (1,0 ponto)

Contextualize o projeto contando a história que motivou seu trabalho.

#### 1.1. Apresente o Domínio do Problema
Descreva o cenário e contexto do problema escolhido. Por que ele é relevante?

**Exemplo**: *"Nosso projeto se insere no contexto do mercado imobiliário, onde a precificação de imóveis é um desafio complexo..."*

#### 1.2. Apresente a Pergunta de Negócio
Declare de forma clara e específica a pergunta que guiou toda a análise.

**Exemplo**: *"A pergunta central que buscamos responder foi: 'Quais características de um imóvel (como área, número de quartos e localização) têm o maior impacto em seu preço de venda?'"*

#### 1.3. Defina o Objetivo do Modelo
Explique o que o modelo preditivo se propõe a fazer.

**Exemplo**: *"O objetivo foi construir um modelo de regressão capaz de estimar o preço de um imóvel com base em suas características, fornecendo uma ferramenta de apoio para corretores e proprietários."*

---

### **Parte 2: A Jornada dos Dados - Pipeline e Arquitetura** (1,0 ponto)

Descreva o caminho completo que os dados percorreram. **Uso de fluxograma ou diagrama visual é fortemente recomendado.**

#### 2.1. Origem e Repositório de Dados

- **Fonte Original**: Identifique a origem dos dados (ex: API, Kaggle, dados abertos do governo)
- **Arquitetura de Armazenamento**: Descreva e justifique a escolha
  - Data Lake (dados brutos)
  - Data Warehouse (dados tratados)
  - Data Lakehouse

#### 2.2. Pipeline de Dados

Explique passo a passo o fluxo de processamento:

1. **Ingestão**: Como os dados foram coletados e armazenados?
2. **Limpeza e Transformação (ETL/ELT)**: 
   - Tratamento de valores ausentes
   - Padronização de formatos
   - Remoção de duplicatas
3. **Análise Exploratória (EDA)**: Como a EDA ajudou a entender os dados e selecionar variáveis?
4. **Preparação para Modelagem**:
   - Seleção de features
   - One-Hot Encoding / get_dummies
   - Divisão treino/teste

---

### **Parte 3: O Coração do Projeto - Modelagem e Avaliação Comparativa** (6,0 pontos)

Esta é a **parte central do trabalho**. Demonstre capacidade de treinar, comparar e avaliar criticamente diferentes modelos.

#### 3.1. Treinamento de Três Modelos

Escolha e treine **pelo menos 3 algoritmos diferentes**:

**Para Classificação:**
- Árvore de Decisão
- Regressão Logística
- Random Forest
- KNN
- SVM

**Para Regressão:**
- Regressão Linear
- Ridge
- Lasso
- Árvore de Decisão para Regressão

#### 3.2. Avaliação com Três Métricas

Escolha **pelo menos 3 métricas** de desempenho:

**Para Classificação:**
- Acurácia
- Precisão
- Recall
- F1-Score

**Para Regressão:**
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² (R-squared)

**⚠️ IMPORTANTE**: Explique cada métrica escolhida antes de apresentar os resultados.

**Exemplo**: *"Para nosso problema de fraude, o Recall é crucial, pois mede a capacidade do modelo de encontrar todas as fraudes reais, mesmo que isso gere alguns alarmes falsos..."*

#### 3.3. Análise Comparativa dos Resultados

- Apresente os resultados em **tabela comparativa**
- Discuta: Qual modelo obteve melhor performance geral?
- Houve modelo que se destacou em métrica específica?
- **Justifique**: Com base na análise e no objetivo de negócio, qual modelo você escolheria e por quê?

---

### **Parte 4: Tornando o Modelo Útil - Deploy** (2,0 pontos)

Demonstre que seu modelo pode ser reutilizado para fazer novas previsões.

#### 4.1. Salvando o Modelo Treinado

Mostre o código para salvar o modelo usando `pickle` ou `joblib`:

```python
import joblib
joblib.dump(meu_melhor_modelo, 'modelo_final.pkl')
```

#### 4.2. Carregando e Utilizando o Modelo

- Carregue o arquivo do modelo salvo
- Crie um exemplo de **novo dado** (entrada que o modelo nunca viu)
- Use o modelo para fazer uma previsão
- Apresente e explique o resultado

**Exemplo**: *"Carregamos nosso modelo de preços e, para um novo imóvel com estas características, ele previu um preço de R$ X."*

---

## 📌 Resumo da Avaliação

| Parte | Descrição | Pontuação |
|-------|-----------|-----------|
| **Parte 1** | Problema de Negócio | 1,0 ponto |
| **Parte 2** | Pipeline e Arquitetura | 1,0 ponto |
| **Parte 3** | Modelagem e Avaliação | 6,0 pontos |
| **Parte 4** | Deploy do Modelo | 2,0 pontos |
| **TOTAL** | | **10,0 pontos** |

---

## 🚀 Como Executar Este Projeto

### Instalação

```bash
# Clone o repositório
git clone https://github.com/pedrohdcosta/CienciaDeDadosN3.git
cd CienciaDeDadosN3

# Instale as dependências
pip install -r requirements.txt
```

### Executar os Notebooks

```bash
# Execute os notebooks de análise
jupyter notebook notebooks/
```

### 🌐 Executar a API Localmente

A API de predição de churn pode ser executada localmente através de endpoints REST.

```bash
# Iniciar a API
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

#### Documentação Interativa

Acesse a documentação automática da API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/health` | GET | Verifica status da API e se o modelo está carregado |
| `/predict` | POST | Predição de churn para um único cliente |
| `/predict/batch` | POST | Predição de churn para múltiplos clientes |

#### Exemplos de Uso

**Verificar Status da API:**
```bash
curl http://localhost:8000/health
```

**Predição para um Cliente:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure": 12,
    "MonthlyCharges": 75.00,
    "TotalCharges": 900.00,
    "Contract": "Month-to-month",
    "InternetService": "DSL",
    "PaymentMethod": "Electronic check",
    "OnlineSecurity": "No",
    "TechSupport": "No",
    "PaperlessBilling": "Yes",
    "SeniorCitizen": 0
  }'
```

**Resposta Esperada:**
```json
{
  "predicao": "No",
  "probabilidade_churn": 0.3521,
  "nivel_risco": "BAIXO",
  "acao_recomendada": "MANTER: Cliente estável, continuar comunicação regular e programa de fidelidade"
}
```

**Predição em Lote:**
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "clientes": [
      {
        "tenure": 2,
        "MonthlyCharges": 89.99,
        "TotalCharges": 179.98,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "PaymentMethod": "Electronic check",
        "OnlineSecurity": "No",
        "TechSupport": "No",
        "PaperlessBilling": "Yes",
        "SeniorCitizen": 0
      },
      {
        "tenure": 60,
        "MonthlyCharges": 55.00,
        "TotalCharges": 3300.00,
        "Contract": "Two year",
        "InternetService": "DSL",
        "PaymentMethod": "Credit card (automatic)",
        "OnlineSecurity": "Yes",
        "TechSupport": "Yes",
        "PaperlessBilling": "No",
        "SeniorCitizen": 1
      }
    ]
  }'
```

#### Campos de Entrada

| Campo | Tipo | Descrição | Valores Aceitos |
|-------|------|-----------|-----------------|
| `tenure` | int | Meses como cliente | 0-120 |
| `MonthlyCharges` | float | Valor mensal (R$) | ≥ 0 |
| `TotalCharges` | float | Total gasto (R$) | ≥ 0 |
| `Contract` | string | Tipo de contrato | "Month-to-month", "One year", "Two year" |
| `InternetService` | string | Serviço de internet | "DSL", "Fiber optic", "No" |
| `PaymentMethod` | string | Método de pagamento | "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)" |
| `OnlineSecurity` | string | Segurança online | "Yes", "No", "No internet service" |
| `TechSupport` | string | Suporte técnico | "Yes", "No", "No internet service" |
| `PaperlessBilling` | string | Fatura digital | "Yes", "No" |
| `SeniorCitizen` | int | É idoso | 0, 1 |

### Executar Testes

```bash
# Executar testes da API
python -m pytest test/test_api.py -v

# Testar modelo manualmente
python test/test_pkl_model.py
```

---

## 👥 Equipe

- Pedro Henrique Dias da Costa
- Gustavo Schinieder Rodrigues

---

## 📚 Referências

A documentação está localizada no repositorio CienciaDeDadosN3/doc
---
