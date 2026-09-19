#!/usr/bin/env node
/**
 * dio-explorer-mcp — MCP Server para o projeto DIO Explorer
 *
 * Expõe três ferramentas para acesso via MCP (stdio, HTTP SSE ou qualquer
 * transporte suportado pelo SDK):
 *
 *   • trilha_buscar     — /trilha <tecnologia>
 *   • desafio_gerar     — /desafio <tecnologia> <nivel>
 *   • certificado_gerar — /certificado <nome> <tecnologia>
 *
 * Os dados são lidos do arquivo JSON localizado em ../data/trilhas_dio.json
 * (relativo a este arquivo, dentro do monorepo).
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join, dirname } from "node:path";

// ---------------------------------------------------------------------------
// Tipagem local dos dados
// ---------------------------------------------------------------------------

interface Promocao {
  desconto: string;
  validade: string | null;
  cupom: string | null;
}

interface Live {
  titulo: string;
  data: string;
  horario: string;
}

interface Trilha {
  id: number;
  nome: string;
  tecnologia: string;
  nivel: string;
  numero_de_modulos: number;
  xp_total: number;
  badges_disponiveis: string[];
  promocoes: Promocao | null;
  vitalicio: boolean;
  lives_ao_vivo: Live[];
}

// ---------------------------------------------------------------------------
// Carregamento do catálogo de trilhas
// ---------------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const DATA_PATH = join(__dirname, "..", "..", "data", "trilhas_dio.json");

function carregarTrilhas(): Trilha[] {
  const raw = readFileSync(DATA_PATH, "utf-8");
  const dados = JSON.parse(raw) as { trilhas: Trilha[] };
  return dados.trilhas;
}

// ---------------------------------------------------------------------------
// Lógica de negócio — /trilha
// ---------------------------------------------------------------------------

function buscarTrilha(tecnologia: string, trilhas: Trilha[]): Trilha | null {
  const termo = tecnologia.trim().toLowerCase();
  if (!termo) return null;
  return trilhas.find((t) => t.tecnologia.toLowerCase().includes(termo)) ?? null;
}

function formatarPlanoEstudos(trilha: Trilha): string {
  const vitalicio = trilha.vitalicio ? "Sim" : "Não";
  const linhas: string[] = [
    `# 📚 Plano de Estudos — ${trilha.nome}`,
    `**🎯 Tecnologia:** ${trilha.tecnologia}`,
    `**📊 Nível:** ${trilha.nivel}`,
    `**🔢 Módulos:** ${trilha.numero_de_modulos}`,
    `**⭐ XP Total:** ${trilha.xp_total} XP`,
    `**♾️ Acesso Vitalício:** ${vitalicio}`,
    "",
    "## 🏅 Badges Disponíveis",
    ...trilha.badges_disponiveis.map((b) => `- 🥇 ${b}`),
    "",
    "## 🎁 Promoção",
  ];

  if (trilha.promocoes) {
    const p = trilha.promocoes;
    linhas.push(
      `Desconto: ${p.desconto} | Cupom: ${p.cupom ?? "—"} | Válido até: ${p.validade ?? "—"}`
    );
  } else {
    linhas.push("Nenhuma promoção ativa no momento.");
  }

  if (trilha.lives_ao_vivo.length > 0) {
    linhas.push("", "## 📡 Lives Ao Vivo");
    for (const live of trilha.lives_ao_vivo) {
      linhas.push(`- **${live.titulo}** — ${live.data} às ${live.horario}`);
    }
  }

  return linhas.join("\n");
}

// ---------------------------------------------------------------------------
// Lógica de negócio — /desafio
// ---------------------------------------------------------------------------

type Nivel = "Básico" | "Intermediário" | "Avançado";

const DESAFIOS: Record<Nivel, [string, string, string, string][]> = {
  Básico: [
    ["Calculadora Simples", "Implemente uma calculadora que realize as quatro operações básicas.", "2 + 3", "5"],
    ["Verificador de Par/Ímpar", "Dado um número inteiro, informe se é par ou ímpar.", "7", "Ímpar"],
    ["Contador de Vogais", "Conte quantas vogais há em uma string.", "abcde", "2"],
  ],
  Intermediário: [
    ["Anagrama", "Verifique se duas palavras são anagramas uma da outra.", "listen / silent", "True"],
    ["FizzBuzz", "Imprima números de 1 a N; múltiplos de 3 → Fizz, 5 → Buzz, ambos → FizzBuzz.", "15", "1 2 Fizz 4 Buzz ... FizzBuzz"],
    ["Pilha com Mínimo", "Implemente uma pilha que retorne o elemento mínimo em O(1).", "push(3),push(1),push(2),getMin()", "1"],
  ],
  Avançado: [
    ["LRU Cache", "Implemente um cache LRU com get e put em O(1).", "capacity=2, put(1,1), put(2,2), get(1)", "1"],
    ["Merge Sort", "Implemente o algoritmo Merge Sort sem usar funções nativas de sort.", "[5,2,4,6,1,3]", "[1,2,3,4,5,6]"],
    ["Grafo BFS", "Encontre o caminho mais curto entre dois nós usando BFS.", "A→B→C, A→C", "A→C (distância 1)"],
  ],
};

const XP_RANGE: Record<Nivel, [number, number]> = {
  Básico: [200, 500],
  Intermediário: [500, 1000],
  Avançado: [1000, 2000],
};

const NIVEIS_VALIDOS: Nivel[] = ["Básico", "Intermediário", "Avançado"];

function gerarDesafio(tecnologia: string, nivel: string): object {
  if (!NIVEIS_VALIDOS.includes(nivel as Nivel)) {
    throw new Error(`Nível inválido: '${nivel}'. Use: ${NIVEIS_VALIDOS.join(", ")}`);
  }
  const n = nivel as Nivel;
  const opcoes = DESAFIOS[n];
  const [titulo, descricao, entrada, saida_esperada] = opcoes[Math.floor(Math.random() * opcoes.length)];
  const [xpMin, xpMax] = XP_RANGE[n];
  const xp = Math.floor(Math.random() * (xpMax - xpMin + 1)) + xpMin;

  return { tecnologia, nivel, titulo, descricao, entrada, saida_esperada, xp };
}

// ---------------------------------------------------------------------------
// Lógica de negócio — /certificado
// ---------------------------------------------------------------------------

function gerarCertificado(nome: string, trilha: Trilha): string {
  const hoje = new Date();
  const dataEmissao = hoje.toLocaleDateString("pt-BR");
  const certId = `DIO-${String(trilha.id).padStart(3, "0")}-${hoje.getFullYear()}-${String(Math.floor(Math.random() * 900000) + 100000)}`;
  const badges = trilha.badges_disponiveis.map((b) => `🥇 ${b}`).join("\n");

  return [
    "# 🎓 CERTIFICADO DE CONCLUSÃO",
    "",
    "**Certificamos que**",
    "",
    `## ✨ ${nome} ✨`,
    "",
    "concluiu com êxito a trilha:",
    "",
    `### 📚 ${trilha.nome}`,
    "",
    "| Campo | Detalhe |",
    "|-------|---------|",
    `| 🎯 Tecnologia | ${trilha.tecnologia} |`,
    `| 📊 Nível | ${trilha.nivel} |`,
    `| 🔢 Módulos | ${trilha.numero_de_modulos} |`,
    `| ⭐ XP | ${trilha.xp_total} XP |`,
    `| 📅 Emissão | ${dataEmissao} |`,
    `| 🔖 ID | ${certId} |`,
    "",
    "### 🏅 Badges",
    "",
    badges,
    "",
    "*Certificado fictício gerado para fins educacionais.*",
  ].join("\n");
}

// ---------------------------------------------------------------------------
// Servidor MCP
// ---------------------------------------------------------------------------

const server = new McpServer({ name: "dio-explorer", version: "0.1.0" });

// ── Ferramenta 1: trilha_buscar ──────────────────────────────────────────────
server.tool(
  "trilha_buscar",
  "Busca uma trilha de estudos DIO pela tecnologia desejada e retorna o plano de estudos em Markdown.",
  {
    tecnologia: z.string().describe("Nome ou parte do nome da tecnologia (ex: Python, Java, React)"),
  },
  async ({ tecnologia }) => {
    try {
      const trilhas = carregarTrilhas();
      const trilha = buscarTrilha(tecnologia, trilhas);
      if (!trilha) {
        return {
          content: [{ type: "text", text: `Nenhuma trilha encontrada para a tecnologia: **${tecnologia}**.\nTente outro nome — ex: Python, Java, React, Node.` }],
          isError: false,
        };
      }
      return { content: [{ type: "text", text: formatarPlanoEstudos(trilha) }] };
    } catch (err) {
      return {
        content: [{ type: "text", text: `Erro ao buscar trilha: ${err instanceof Error ? err.message : String(err)}` }],
        isError: true,
      };
    }
  }
);

// ── Ferramenta 2: desafio_gerar ──────────────────────────────────────────────
server.tool(
  "desafio_gerar",
  "Gera um desafio de código aleatório para uma tecnologia e nível escolhidos.",
  {
    tecnologia: z.string().describe("Tecnologia do desafio (ex: Java, Python, JavaScript)"),
    nivel: z.enum(["Básico", "Intermediário", "Avançado"]).describe("Nível de dificuldade do desafio"),
  },
  async ({ tecnologia, nivel }) => {
    try {
      const desafio = gerarDesafio(tecnologia, nivel) as Record<string, unknown>;
      const texto = [
        `# 🏆 Desafio: ${desafio["titulo"]}`,
        "",
        `**🎯 Tecnologia:** ${desafio["tecnologia"]}`,
        `**📊 Nível:** ${desafio["nivel"]}`,
        `**⭐ XP ao concluir:** ${desafio["xp"]} XP`,
        "",
        "## 📋 Descrição",
        String(desafio["descricao"]),
        "",
        "## 📥 Entrada de Exemplo",
        `\`${desafio["entrada"]}\``,
        "",
        "## 📤 Saída Esperada",
        `\`${desafio["saida_esperada"]}\``,
      ].join("\n");
      return { content: [{ type: "text", text: texto }] };
    } catch (err) {
      return {
        content: [{ type: "text", text: `Erro ao gerar desafio: ${err instanceof Error ? err.message : String(err)}` }],
        isError: true,
      };
    }
  }
);

// ── Ferramenta 3: certificado_gerar ─────────────────────────────────────────
server.tool(
  "certificado_gerar",
  "Gera um certificado fictício de conclusão para um aluno em uma trilha DIO.",
  {
    nome: z.string().describe("Nome completo do aluno"),
    tecnologia: z.string().describe("Tecnologia da trilha concluída (ex: Java, Python)"),
  },
  async ({ nome, tecnologia }) => {
    try {
      const trilhas = carregarTrilhas();
      const trilha = buscarTrilha(tecnologia, trilhas);
      if (!trilha) {
        return {
          content: [{ type: "text", text: `Trilha não encontrada para: **${tecnologia}**. Verifique o nome da tecnologia.` }],
          isError: false,
        };
      }
      return { content: [{ type: "text", text: gerarCertificado(nome, trilha) }] };
    } catch (err) {
      return {
        content: [{ type: "text", text: `Erro ao gerar certificado: ${err instanceof Error ? err.message : String(err)}` }],
        isError: true,
      };
    }
  }
);

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("DIO Explorer MCP Server rodando via stdio");
}

main().catch((err) => {
  console.error("Erro fatal:", err);
  process.exit(1);
});
