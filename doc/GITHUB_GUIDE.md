# 🌐 Guia Rápido: Como Subir no GitHub

## ⚡ OPÇÃO MAIS FÁCIL - Interface Web

### Passo 1: Criar Repositório

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name:** `churn-telecom-project`
   - **Description:** "Projeto completo de previsão de churn em telecomunicações - Trabalho Final de Ciência de Dados"
   - **Public** ✅ (para o professor avaliar)
   - **NÃO** marque "Add a README file"
3. Clique em **"Create repository"**

### Passo 2: Upload dos Arquivos

1. No repositório recém-criado, clique em **"uploading an existing file"**

2. **IMPORTANTE:** Você precisa fazer upload da seguinte estrutura:

```
Arquivos na raiz (arraste todos juntos):
✓ README.md
✓ INSTRUCOES.md
✓ RESUMO_EXECUTIVO.md
✓ requirements.txt
```

3. Depois, crie as pastas:
   - Clique em **"Add file" > "Create new file"**
   - Digite: `notebooks/placeholder.txt`
   - Isso cria a pasta `notebooks/`
   - Commit e depois faça upload dos notebooks nessa pasta

4. Repita para a pasta `scripts/`:
   - `scripts/funcoes_auxiliares.py`

### Passo 3: Verificar

✅ Seu repositório deve ter:
```
churn-telecom-project/
├── README.md
├── INSTRUCOES.md
├── RESUMO_EXECUTIVO.md
├── requirements.txt
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modelagem_comparativa.ipynb
│   └── 03_deploy_exemplo.ipynb
└── scripts/
    └── funcoes_auxiliares.py
```

### Passo 4: Copiar Link

Copie a URL completa do seu repositório:
```
https://github.com/SEU-USUARIO/churn-telecom-project
```

---

## 🖥️ OPÇÃO 2 - Git via Terminal (Avançado)

### Se você já tem Git instalado:

```bash
# 1. Navegue até a pasta do projeto
cd /caminho/para/seu/projeto

# 2. Inicialize Git
git init

# 3. Adicione todos os arquivos
git add .

# 4. Faça o primeiro commit
git commit -m "Projeto completo de previsão de churn"

# 5. Adicione o repositório remoto
# Substitua SEU-USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU-USUARIO/churn-telecom-project.git

# 6. Renomeie branch para main
git branch -M main

# 7. Faça o push
git push -u origin main
```

**Se pedir usuário e senha:**
- **Username:** seu username do GitHub
- **Password:** você precisa usar um **Personal Access Token**
  - Vá em: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Dê permissões: `repo` (full control)
  - Copie o token e use como senha

---

## 🔍 CHECKLIST FINAL

Antes de enviar o link, verifique no GitHub:

- [ ] README.md está renderizado e formatado corretamente
- [ ] Todos os 3 notebooks estão visíveis
- [ ] Notebooks têm outputs (gráficos, tabelas) visíveis
- [ ] Estrutura de pastas está correta
- [ ] Não faltam arquivos importantes
- [ ] O link funciona quando você copia/cola

---

## 📤 ENTREGAR

### Onde enviar:
**MS Teams** (conforme instrução do professor)

### O que enviar:
```
Link do Repositório GitHub:
https://github.com/SEU-USUARIO/churn-telecom-project

Integrantes:
- Pedro Dias
- Gustavo Rodrigues
```

### Prazo:
⏰ **01 de dezembro de 2025, 23h59**

---

## 🆘 PROBLEMAS COMUNS

### "Não consigo fazer upload de .ipynb"
- **Solução:** Certifique-se de que o arquivo não está corrompido
- Tente abrir no Jupyter primeiro
- Se necessário, salve novamente

### "README não está formatado"
- **Causa:** Arquivo não está como .md
- **Solução:** Renomeie para README.md (não .txt)

### "Repositório vazio no GitHub"
- **Causa:** Arquivos não foram commitados
- **Solução:** Refresque a página ou refaça o upload

### "Git pede senha mas não aceita"
- **Causa:** GitHub não aceita mais senha normal
- **Solução:** Use Personal Access Token (veja instruções acima)

---

## ✅ TESTE FINAL

Depois de subir tudo:

1. **Abra uma aba anônima** no navegador
2. Cole o link do seu repositório
3. Verifique se consegue ver tudo

Se você conseguir ver tudo na aba anônima, o professor também conseguirá! ✅

---

## 🎉 PRONTO!

Seu projeto está no ar e pronto para ser avaliado!

**Boa sorte! 🍀**
