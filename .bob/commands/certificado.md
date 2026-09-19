---
description: Gera um certificado fictício em Markdown com nome do usuário e trilha concluída
argument-hint: <seu-nome> <tecnologia-da-trilha>
---

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e localize a trilha cuja propriedade `tecnologia` contenha (busca parcial, sem distinção de maiúsculas/minúsculas) o valor "$2".

Se nenhuma trilha for encontrada, informe ao usuário de forma amigável e liste as tecnologias disponíveis.

Caso a trilha seja encontrada, gere um certificado fictício formatado em Markdown conforme o modelo abaixo. Use a data atual do sistema para a data de emissão.

---

# 🎓 CERTIFICADO DE CONCLUSÃO

---

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🏆  DIO — Digital Innovation One  🏆               ║
║                                                                  ║
║                   CERTIFICADO DE CONCLUSÃO                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Certificamos que**

## ✨ {$1} ✨

concluiu com êxito a trilha de aprendizado:

### 📚 {nome da trilha}

---

| Campo                  | Detalhe                        |
|------------------------|--------------------------------|
| 🎯 Tecnologia          | {tecnologia}                   |
| 📊 Nível               | {nivel}                        |
| 🔢 Módulos Concluídos  | {numero_de_modulos} módulos    |
| ⭐ XP Conquistado       | {xp_total} XP                  |
| 📅 Data de Emissão     | {data atual formatada DD/MM/AAAA} |
| 🔖 ID do Certificado   | DIO-{id da trilha}-{ano atual}-{número aleatório de 6 dígitos} |

---

### 🏅 Badges Conquistadas

{liste cada badge de badges_disponiveis com o emoji 🥇 na frente}

---

> *"A jornada de mil milhas começa com um único passo."*
> — Lao Tsé

---

**Digital Innovation One**
Plataforma líder em educação tecnológica no Brasil.

*Este é um certificado fictício gerado para fins educacionais e de demonstração.*
