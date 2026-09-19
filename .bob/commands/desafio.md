---
description: Gera um desafio de código aleatório baseado em uma tecnologia e nível de dificuldade
argument-hint: <tecnologia> <nivel: Básico|Intermediário|Avançado>
---

Com base nos parâmetros fornecidos — tecnologia: "$1" e nível: "$2" — gere um desafio de código aleatório e criativo.

Se nenhum argumento for informado, escolha aleatoriamente uma tecnologia e nível do arquivo `dio_explorer/data/trilhas_dio.json` e informe ao usuário o que foi sorteado.

O desafio deve ser exibido no seguinte formato Markdown:

---

# ⚔️ Desafio de Código — {tecnologia} | Nível {nivel}

**🎲 Desafio:** {título criativo e curto do desafio, ex: "Construtor de Fibonacci Recursivo"}

**📝 Descrição:**
{Descrição clara do problema em 3 a 5 linhas, definindo o que deve ser implementado, quais entradas o programa receberá e qual saída é esperada.}

**📌 Requisitos:**
- {Requisito 1}
- {Requisito 2}
- {Requisito 3 (adicione mais se necessário)}

**💡 Exemplo de Entrada e Saída:**
```
Entrada: {exemplo de input}
Saída esperada: {exemplo de output}
```

**🏆 Critérios de Avaliação:**
- Correção da solução
- Legibilidade e organização do código
- Uso de boas práticas da linguagem {tecnologia}
- {Critério extra relevante para o nível}

**⏱️ Tempo sugerido:** {X} minutos

**⭐ XP ao completar:** {valor proporcional ao nível: Básico = 200-500 XP, Intermediário = 500-1000 XP, Avançado = 1000-2000 XP}

---

> 💬 Quando terminar, compartilhe sua solução aqui no chat para eu revisar e dar feedback!
