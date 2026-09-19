<div align="center">

<img src="https://img.shields.io/badge/DIO-Explorer-7c3aed?style=for-the-badge&logo=bookstack&logoColor=white" alt="DIO Explorer"/>
<img src="https://img.shields.io/badge/IBM-Bob-0f62fe?style=for-the-badge&logo=ibm&logoColor=white" alt="IBM Bob"/>
<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/TypeScript-5.5-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
<img src="https://img.shields.io/badge/MCP-Server-10b981?style=for-the-badge&logo=node.js&logoColor=white" alt="MCP"/>

<br/><br/>

# 🎓 DIO Explorer

### Projeto Final — IBM Bob × Digital Innovation One

*Um assistente de aprendizado construído com IA, do início ao fim.*

<br/>

[![Testes](https://img.shields.io/badge/testes-36%2F36%20passed-22c55e?style=flat-square&logo=pytest)](dio_explorer/src/test_slash_commands.py)
[![Cobertura](https://img.shields.io/badge/coverage-100%25-22c55e?style=flat-square&logo=codecov)](dio_explorer/docs/test_results.txt)
[![Trilhas](https://img.shields.io/badge/trilhas-32%20no%20catálogo-7c3aed?style=flat-square)](dio_explorer/data/trilhas_dio.json)
[![Licença](https://img.shields.io/badge/licença-MIT-blue?style=flat-square)](LICENSE)

</div>

---

## 📖 Sobre o Projeto

O **DIO Explorer** é um assistente de aprendizado desenvolvido como **projeto final do programa IBM Bob × DIO**. Ele simula funcionalidades reais da plataforma [Digital Innovation One](https://www.dio.me/) — busca de trilhas, geração de desafios de código e emissão de certificados — tudo diretamente no chat do IBM Bob.

O diferencial: o projeto foi **construído com IA como copiloto**, demonstrando na prática como um desenvolvedor moderno usa ferramentas de IA generativa para ir da ideia à produção com qualidade de código, testes e documentação.

---

## ✨ Funcionalidades

| Comando | Descrição |
|---------|-----------|
| [`/trilha <tecnologia>`](.bob/commands/trilha.md) | Busca uma trilha no catálogo e exibe o plano de estudos completo |
| [`/desafio <tecnologia> <nivel>`](.bob/commands/desafio.md) | Gera um desafio de código aleatório com XP proporcional ao nível |
| [`/certificado <nome> <tecnologia>`](.bob/commands/certificado.md) | Emite um certificado fictício de conclusão de trilha |

> **Dica rápida:** `/desafio` sem argumentos sorteia tecnologia e nível automaticamente!

---

## 🚀 Demo Rápida

```
# Consultar uma trilha
/trilha Python

# Gerar um desafio
/desafio Java Intermediário

# Emitir um certificado
/certificado Seu Nome watsonx

# Surpresa! Bob sorteia pra você
/desafio
```

---

## 🏗️ Arquitetura

```
projeto_final_dio_ibm_bob/
│
├── 📁 .bob/
│   ├── mcp.json                   ← Registro do servidor MCP local
│   └── commands/                  ← Slash commands do projeto
│       ├── trilha.md              → /trilha <tecnologia>
│       ├── desafio.md             → /desafio <tecnologia> <nivel>
│       └── certificado.md         → /certificado <nome> <tecnologia>
│
├── 📁 dio_explorer/
│   ├── data/
│   │   └── trilhas_dio.json       ← 32 trilhas (fonte de verdade)
│   ├── src/
│   │   ├── trilhas_utils.py       ← Lógica de negócio (Python puro)
│   │   └── test_slash_commands.py ← 36 testes unitários
│   ├── mcp/
│   │   ├── src/index.ts           ← Servidor MCP (TypeScript)
│   │   └── build/index.js         ← Build compilado
│   └── docs/
│       └── test_results.txt       ← Relatório de cobertura
│
├── 📄 conftest.py                 ← Configuração pytest
├── 📄 .gitignore
└── 📄 .bobignore
```

O projeto tem **duas superfícies de exposição** para a mesma lógica:

| Superfície | Tecnologia | Como é acionada |
|------------|-----------|-----------------|
| **Slash Commands** | Markdown | Usuário digita `/trilha Python` no chat |
| **MCP Server** | TypeScript + Node.js | Bob chama as ferramentas automaticamente |

---

## 🗂️ Catálogo de Trilhas

O arquivo [`trilhas_dio.json`](dio_explorer/data/trilhas_dio.json) contém **32 trilhas** com schema completo:

<details>
<summary>Ver schema completo</summary>

```json
{
  "id": 1,
  "nome": "Fundamentos de Python para Iniciantes",
  "tecnologia": "Python",
  "nivel": "Básico",
  "numero_de_modulos": 6,
  "xp_total": 4200,
  "badges_disponiveis": ["Python Rookie", "Code Starter", "Logic Builder"],
  "promocoes": {
    "desconto": "30%",
    "validade": "2025-08-31",
    "cupom": "PYTHON30"
  },
  "vitalicio": true,
  "lives_ao_vivo": [
    { "titulo": "Introdução ao Python", "data": "2025-07-10", "horario": "19:00" }
  ]
}
```

</details>

| Nível | Trilhas | Exemplos |
|-------|---------|---------|
| 🟢 Básico | 8 | Python, Git, Lógica, Power BI, Figma... |
| 🟡 Intermediário | 14 | Java, React, Node, TypeScript, Flutter... |
| 🔴 Avançado | 10 | watsonx, ML, AWS, DevOps, Blockchain... |

---

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest dio_explorer/src/test_slash_commands.py -v

# Com relatório de cobertura
python -m pytest dio_explorer/src/test_slash_commands.py -v \
  --cov=dio_explorer.src.trilhas_utils \
  --cov-report=term-missing
```

**Resultado:**

```
36 passed in 0.21s  ·  Coverage: 100% (48/48 linhas)
```

| Suite | Testes | O que valida |
|-------|--------|-------------|
| `TestCarregarTrilhas` | 3 | Leitura do JSON, 32 trilhas |
| `TestBuscarTrilha` | 8 | Busca exata, parcial, case-insensitive, None |
| `TestFormatarPlanoEstudos` | 7 | Campos, badges, promoção presente/ausente |
| `TestGerarDesafio` | 9 | Dict, faixa de XP por nível, ValueError |
| `TestGerarCertificado` | 9 | Nome, data, regex do ID, badges, fluxo integrado |

---

## 🔌 MCP Server

O servidor MCP expõe as mesmas três funcionalidades como ferramentas nativas do Bob:

```bash
# Instalar dependências
cd dio_explorer/mcp
npm install

# Compilar TypeScript
npm run build

# Registrar no Bob (.bob/mcp.json já configurado)
```

Ferramentas disponíveis:

| Ferramenta | Parâmetros |
|------------|-----------|
| `trilha_buscar` | `tecnologia: string` |
| `desafio_gerar` | `tecnologia: string, nivel: "Básico"\|"Intermediário"\|"Avançado"` |
| `certificado_gerar` | `nome: string, tecnologia: string` |

> Veja o [README do servidor MCP](dio_explorer/mcp/README.md) para mais detalhes.

---

## 📦 Dependências

**Python**
```
pytest >= 9.0
pytest-cov >= 7.0
```

**Node.js / TypeScript**
```json
{
  "@modelcontextprotocol/sdk": "^1.0.0",
  "zod": "^3.23.0",
  "typescript": "^5.5.0"
}
```

---

## 🧠 O que este projeto demonstra

- **Slash Commands personalizados** no IBM Bob (escopo de projeto)
- **Servidor MCP** com TypeScript, zod e transporte stdio
- **Funções puras em Python** — testáveis sem dependências externas
- **Testes com injeção de dependência** — datas injetáveis, resultados determinísticos
- **100% de cobertura** de código sem over-engineering
- **Schema de dados unificado** — mesmo JSON consumido por Python e TypeScript

---

## 📚 Documentação

| Recurso | Link |
|---------|------|
| Slash Commands (guia completo) | [`.bob/commands/README.md`](.bob/commands/README.md) |
| MCP Server | [`dio_explorer/mcp/README.md`](dio_explorer/mcp/README.md) |
| Relatório de Testes | [`dio_explorer/docs/test_results.txt`](dio_explorer/docs/test_results.txt) |
| Documentação HTML | [`docs/documentacao.html`](docs/documentacao.html) |

---

## 👤 Autor

**Fabricio Eirim Castro**
Projeto Final — Programa IBM Bob × DIO

---

<div align="center">

*Construído com [IBM Bob](https://www.ibm.com/products/ai-assistant) · [Digital Innovation One](https://www.dio.me/)*

</div>
