# Efeitos e checagens de motion: o que as skills da comunidade fazem que a reel-motion não faz

Resumo: dois posts de Instagram de 2026 apresentaram skills de vídeo e animação para agentes. Um mostra uma skill só, de efeitos sobre talking-head (51 efeitos com recorte da pessoa e rastreio do rosto); o outro, um carrossel com nove skills de animação feitas com código. Li o código das que encontrei. A arquitetura da maioria é a mesma da `reel-motion` (cena em código, render quadro a quadro, vídeo), então o ganho não está no motor: está no que elas conferem antes de entregar e no repertório de efeitos com profundidade (coisas atrás da cabeça). Esta nota separa o que confirmei no código do que é palpite, compara com as skills `reel-*` e lista o que virou mudança, o que virou ticket e o que fica de fora. Pesquisa de 2026-11-05.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [A skill de efeitos sobre talking-head](#2-a-skill-de-efeitos-sobre-talking-head)
3. [As skills de animação do carrossel](#3-as-skills-de-animação-do-carrossel)
4. [O que as skills reel-* já fazem melhor](#4-o-que-as-skills-reel-já-fazem-melhor)
5. [Decisões](#5-decisões)

## 1. Fontes e método

Os dois posts (links públicos, só o texto e os frames foram lidos; nada deles está transcrito aqui):

- [instagram.com/p/DfPGypijw2f](https://www.instagram.com/p/DfPGypijw2f/): carrossel de @okaashish com nove skills de animação para o Claude.
- [instagram.com/reel/De7JFJdo4KX](https://www.instagram.com/reel/De7JFJdo4KX/): reel de @vibha.in.progress mostrando a skill `/effects` sobre o próprio vídeo.

Repositórios lidos (clonados e lidos no código, não só no README):

| Sigla | Repositório | Licença | Achado com certeza? |
| - | - | - | - |
| VE | [Vibha-Ramprakash/claude-video-effects](https://github.com/Vibha-Ramprakash/claude-video-effects) | MIT | sim, é o do reel |
| AD | [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) | Apache 2.0 | sim |
| CAB | [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | MIT | sim |
| CDS | [cloveric/claude-drawing-skill](https://github.com/cloveric/claude-drawing-skill) | MIT | sim |
| MS | [LunaAI519/motion-skill](https://github.com/LunaAI519/motion-skill) | MIT | sim |
| MAN | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) | MIT | sim |
| HU | [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) | MIT | sim |
| LF | [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) | MIT | provável: o nome bate com o slide, o autor do slide não diz o repositório |
| AN | [cth9191/animate](https://github.com/cth9191/animate) | MIT | provável, pelo mesmo motivo |

Uma das nove (a de desenho à mão) não encontrei. O post de @vibha.in.progress diz 36 efeitos; o README do repositório lista 51.

Método: para cada skill, li o `SKILL.md`, os scripts que ele chama e o README, procurando três coisas que a `reel-motion` e a `reel-finish` não têm: uma checagem antes da entrega, um efeito que caiba no fluxo de talking-head com legenda, e uma técnica de render melhor que a nossa. Não rodei as skills em vídeo; o que digo do resultado delas vem do código e do que o reel mostra.

## 2. A skill de efeitos sobre talking-head

**O que é (VE, confirmado no código).** Um script Python grande (`scripts/fx.py`) com numpy e OpenCV. Para cada vídeo: recorta a pessoa com o MediaPipe Selfie Segmenter, acha o rosto com o detector YuNet do OpenCV, suaviza a trilha do rosto com um filtro de ida e volta (sem atraso, `smooth` em `fx.py`) e refina a borda da máscara com um guided filter (`guided`). Cada efeito é desenhado em camadas: o que fica atrás da pessoa, a pessoa recortada, o que fica na frente. O README resume como "tudo segue o rosto, e o que cobriria o rosto vai para trás da cabeça".

**Os efeitos.** 51, cada um com um nome que o usuário digita. Agrupados por mecanismo:

- **Atrás da cabeça:** palavra gigante na parede, palavra riscada, pilha de reels ou manchetes, sala que apaga com a pessoa acesa, túnel, chuva de teclas.
- **Seguindo o rosto:** mira que trava no rosto, itens orbitando a cabeça, lista ao lado da cabeça que se marca.
- **Interface:** comentário que se digita, botão seguir, notificações, interruptores do celular, cópias de apps.
- **Câmera e cor:** punch-in numa palavra, empurrão lento, gradações de cor, quadro congelado com seta.

**O que funciona e cabe no nosso fluxo.** A camada atrás da cabeça é a ideia de mais ganho: põe o autor dentro da cena em vez de debaixo de um adesivo. A `reel-finish` já recortava a pessoa, mas só para as palavras do template; os overlays da `reel-motion` ficavam sempre por cima do rosto. A suavização de ida e volta e o guided filter são técnicas conhecidas e baratas que deixariam o nosso recorte menos tremido. A trilha do rosto, se for um arquivo que as cenas leem, abre os efeitos que seguem a cabeça.

**O que não serve.** O agente aprova o próprio resultado, sem parar para o autor ver. Não há som nem legenda (o README diz). Instala dependências em silêncio. Roda um arquivo opcional com `exec`. As cores e as fontes da autora estão no código, então o estilo dela vem junto com a skill. Os efeitos de interface copiam a aparência de apps reais. Um deles desenha uma forma de onda falsa, com barras aleatórias, em vez da voz.

## 3. As skills de animação do carrossel

Todas fazem animação com código (SVG, canvas, HTML, Manim, Lottie) e transformam em vídeo. O que cada uma tem de diferente:

| Skill | Ideia que vale olhar | Confirmado? |
| - | - | - |
| AN | `textcheck.mjs` mede o texto renderizado: sai da margem, encosta em outro, fica pequeno demais; `framehash.mjs` compara quadros por hash para achar regressão | sim, li os dois scripts |
| HU | um portão anti-slideshow (`film_gate.py`) mede quanto a cena se mexe e reprova a que vira slide; um revisor independente, um agente que não fez a cena, confere antes de entregar; regras de leitura (pausa depois do sentido, respiro no fim) | sim, no README.en.md e nos scripts |
| CAB | folha de quadros de cada transição, um quadro a cada 0,1 s, para ver salto e peça que se mexe junto com outra | sim |
| LF | vocabulário de easing e durações por tipo de movimento | sim; o #52 já decidiu que easing não era o problema |
| AD, CDS | desenho traço a traço | sim; o ticket 70 já limitou o traço ao que carrega sentido |
| MS | catálogo de estilos de movimento por nome | sim; catálogo de estilo vai contra deixar o estilo com o autor |
| MAN | Manim para matemática | sim; fora do nosso tipo de vídeo |

## 4. O que as skills reel-* já fazem melhor

- **O autor aprova plano e stills antes do render.** Nas skills lidas, o agente renderiza e se aprova; só a HU tem uma conferência, feita por outro agente.
- **O tempo vem da fala.** Cada entrada cai no quadro da palavra, medida pelo Whisper sobre o SRT corrigido. As skills lidas pedem o tempo ao usuário ("quando eu disser 'olha'") ou animam sem fala.
- **Cada regra tem o porquê**, e o estilo fica num arquivo do autor, fora da skill.
- **Som e legenda** fazem parte da entrega (sons por material, legenda no template do autor). VE não tem nenhum dos dois.

## 5. Decisões

**Mudança feita nesta pesquisa.** A camada atrás da cabeça entrou nas duas skills:

- a `reel-finish` aceita `"behind": true` num overlay e põe o recorte da pessoa por cima dele, no projeto do CapCut e no mp4, só onde o rosto ocupa o quadro e por até 8 s;
- a `reel-motion` ganhou um catálogo de efeitos (`references/effects.md`) com o que está pronto, o que espera outra peça e o que não é oferecido, e oferece os efeitos no portão do plano, por nome, com um still dos que o autor nunca viu e com o `estilo.md` decidindo o gosto.

O buraco de referência: a `reel-motion` não tinha como pôr nada atrás do autor, então nenhum efeito desse tipo podia aparecer no plano, qualquer que fosse o reel. Testei a camada num trecho de um reel já publicado do autor (palavra gigante atrás da cabeça e sala apagada, com os prints por cima); a saída dos reels antigos ficou idêntica quadro a quadro. Falta abrir no CapCut um projeto com um overlay atrás da cabeça e fazer um reel real com um efeito do catálogo.

**Tickets no mapa #76** (cada um começa rodando a skill atual numa entrada real, para mostrar o buraco antes de mudar):

1. Checagem medida da cena antes do gate: texto fora da margem ou na legenda, quanto a cena se mexe, maior trecho parado (AN, HU). [#95](https://github.com/eusouosalmo/skills/issues/95)
2. Folha de quadros das transições (CAB). [#96](https://github.com/eusouosalmo/skills/issues/96)
3. Recorte mais estável: borda com guided filter e máscara suavizada entre quadros (VE). [#97](https://github.com/eusouosalmo/skills/issues/97)
4. Ritmo de leitura: pausa depois do sentido, respiro no fim, antecipação (HU). [#98](https://github.com/eusouosalmo/skills/issues/98)
5. Trilha do rosto lida pelas cenas e pelo punch-in (VE); destrava mira, órbita e adesivo que segue a cabeça. [#99](https://github.com/eusouosalmo/skills/issues/99)
6. Revisor independente antes do gate de stills (HU). [#100](https://github.com/eusouosalmo/skills/issues/100)
7. Silêncio antes do clímax nos efeitos sonoros. [#101](https://github.com/eusouosalmo/skills/issues/101)
8. Empurrão lento na `reel-finish`. [#102](https://github.com/eusouosalmo/skills/issues/102)

**Fora:** Manim, catálogos de estilo, música gerada, voz de IA, cópia da interface de apps, efeitos que alteram a aparência do autor, gradações de cor como look da skill.
