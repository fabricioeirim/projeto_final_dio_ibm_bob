# 📖 Documentação — Slash Commands DIO Explorer

> Comandos personalizados para o projeto **DIO Explorer** (`C:\Users\fabricio\.bob\projeto_final_dio_ibm_bob`).
> Ficam armazenados em `.bob/commands/` e são **exclusivos deste projeto**.

---

## 📋 Índice

- [Como funcionam os slash commands](#como-funcionam-os-slash-commands)
- [/trilha](#trilha)
- [/desafio](#desafio)
- [/certificado](#certificado)
- [Trilhas disponíveis](#trilhas-disponíveis)
- [Estrutura de arquivos](#estrutura-de-arquivos)

---

## Como funcionam os slash commands

Slash commands personalizados são arquivos `.md` armazenados em `.bob/commands/` (escopo de projeto) ou `~/.bob/commands/` (escopo global).

- O **nome do arquivo** define o comando (ex: `trilha.md` → `/trilha`)
- O **frontmatter** declara metadados como `description` e `argument-hint`
- Os **argumentos** digitados após o comando são mapeados para `$1`, `$2`, etc.
- Comandos de projeto **sobrescrevem** comandos globais de mesmo nome
- O Bob injeta o conteúdo do arquivo como prompt e executa a tarefa

---

## /trilha

**Arquivo:** `.bob/commands/trilha.md`
**Invocação:** `/trilha <tecnologia>`

### Descrição

Localiza uma trilha de aprendizado no catálogo do DIO Explorer (`dio_explorer/data/trilhas_dio.json`) com base na tecnologia informada e retorna um **plano de estudos completo e formatado**.

A busca é **parcial e case-insensitive** — você não precisa digitar o nome exato.

### Sintaxe

```
/trilha <tecnologia>
```

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `$1` — tecnologia | string | ✅ Sim | Nome ou parte da tecnologia desejada |

### Exemplos de uso

```
/trilha Python
/trilha java
/trilha react
/trilha watsonx
/trilha docker
```

### O que é retornado

O plano de estudos inclui:

| Seção | Conteúdo |
|-------|----------|
| **Cabeçalho** | Nome da trilha, tecnologia, nível, módulos, XP e acesso vitalício |
| **Módulos** | Lista numerada com títulos e descrições gerados contextualmente |
| **Badges** | Todas as badges disponíveis para conquista |
| **Lives ao Vivo** | Tabela com título, data (DD/MM/AAAA) e horário |
| **Promoção** | Desconto, validade e cupom (se houver) |

### Comportamento de erro

Se nenhuma trilha for encontrada para a tecnologia informada, o Bob responderá de forma amigável e **listará todas as tecnologias disponíveis** no catálogo.

---

## /desafio

**Arquivo:** `.bob/commands/desafio.md`
**Invocação:** `/desafio <tecnologia> <nivel>`

### Descrição

Gera um **desafio de código aleatório e criativo** baseado na tecnologia e nível de dificuldade escolhidos. Se nenhum argumento for informado, sorteia automaticamente uma tecnologia e nível do catálogo.

### Sintaxe

```
/desafio <tecnologia> <nivel>
```

| Parâmetro | Tipo | Obrigatório | Valores aceitos |
|-----------|------|-------------|-----------------|
| `$1` — tecnologia | string | ⚠️ Opcional | Qualquer tecnologia do catálogo |
| `$2` — nivel | string | ⚠️ Opcional | `Básico`, `Intermediário`, `Avançado` |

> **Dica:** Se omitir os argumentos, o Bob sorteia a tecnologia e nível automaticamente e informa o que foi sorteado.

### Exemplos de uso

```
/desafio Python Básico
/desafio Java Intermediário
/desafio React Avançado
/desafio
```

### O que é retornado

O desafio gerado inclui:

| Campo | Descrição |
|-------|-----------|
| **Título** | Nome criativo e curto para o desafio |
| **Descrição** | Enunciado claro (3–5 linhas) com entrada e saída esperadas |
| **Requisitos** | Lista de requisitos técnicos a cumprir |
| **Exemplo** | Bloco de código com exemplo de entrada e saída |
| **Critérios de avaliação** | Correção, legibilidade, boas práticas e critério bônus por nível |
| **Tempo sugerido** | Estimativa de tempo para resolução |
| **XP ao completar** | Proporcional ao nível (Básico: 200–500 | Intermediário: 500–1000 | Avançado: 1000–2000) |

### Tabela de XP por nível

| Nível | XP Mínimo | XP Máximo |
|-------|-----------|-----------|
| Básico | 200 XP | 500 XP |
| Intermediário | 500 XP | 1.000 XP |
| Avançado | 1.000 XP | 2.000 XP |

> 💬 Após resolver, compartilhe sua solução no chat para receber feedback do Bob!

---

## /certificado

**Arquivo:** `.bob/commands/certificado.md`
**Invocação:** `/certificado <seu-nome> <tecnologia>`

### Descrição

Gera um **certificado fictício em Markdown** para o usuário que concluiu uma trilha. O certificado inclui dados reais da trilha extraídos do catálogo, data atual de emissão e um ID único gerado automaticamente.

> ⚠️ Este é um certificado fictício gerado para fins educacionais e de demonstração no contexto do projeto DIO Explorer.

### Sintaxe

```
/certificado <seu-nome> <tecnologia>
```

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `$1` — nome | string | ✅ Sim | Nome completo do usuário (pode conter espaços) |
| `$2` — tecnologia | string | ✅ Sim | Tecnologia da trilha a certificar |

### Exemplos de uso

```
/certificado Fabricio Eirim Castro Python
/certificado Ana Paula Java
/certificado Carlos React
/certificado Maria Souza watsonx
```

### O que é retornado

O certificado contém:

| Campo | Descrição |
|-------|-----------|
| **Nome do usuário** | Destacado em destaque central |
| **Nome da trilha** | Nome completo conforme o catálogo |
| **Tecnologia** | Tecnologia da trilha |
| **Nível** | Nível de dificuldade |
| **Módulos concluídos** | Total de módulos da trilha |
| **XP conquistado** | Total de XP da trilha |
| **Data de emissão** | Data atual formatada (DD/MM/AAAA) |
| **ID do certificado** | Formato: `DIO-{id}-{ano}-{6 dígitos aleatórios}` |
| **Badges conquistadas** | Lista completa de badges da trilha |

### Formato do ID do Certificado

```
DIO-{id_da_trilha}-{ano_atual}-{número_aleatório_6_dígitos}

Exemplos:
  DIO-001-2025-847362
  DIO-010-2025-293847
```

---

## Trilhas disponíveis

Lista completa das **32 trilhas** disponíveis no catálogo (`dio_explorer/data/trilhas_dio.json`):

| ID | Nome da Trilha | Tecnologia (use no comando) | Nível | Módulos | XP |
|----|---------------|----------------------------|-------|---------|-----|
| 1 | Fundamentos de Python para Iniciantes | `Python` | Básico | 6 | 4.200 |
| 2 | Desenvolvedor Java Full Stack | `Java` | Intermediário | 12 | 11.500 |
| 3 | Trilha de Machine Learning com Python | `Machine Learning` | Avançado | 15 | 18.000 |
| 4 | Formação React Developer | `React` | Intermediário | 10 | 9.800 |
| 5 | Cloud Native com AWS | `AWS` | Avançado | 14 | 16.500 |
| 6 | Banco de Dados SQL e NoSQL | `SQL` ou `MongoDB` | Básico | 8 | 5.600 |
| 7 | Desenvolvimento Android com Kotlin | `Kotlin` | Intermediário | 11 | 10.200 |
| 8 | DevOps e CI/CD na Prática | `Docker` ou `Kubernetes` | Avançado | 13 | 15.000 |
| 9 | Frontend com Vue.js 3 | `Vue` | Intermediário | 9 | 8.700 |
| 10 | IA Generativa com IBM watsonx | `watsonx` | Avançado | 16 | 20.000 |
| 11 | TypeScript do Zero ao Avançado | `TypeScript` | Intermediário | 8 | 7.800 |
| 12 | Formação Data Engineering | `Spark` ou `Kafka` | Avançado | 14 | 17.500 |
| 13 | Desenvolvimento iOS com Swift | `Swift` | Intermediário | 10 | 9.500 |
| 14 | Cibersegurança e Ethical Hacking | `Pentest` ou `Segurança` | Avançado | 12 | 14.000 |
| 15 | Lógica de Programação do Zero | `Lógica` | Básico | 5 | 3.000 |
| 16 | Node.js e APIs RESTful | `Node` | Intermediário | 9 | 8.400 |
| 17 | Flutter e Dart para Apps Multiplataforma | `Flutter` | Intermediário | 11 | 10.500 |
| 18 | Análise de Dados com Power BI | `Power BI` | Básico | 7 | 5.000 |
| 19 | Rust: Programação de Sistemas | `Rust` | Avançado | 13 | 16.000 |
| 20 | Formação Angular Developer | `Angular` | Intermediário | 10 | 9.200 |
| 21 | Blockchain e Web3 para Desenvolvedores | `Solidity` ou `Blockchain` | Avançado | 12 | 14.500 |
| 22 | Go Lang: Backend de Alta Performance | `Go` ou `Golang` | Intermediário | 9 | 8.900 |
| 23 | Introdução à Computação em Nuvem | `Azure` ou `GCP` | Básico | 6 | 4.500 |
| 24 | C# e .NET para Desenvolvimento Web | `C#` ou `.NET` | Intermediário | 11 | 10.800 |
| 25 | UX/UI Design com Figma | `Figma` | Básico | 7 | 4.800 |
| 26 | PHP Moderno com Laravel | `PHP` ou `Laravel` | Intermediário | 10 | 9.000 |
| 27 | Formação Game Development com Unity | `Unity` | Intermediário | 12 | 11.000 |
| 28 | Microsserviços com Spring Boot e Docker | `Spring Boot` | Avançado | 14 | 16.800 |
| 29 | Fundamentos de Git e GitHub | `Git` | Básico | 4 | 2.500 |
| 30 | Next.js e SSR com React | `Next.js` | Avançado | 11 | 12.500 |
| 31 | Terraform e Infraestrutura como Código | `Terraform` | Avançado | 10 | 13.000 |
| 32 | Introdução à Robótica com Arduino | `Arduino` | Básico | 6 | 3.800 |

---

## Estrutura de arquivos

```
C:\Users\fabricio\.bob\projeto_final_dio_ibm_bob\
│
├── .bob/
│   └── commands/                  ← Slash commands locais do projeto
│       ├── README.md              ← Esta documentação
│       ├── trilha.md              → /trilha <tecnologia>
│       ├── desafio.md             → /desafio <tecnologia> <nivel>
│       └── certificado.md         → /certificado <nome> <tecnologia>
│
└── dio_explorer/
    └── data/
        └── trilhas_dio.json       ← Fonte de dados (32 trilhas)
```

---

*Projeto Final DIO × IBM Bob — Slash Commands v1.0*
