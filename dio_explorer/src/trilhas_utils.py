"""
trilhas_utils.py
----------------
Módulo utilitário que implementa as regras de negócio dos slash commands
/trilha, /desafio e /certificado do projeto DIO Explorer.

Todas as funções aqui são puras (sem I/O de rede) e testáveis unitariamente.
"""

import json
import os
import random
import re
from datetime import date
from typing import Optional

# ---------------------------------------------------------------------------
# Caminho padrão para o arquivo de dados
# ---------------------------------------------------------------------------
_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "trilhas_dio.json"
)


# ---------------------------------------------------------------------------
# Carregamento de dados
# ---------------------------------------------------------------------------

def carregar_trilhas(caminho: str = _DATA_FILE) -> list[dict]:
    """Lê trilhas_dio.json e retorna a lista de trilhas."""
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    return dados["trilhas"]


# ---------------------------------------------------------------------------
# /trilha  — busca de trilha por tecnologia
# ---------------------------------------------------------------------------

def buscar_trilha(tecnologia: str, trilhas: list[dict]) -> Optional[dict]:
    """
    Retorna a primeira trilha cujo campo 'tecnologia' contém a string
    informada (busca parcial, case-insensitive).
    Retorna None se não houver correspondência.
    """
    if not tecnologia or not tecnologia.strip():
        return None
    termo = tecnologia.strip().lower()
    for trilha in trilhas:
        if termo in trilha["tecnologia"].lower():
            return trilha
    return None


def formatar_plano_estudos(trilha: dict) -> str:
    """
    Recebe um dict de trilha e retorna o plano de estudos formatado
    em Markdown (versão simplificada para testes).
    """
    vitalicio = "Sim" if trilha.get("vitalicio") else "Não"
    linhas = [
        f"# 📚 Plano de Estudos — {trilha['nome']}",
        f"**🎯 Tecnologia:** {trilha['tecnologia']}",
        f"**📊 Nível:** {trilha['nivel']}",
        f"**🔢 Módulos:** {trilha['numero_de_modulos']}",
        f"**⭐ XP Total:** {trilha['xp_total']} XP",
        f"**♾️ Acesso Vitalício:** {vitalicio}",
    ]
    # Badges
    linhas.append("\n## 🏅 Badges Disponíveis")
    for badge in trilha.get("badges_disponiveis", []):
        linhas.append(f"- 🥇 {badge}")
    # Promoção
    linhas.append("\n## 🎁 Promoção")
    promo = trilha.get("promocoes")
    if promo:
        linhas.append(
            f"Desconto: {promo['desconto']} | Cupom: {promo.get('cupom','—')} | Válido até: {promo.get('validade','—')}"
        )
    else:
        linhas.append("Nenhuma promoção ativa no momento.")
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
# /desafio  — geração de desafio de código
# ---------------------------------------------------------------------------

_DESAFIOS = {
    "Básico": [
        ("Calculadora Simples", "Implemente uma calculadora que realize as quatro operações básicas.", "2 + 3", "5"),
        ("Verificador de Par/Ímpar", "Dada um número inteiro, informe se é par ou ímpar.", "7", "Ímpar"),
        ("Contador de Vogais", "Conte quantas vogais há em uma string.", "abcde", "2"),
    ],
    "Intermediário": [
        ("Anagrama", "Verifique se duas palavras são anagramas uma da outra.", "listen / silent", "True"),
        ("FizzBuzz", "Imprima números de 1 a N; múltiplos de 3 → Fizz, 5 → Buzz, ambos → FizzBuzz.", "15", "1 2 Fizz 4 Buzz ... FizzBuzz"),
        ("Pilha com Mínimo", "Implemente uma pilha que retorne o elemento mínimo em O(1).", "push(3),push(1),push(2),getMin()", "1"),
    ],
    "Avançado": [
        ("LRU Cache", "Implemente um cache LRU com get e put em O(1).", "capacity=2, put(1,1), put(2,2), get(1)", "1"),
        ("Merge Sort", "Implemente o algoritmo Merge Sort sem usar funções nativas de sort.", "[5,2,4,6,1,3]", "[1,2,3,4,5,6]"),
        ("Grafo BFS", "Encontre o caminho mais curto entre dois nós usando BFS.", "A→B→C, A→C", "A→C (distância 1)"),
    ],
}

_XP_RANGE = {
    "Básico": (200, 500),
    "Intermediário": (500, 1000),
    "Avançado": (1000, 2000),
}


def gerar_desafio(tecnologia: str, nivel: str) -> dict:
    """
    Retorna um dict com os campos do desafio gerado:
    titulo, descricao, entrada, saida_esperada, xp, nivel, tecnologia.
    Lança ValueError se o nível for inválido.
    """
    niveis_validos = list(_DESAFIOS.keys())
    if nivel not in niveis_validos:
        raise ValueError(f"Nível inválido: '{nivel}'. Use: {niveis_validos}")

    titulo, descricao, entrada, saida = random.choice(_DESAFIOS[nivel])
    xp_min, xp_max = _XP_RANGE[nivel]
    xp = random.randint(xp_min, xp_max)

    return {
        "tecnologia": tecnologia,
        "nivel": nivel,
        "titulo": titulo,
        "descricao": descricao,
        "entrada": entrada,
        "saida_esperada": saida,
        "xp": xp,
    }


# ---------------------------------------------------------------------------
# /certificado  — geração de certificado fictício
# ---------------------------------------------------------------------------

def gerar_certificado(nome: str, trilha: dict, hoje: Optional[date] = None) -> str:
    """
    Gera o certificado fictício em Markdown para o usuário e a trilha informados.
    Retorna a string completa do certificado.
    """
    if hoje is None:
        hoje = date.today()
    data_emissao = hoje.strftime("%d/%m/%Y")
    cert_id = f"DIO-{trilha['id']:03d}-{hoje.year}-{random.randint(100000, 999999)}"

    badges = "\n".join(f"🥇 {b}" for b in trilha.get("badges_disponiveis", []))

    return (
        f"# 🎓 CERTIFICADO DE CONCLUSÃO\n\n"
        f"**Certificamos que**\n\n"
        f"## ✨ {nome} ✨\n\n"
        f"concluiu com êxito a trilha:\n\n"
        f"### 📚 {trilha['nome']}\n\n"
        f"| Campo | Detalhe |\n"
        f"|-------|---------|\n"
        f"| 🎯 Tecnologia | {trilha['tecnologia']} |\n"
        f"| 📊 Nível | {trilha['nivel']} |\n"
        f"| 🔢 Módulos | {trilha['numero_de_modulos']} |\n"
        f"| ⭐ XP | {trilha['xp_total']} XP |\n"
        f"| 📅 Emissão | {data_emissao} |\n"
        f"| 🔖 ID | {cert_id} |\n\n"
        f"### 🏅 Badges\n\n{badges}\n\n"
        f"*Certificado fictício gerado para fins educacionais.*"
    )
