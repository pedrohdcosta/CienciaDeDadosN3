# 📖 Instruções de Execução do Projeto

## 🎯 Objetivo

Este documento contém o **passo a passo completo** para executar o projeto de previsão de churn desde a instalação até a apresentação final.

---

## 📋 Checklist Rápido

- [ ] Python 3.8+ instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Notebooks executados em ordem
- [ ] Modelo treinado e salvo
- [ ] README.md revisado
- [ ] Repositório GitHub criado
- [ ] Projeto pronto para entrega!

---

## 🚀 Passo 1: Configuração do Ambiente

### 1.1 Verificar Python

```bash
python --version
# Deve mostrar: Python 3.8.x ou superior
```

Se não tiver Python instalado:
- **Windows:** https://www.python.org/downloads/
- **Mac:** `brew install python3`
- **Linux:** `sudo apt-get install python3`

### 1.2 Criar Ambiente Virtual (RECOMENDADO)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Mac/Linux)
source venv/bin/activate
```

**Por que usar ambiente virtual?**
- Isola dependências do projeto
- Evita conflitos com outros projetos
- Facilita reprodutibilidade

### 1.3 Instalar Dependências

```bash
pip install -r requirements.txt
```

**Tempo estimado:** 2-5 minutos

### 1.4 Verificar Instalação

```bash
python -c "import pandas, sklearn, matplotlib; print('✅ Tudo OK!')"
```

---

## 📊 Passo 2: Executar a Análise Exploratória (EDA)

### 2.1 Abrir Jupyter Notebook

```bash
jupyter notebook
```

Isso abrirá o navegador automaticamente.

### 2.2 Executar `notebooks/01_eda.ipynb`

1. Navegue até `notebooks/01_eda.ipynb`
2. Execute célula por célula (Shift + Enter)
3. Ou execute tudo: `Cell > Run All`

**O que você vai ver:**
- ✅ Carregamento e limpeza dos dados
- ✅ Estatísticas descritivas
- ✅ Análise de valores ausentes
- ✅ Distribuição do target (Churn)
- ✅ Análise de correlações
- ✅ Visualizações (gráficos)
- ✅ Seleção de features

**Tempo estimado:** 10-15 minutos

**⚠️  Atenção:**
- Não modifique as células de limpeza de dados
- Anote os insights principais para o relatório
- Salve o notebook após execução

---

## 🤖 Passo 3: Treinar e Comparar Modelos

### 3.1 Executar `notebooks/02_modelagem_comparativa.ipynb`

1. Abra o notebook
2. Execute célula por célula
3. Observe os resultados de cada modelo

**O que você vai ver:**
- ✅ Preparação dos dados (encoding, train/test split)
- ✅ Treinamento de 5 modelos diferentes
- ✅ Comparação de métricas (Acurácia, Precisão, Recall, F1)
- ✅ Matriz de confusão
- ✅ Feature importance
- ✅ Análise de ROI
- ✅ Salvamento do melhor modelo

**Tempo estimado:** 15-20 minutos

**📌 IMPORTANTE:**
Este notebook salva automaticamente:
- `modelo_final.pkl` (modelo treinado)
- `feature_columns.pkl` (nomes das features)
- `scaler.pkl` (se necessário)

**Não perca esses arquivos!** Eles são necessários para o deploy.

---

## 🚀 Passo 4: Testar o Deploy

### 4.1 Executar `notebooks/03_deploy_exemplo.ipynb`

1. Abra o notebook
2. Execute célula por célula
3. Teste com seus próprios exemplos

**O que você vai ver:**
- ✅ Carregamento do modelo salvo
- ✅ Função de predição reutilizável
- ✅ Exemplos de clientes (alto, médio e baixo risco)
- ✅ Análise em lote
- ✅ Simulação de intervenções
- ✅ Código para produção

**Tempo estimado:** 10 minutos

**💡 Dica:**
Modifique os exemplos de clientes para testar diferentes cenários!

---

## 📦 Passo 5: Organizar Arquivos para Entrega

### 5.1 Estrutura Final do Projeto

Seu projeto deve ter esta estrutura:

```
churn-telecom-project/
│
├── README.md                    # ⭐ Relatório principal
├── requirements.txt             # Dependências
│
├── notebooks/
│   ├── 01_eda.ipynb            # Análise exploratória
│   ├── 02_modelagem_comparativa.ipynb  # Modelagem
│   └── 03_deploy_exemplo.ipynb  # Deploy
│
├── scripts/
│   └── funcoes_auxiliares.py   # Funções úteis
│
├── data/
│   └── (opcional - dataset baixado automaticamente)
│
├── modelo_final.pkl            # ⭐ Modelo treinado
├── feature_columns.pkl         # Features usadas
└── scaler.pkl                  # (se aplicável)
```

### 5.2 Verificar Arquivos Essenciais

✅ Certifique-se de que você tem:
- [ ] README.md completo e revisado
- [ ] 3 notebooks executados (com outputs visíveis)
- [ ] modelo_final.pkl
- [ ] feature_columns.pkl
- [ ] requirements.txt

---

## 🌐 Passo 6: Criar Repositório no GitHub

### 6.1 Criar Repositório

1. Vá para https://github.com/new
2. Nome do repositório: `churn-telecom-project` (ou similar)
3. Descrição: "Projeto de previsão de churn em telecomunicações"
4. **Público** (para a avaliação)
5. **NÃO** inicialize com README (você já tem um)
6. Clique em "Create repository"

### 6.2 Subir Arquivos

**Opção A - Via Interface Web (Mais Fácil):**

1. No GitHub, clique em "uploading an existing file"
2. Arraste todos os arquivos do projeto
3. Commit: "Projeto completo de churn"
4. Clique em "Commit changes"

**Opção B - Via Git (Linha de Comando):**

```bash
# No diretório do projeto
git init
git add .
git commit -m "Projeto completo de churn"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/churn-telecom-project.git
git push -u origin main
```

### 6.3 Verificar no GitHub

✅ Acesse seu repositório e verifique:
- [ ] README.md está renderizado corretamente
- [ ] Notebooks estão visíveis com outputs
- [ ] Todos os arquivos foram enviados
- [ ] Links estão funcionando

---

## 📝 Passo 7: Preparar para Apresentação/Entrega

### 7.1 Revisar README.md

Certifique-se de que o README contém:
- [x] Problema de negócio claro
- [x] Pergunta de negócio específica
- [x] Pipeline de dados documentado
- [x] Comparação de modelos (tabela)
- [x] Melhor modelo justificado
- [x] Instruções de execução
- [x] Impacto de negócio (ROI)

### 7.2 Testar Reprodutibilidade

**Teste Final:**
1. Clone seu próprio repositório em uma nova pasta
2. Siga suas próprias instruções do README
3. Execute todos os notebooks
4. Verifique se tudo funciona

```bash
# Em uma pasta diferente
git clone https://github.com/SEU-USUARIO/churn-telecom-project.git
cd churn-telecom-project
pip install -r requirements.txt
jupyter notebook
```

### 7.3 Checklist de Entrega

✅ Antes de entregar, verifique:

**Parte 1: Problema de Negócio (1,0 ponto)**
- [ ] Domínio do problema descrito
- [ ] Pergunta de negócio clara
- [ ] Objetivo do modelo definido

**Parte 2: Pipeline e Arquitetura (1,0 ponto)**
- [ ] Origem dos dados especificada
- [ ] Arquitetura de dados justificada
- [ ] Pipeline completo documentado (fluxograma)
- [ ] EDA explicada

**Parte 3: Modelagem (6,0 pontos)**
- [ ] 3+ modelos treinados ✅ (temos 5!)
- [ ] 3+ métricas calculadas ✅ (temos 4!)
- [ ] Métricas explicadas
- [ ] Análise comparativa detalhada
- [ ] Melhor modelo justificado

**Parte 4: Deploy (2,0 pontos)**
- [ ] Modelo salvo (pickle/joblib)
- [ ] Código de carregamento
- [ ] Exemplo de predição com novo dado
- [ ] Resultado interpretado

**Extras:**
- [ ] Código bem comentado
- [ ] Gráficos profissionais
- [ ] Análise de impacto de negócio
- [ ] Próximos passos sugeridos

---

## 🎯 Passo 8: Entrega

### 8.1 Link do GitHub

Copie a URL do seu repositório:
```
https://github.com/SEU-USUARIO/churn-telecom-project
```

### 8.2 Onde Entregar

Envie o link via **MS Teams** conforme instruções do professor.

### 8.3 Prazo

⏰ **Data limite:** 01 de dezembro de 2025, 23h59min

⚠️ **Atenção:** Atraso = -1,0 ponto por hora!

---

## 🆘 Troubleshooting (Solução de Problemas)

### Problema: "ModuleNotFoundError"

```bash
# Solução: Reinstalar dependências
pip install -r requirements.txt
```

### Problema: "Dataset não carrega"

- **Causa:** Problema de conexão
- **Solução:** Os notebooks têm URLs alternativas automáticas
- Se persistir, baixe manualmente de: https://github.com/IBM/telco-customer-churn-on-icp4d

### Problema: "Jupyter não abre"

```bash
# Solução: Instalar novamente
pip install jupyter notebook
jupyter notebook
```

### Problema: "Git não funciona"

- **Windows:** Instale Git: https://git-scm.com/download/win
- **Mac:** `brew install git`
- **Linux:** `sudo apt-get install git`

### Problema: "Notebooks sem outputs"

- Execute célula por célula
- Ou: `Cell > Run All`
- Salve: `Ctrl + S` ou `Cmd + S`

---

## 💡 Dicas Finais

### Para um Projeto Excelente:

1. **README é o rosto do projeto**
   - Capriche na formatação
   - Use emojis com moderação
   - Inclua imagens/gráficos

2. **Notebooks devem contar uma história**
   - Adicione células markdown explicativas
   - Comente o código
   - Interprete os resultados

3. **Dados falam, insights vendem**
   - Não apenas mostre números
   - Explique o que eles significam
   - Conecte com o negócio

4. **Mostre que entendeu**
   - Não apenas copie/cole código
   - Adapte para o contexto
   - Adicione suas análises

### Diferencial para Nota Máxima:

- [ ] Visualizações profissionais e informativas
- [ ] Análise de impacto financeiro (ROI)
- [ ] Feature engineering criativo
- [ ] Código limpo e bem documentado
- [ ] Insights acionáveis para o negócio
- [ ] Próximos passos bem pensados

---

## 📞 Precisa de Ajuda?

Se tiver dúvidas durante a execução:

1. **Revise este guia** - A resposta provavelmente está aqui
2. **Consulte o README.md** - Documentação completa
3. **Google é seu amigo** - Erros comuns têm soluções online
4. **Stack Overflow** - Comunidade de desenvolvedores

---

## ✅ Conclusão

Seguindo este guia passo a passo, você terá um projeto completo e profissional de Ciência de Dados!

**Tempo total estimado:** 2-3 horas (incluindo revisões)

**Boa sorte na apresentação! 🚀**

---

**Última atualização:** Dezembro 2025
