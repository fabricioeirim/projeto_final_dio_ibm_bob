---
description: Exibe o plano de estudos formatado de uma trilha DIO com base na tecnologia informada
argument-hint: <tecnologia>
---

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja propriedade `tecnologia` contenha (busca parcial, sem distinção de maiúsculas/minúsculas) o valor "$1".

Se nenhuma trilha for encontrada, informe ao usuário de forma amigável e liste as tecnologias disponíveis no arquivo.

Caso encontre a trilha, exiba o plano de estudos completo no seguinte formato Markdown:

---

# 📚 Plano de Estudos — {nome da trilha}

**🎯 Tecnologia:** {tecnologia}
**📊 Nível:** {nivel}
**🔢 Número de Módulos:** {numero_de_modulos}
**⭐ XP Total:** {xp_total} XP
**♾️ Acesso Vitalício:** Sim / Não

---

## 🗺️ Módulos da Trilha

Gere uma lista numerada de {numero_de_modulos} módulos coerentes e realistas para a tecnologia informada. Cada módulo deve ter um título descritivo e uma breve descrição de 1 linha do que o aluno aprenderá.

---

## 🏅 Badges Disponíveis

Liste as badges: {badges_disponiveis}

---

## 📡 Próximas Lives ao Vivo

Para cada item em `lives_ao_vivo`, exiba: título, data formatada (DD/MM/AAAA) e horário.

---

## 🎁 Promoção Ativa

Se `promocoes` não for nulo, exiba: desconto, validade formatada e cupom. Caso contrário, escreva "Nenhuma promoção ativa no momento."
