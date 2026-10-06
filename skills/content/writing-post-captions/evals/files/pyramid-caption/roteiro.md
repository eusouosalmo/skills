---
type: project
status: active
date: 2026-10-05
---

# Roteiro: arquiteto, amplitude e profundidade

Plataforma: Instagram Reels | Duração alvo: 60 a 90 s | Objetivo: puxar conversa nos comentários
Série: primeiro reel sobre pensar como arquiteto de software (capítulo 2 de Fundamentos da Arquitetura de Software). Feito com a skill writing-short-video-scripts.

## Script

| Bloco | Fala | Visual |
|---|---|---|
| Gancho | Quando eu precisei tomar decisões como arquiteto de software, eu tive dificuldade. Justamente porque eu tava acostumado a ser só desenvolvedor. | Tu falando pra câmera. Texto na tela: "Decidir como arquiteto de software foi difícil. Por quê?" |
| Contexto | Pensa numa pirâmide com tudo que tu sabe. Em cima, o que tu domina. No meio, o que tu sabe que existe, mas não domina. Embaixo, o que tu nem sabe que existe. | Pirâmide desenhada, uma camada por frase, com o texto de cada uma. A pirâmide sai da tela depois da terceira camada. |
| Entrega | O desenvolvedor escolhe uma tecnologia e se aprofunda nela. E precisa se atualizar o tempo todo, porque sempre sai versão nova, vulnerabilidade, biblioteca nova. Já o arquiteto precisa de um conhecimento amplo, porque é ele que escolhe a tecnologia. Só que não dá pra se aprofundar em tudo, porque cada uma toma o tempo de conhecer as outras. | Volta pra câmera. Texto na tela: "versão nova, vulnerabilidade, biblioteca nova". |
| Entrega (caso) | Na prática, fui aprendendo o que precisava, tipo serviços do GCP e partição de banco. Uma vez, uma query ignorava o índice GIN que a gente criou num campo jsonb. Eu filtrava com a setinha, e o índice só entra com operadores como o arroba maior que. Eu nem sabia que essa diferença existia. | Na tela, os operadores: `->` riscado e `@>` destacado. Em "nem sabia", um flash da camada de baixo da pirâmide. |
| Conexão | Pra decidir arquitetura, conhece mais opções, porque só dá pra comparar o que tu conhece. | Tu falando pra câmera. |
| CTA | E tu, hoje tá mais pra se aprofundar numa tecnologia ou pra conhecer várias? | Texto na tela: "Se aprofundar ou conhecer várias?" |

Ganchos alternativos:
- Crença contrariada: "Se aprofundar numa tecnologia te faz um desenvolvedor melhor. Pra decidir como arquiteto de software, não é bem assim."
- Público pelo papel: "Se tu é desenvolvedor e vai ter que escolher a tecnologia do projeto, o jeito que tu estudou até aqui não é o que tu vai precisar."

A checar antes de gravar:
- As três camadas da pirâmide e como cada papel se relaciona com elas. Conferido em fonte pública (Neal Ford, "Knowledge Breadth versus Depth", 2015); falta reler as duas páginas do capítulo 2 no livro.
- Índice GIN e operadores: conferido na doc oficial do PostgreSQL (seção 8.14.4). O GIN em jsonb atende `@>` (e outros operadores de contenção e existência), não o `->`.
- Ler a fala em voz alta: "setinha" e "arroba maior que" soam naturais pra ti?
- Duração: 195 palavras, no limite dos 90 s. Medir na leitura.

Crédito para a legenda: Fundamentos da Arquitetura de Software, de Mark Richards e Neal Ford, capítulo 2.

## Teleprompter

Quando eu precisei tomar decisões como arquiteto de software, eu tive dificuldade.
Justamente porque eu tava acostumado a ser só desenvolvedor.
Pensa numa pirâmide com tudo que tu sabe.
Em cima, o que tu domina.
No meio, o que tu sabe que existe, mas não domina.
Embaixo, o que tu nem sabe que existe.
O desenvolvedor escolhe uma tecnologia e se aprofunda nela.
E precisa se atualizar o tempo todo, porque sempre sai versão nova, vulnerabilidade, biblioteca nova.
Já o arquiteto precisa de um conhecimento amplo, porque é ele que escolhe a tecnologia.
Só que não dá pra se aprofundar em tudo, porque cada uma toma o tempo de conhecer as outras.
Na prática, fui aprendendo o que precisava, tipo serviços do GCP e partição de banco.
Uma vez, uma query ignorava o índice GIN que a gente criou num campo jsonb.
Eu filtrava com a setinha, e o índice só entra com operadores como o arroba maior que.
Eu nem sabia que essa diferença existia.
Pra decidir arquitetura, conhece mais opções, porque só dá pra comparar o que tu conhece.
E tu, hoje tá mais pra se aprofundar numa tecnologia ou pra conhecer várias?

Duração estimada: 195 palavras, 90 s a 130 palavras por minuto.

