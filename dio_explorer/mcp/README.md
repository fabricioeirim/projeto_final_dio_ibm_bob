# 🔌 DIO Explorer — MCP Server

Servidor **Model Context Protocol (MCP)** do projeto DIO Explorer.  
Expõe três ferramentas para uso nativo pelo IBM Bob via transporte **stdio**.

---

## Ferramentas

### `trilha_buscar`

Busca uma trilha de estudos pelo nome da tecnologia e retorna o plano de estudos em Markdown.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `tecnologia` | `string` | ✅ | Nome ou parte da tecnologia (ex: `Python`, `Java`, `react`) |

**Comportamento:** busca parcial e case-insensitive sobre o campo `tecnologia` do catálogo.  
Se não encontrar, retorna mensagem amigável.

---

### `desafio_gerar`

Gera um desafio de código aleatório para uma tecnologia e nível escolhidos.

| Parâmetro | Tipo | Obrigatório | Valores aceitos |
|-----------|------|-------------|-----------------|
| `tecnologia` | `string` | ✅ | Qualquer tecnologia |
| `nivel` | `enum` | ✅ | `Básico` · `Intermediário` · `Avançado` |

**XP gerado por nível:**

| Nível | Mínimo | Máximo |
|-------|--------|--------|
| Básico | 200 XP | 500 XP |
| Intermediário | 500 XP | 1.000 XP |
| Avançado | 1.000 XP | 2.000 XP |

---

### `certificado_gerar`

Gera um certificado fictício de conclusão para um aluno em uma trilha DIO.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `nome` | `string` | ✅ | Nome completo do aluno |
| `tecnologia` | `string` | ✅ | Tecnologia da trilha concluída |

**ID gerado:** `DIO-{id}-{ano}-{6 dígitos aleatórios}`

---

## Instalação e Build

```bash
# 1. Instalar dependências
npm install

# 2. Compilar TypeScript
npm run build
# Gera: build/index.js

# 3. Executar diretamente (opcional — para teste)
npm start
```

---

## Configuração no IBM Bob

O arquivo `.bob/mcp.json` na raiz do projeto já registra este servidor:

```json
{
  "mcpServers": {
    "dio-explorer": {
      "command": "node",
      "args": ["<caminho-absoluto>/dio_explorer/mcp/build/index.js"]
    }
  }
}
```

> Ajuste o caminho absoluto conforme o seu ambiente.

---

## Stack

| Tecnologia | Versão | Papel |
|-----------|--------|-------|
| `@modelcontextprotocol/sdk` | `^1.0.0` | Protocolo MCP (server + transport) |
| `zod` | `^3.23.0` | Validação de inputs das ferramentas |
| `typescript` | `^5.5.0` | Tipagem e compilação |
| `@types/node` | `^22.0.0` | Tipos Node.js |

---

## Estrutura

```
mcp/
├── src/
│   └── index.ts        ← Implementação completa (server + tools + lógica)
├── build/
│   └── index.js        ← Build compilado (não editar)
├── package.json
└── tsconfig.json
```

> A lógica de negócio (`buscarTrilha`, `gerarDesafio`, `gerarCertificado`) é
> uma reimplementação em TypeScript das funções Python de `trilhas_utils.py`,
> compartilhando o mesmo arquivo de dados `../data/trilhas_dio.json`.
