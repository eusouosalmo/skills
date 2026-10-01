# Como a doc oficial e a comunidade escrevem skills

Resumo: as fontes concordam no esqueleto (description como gatilho, SKILL.md curto, detalhe em arquivos de um nível, comparação com e sem a skill em contexto limpo) e divergem no conteúdo da description, no tom das instruções (explicar o porquê ou proibir com MUST) e no formato dos evals. Cada prática abaixo traz o que é, por que existe, a fonte e o nível de confiança. Pesquisa feita em 2026-10-01 para o ticket #2; não toma decisões, só alimenta o ticket de desenho da skill de criação.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [Estrutura e progressive disclosure](#2-estrutura-e-progressive-disclosure)
3. [A description (gatilho)](#3-a-description-gatilho)
4. [Graus de liberdade e tom das instruções](#4-graus-de-liberdade-e-tom-das-instruções)
5. [Invocação: modelo ou usuário](#5-invocação-modelo-ou-usuário)
6. [Evals e como testar uma skill](#6-evals-e-como-testar-uma-skill)
7. [Iteração](#7-iteração)
8. [Anti-padrões](#8-anti-padrões)
9. [Onde as fontes concordam e onde divergem](#9-onde-as-fontes-concordam-e-onde-divergem)
10. [Licença do skill-creator](#10-licença-do-skill-creator)
11. [Perguntas abertas para o ticket de desenho](#11-perguntas-abertas-para-o-ticket-de-desenho)

## 1. Fontes e método

| Sigla | Fonte | Tipo | Licença |
| - | - | - | - |
| BP | [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (platform.claude.com) | doc oficial Anthropic | doc |
| SPEC | [Agent Skills specification](https://agentskills.io/specification) | especificação aberta | doc |
| AS | Guias de agentskills.io: [best practices](https://agentskills.io/skill-creation/best-practices), [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) | doc oficial do padrão | doc |
| CC | [Extend Claude with skills](https://code.claude.com/docs/en/skills) (Claude Code) | doc oficial Anthropic | doc |
| ENG | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (out. 2025) | blog de engenharia Anthropic | doc |
| SC | [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (anthropics/skills) | skill first-party | Apache 2.0 |
| MP | [writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) (SKILL.md e SKILL-MECHANICS.md) e [.agents/invocation.md](https://github.com/mattpocock/skills/blob/main/.agents/invocation.md), de Matt Pocock | comunidade | MIT |
| SP | [writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills), de obra/superpowers (Jesse Vincent) | comunidade | MIT |
| VL | [AGENTS.md de vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/blob/main/AGENTS.md) | comunidade (empresa) | sem licença declarada na API |
| SW | [Claude Skills are awesome, maybe a bigger deal than MCP](https://simonwillison.net/2025/Oct/16/claude-skills/), Simon Willison (out. 2025) | comunidade (comentário) | blog |

Níveis de confiança, como pede o mapa (#1):

- **confirmado:** está em doc oficial (BP, SPEC, AS, CC, ENG).
- **convenção:** não é doc oficial, mas vários repositórios fazem igual.
- **relato:** um autor afirma, sem doc oficial nem prática repetida.

O SC é first-party, mas é uma skill e não documentação. Quando o que ele diz também aparece em AS ou BP, conta como confirmado; quando aparece só nele, vira relato (first-party).

## 2. Estrutura e progressive disclosure

### 2.1 Três níveis de carregamento

- **O que é:** name e description ficam sempre no contexto (cerca de 100 tokens por skill); o corpo do SKILL.md entra quando a skill dispara; arquivos de apoio (scripts/, references/, assets/) só quando forem necessários.
- **Por que existe:** o context window é dividido com system prompt, histórico e as outras skills. A BP chama o contexto de "a public good". O formato permite instalar muitas skills sem pagar o corpo de cada uma em toda conversa. O ENG compara a um manual com sumário, capítulos e apêndice.
- **Fonte:** SPEC (seção Progressive disclosure), BP (Runtime environment), ENG, SC (Progressive Disclosure). SW destaca que cada skill custa "a few dozen extra tokens" até ser usada.
- **Confiança:** confirmado.

### 2.2 SKILL.md com menos de 500 linhas

- **O que é:** o corpo fica abaixo de 500 linhas; a SPEC acrescenta uma recomendação de menos de 5.000 tokens. Ao chegar perto do limite, o conteúdo vai para arquivos separados.
- **Por que existe:** depois de carregado, cada token do corpo compete com o resto do contexto. No Claude Code o custo é recorrente: o corpo entra como mensagem e fica no contexto pelos turnos seguintes (CC, Skill content lifecycle).
- **Fonte:** SPEC, BP, CC, SC, VL.
- **Confiança:** confirmado (e convenção, porque VL repete a regra).
- **Variação:** o SP mira bem mais curto, em palavras: menos de 150 para workflows de getting-started, menos de 200 para skills carregadas com frequência, menos de 500 para as demais. Relato.

### 2.3 Referências a um nível de profundidade

- **O que é:** todo arquivo de apoio é linkado direto do SKILL.md; nada de SKILL.md apontar para advanced.md que aponta para details.md.
- **Por que existe:** a BP diz que, em referências aninhadas, o Claude tende a ler só um pedaço (por exemplo com head -100) e fica com informação incompleta.
- **Fonte:** BP (Avoid deeply nested references), SPEC (File references), VL.
- **Confiança:** confirmado.

### 2.4 Sumário em arquivos de referência longos

- **O que é:** arquivo de referência com mais de 100 linhas (BP) ou 300 linhas (SC) começa com um sumário.
- **Por que existe:** se o agente fizer uma leitura parcial, ainda vê o escopo inteiro e sabe para onde pular.
- **Fonte:** BP, SC.
- **Confiança:** confirmado (o limite exato muda de fonte para fonte).

### 2.5 Dizer quando ler cada arquivo

- **O que é:** o link para um arquivo de apoio vem com a condição de leitura ("leia references/api-errors.md se a API devolver status diferente de 200"), e não com um genérico "veja references/".
- **Por que existe:** é a condição que faz o agente carregar o arquivo na hora certa. Sem ela, o arquivo ou é ignorado ou é lido à toa.
- **Fonte:** AS (Structure large skills), CC (Add supporting files), SC.
- **Confiança:** confirmado.
- **Leitura de Matt Pocock:** ele generaliza isso no conceito de context pointer. A description de uma skill e uma linha do AGENTS.md que cita um doc são o mesmo objeto, e é a redação do ponteiro, não o alvo, que decide se o agente chega ao material. O teste dele para decidir o que sai do arquivo principal: o que todo branch usa fica no arquivo; o que só alguns branches usam vai para trás de um ponteiro. Relato.

### 2.6 Organizar por domínio ou variante

- **O que é:** quando a skill cobre vários domínios (finance, sales; aws, gcp), cada um ganha seu arquivo e o SKILL.md vira índice.
- **Por que existe:** o agente lê só o arquivo do domínio da tarefa; os outros não custam contexto.
- **Fonte:** BP (Pattern 2), SC (Domain organization).
- **Confiança:** confirmado.

### 2.7 Scripts para o que é determinístico

- **O que é:** operações frágeis ou repetitivas viram scripts em scripts/ que o agente executa, em vez de gerar o código toda vez. A instrução precisa deixar claro se o script é para executar ou para ler como referência.
- **Por que existe:** script pronto é mais confiável que código gerado, não ocupa contexto (só a saída entra), economiza tempo e garante consistência. Também é sinal de iteração: se em todas as rodadas de teste o agente escreveu o mesmo helper, ele deve virar script.
- **Fonte:** BP (Provide utility scripts), AS (Bundling reusable scripts), SC (Look for repeated work), VL (Prefer scripts over inline code).
- **Confiança:** confirmado.
- **Detalhe prático:** o SP manda chamar o script pelo interpretador (bash scripts/x.sh), porque alguns empacotadores tiram o bit de execução. VL exige set -e, status em stderr e JSON em stdout. Relato em cada caso.

### 2.8 Pastas padrão e nomes descritivos

- **O que é:** scripts/, references/ e assets/ são as pastas sugeridas pela SPEC, todas opcionais. Os arquivos têm nome que diz o conteúdo (form_validation_rules.md, e não doc2.md).
- **Por que existe:** o agente navega a skill como um sistema de arquivos, e um nome claro ajuda a achar o arquivo certo sem abrir os outros.
- **Fonte:** SPEC, BP (Runtime environment).
- **Confiança:** confirmado.

### 2.9 Co-location e hierarquia de informação

- **O que é:** Matt Pocock separa o conteúdo em steps (o que o agente faz, em ordem) e reference (regras e fatos consultados quando preciso) e põe tudo numa escada: step no arquivo, reference no arquivo, reference em outro arquivo. Co-location é manter definição, regra e ressalva de um conceito juntas, sob o mesmo título.
- **Por que existe:** se reference que deveria sair do arquivo enterra os steps, segui-los vira questão de sorte. Material espalhado é lido aos pedaços. O nome que ele dá a um documento longo demais, mesmo com toda linha válida, é sprawl.
- **Fonte:** MP (SKILL.md, Information hierarchy).
- **Confiança:** relato.

## 3. A description (gatilho)

### 3.1 A description é o mecanismo de disparo

- **O que é:** o agente decide se carrega a skill olhando só name e description. A AS diz que a description "carries the entire burden of triggering".
- **Por que existe:** é consequência direta do progressive disclosure: o corpo não está no contexto na hora da decisão.
- **Fonte:** AS (Optimizing descriptions), BP, CC, SC, ENG.
- **Confiança:** confirmado.

### 3.2 Dizer o que faz e quando usar

- **O que é:** a description traz as duas coisas, com termos concretos que o usuário falaria (PDFs, forms, .xlsx).
- **Por que existe:** o agente escolhe entre potencialmente mais de 100 skills; uma description vaga ("Helps with documents") não diferencia nenhuma delas.
- **Fonte:** BP (Writing effective descriptions), SPEC (description field), CC, VL.
- **Confiança:** confirmado.
- **Divergência forte:** o SP manda a description dizer só quando usar e nunca resumir o processo. A justificativa é um teste do autor: a description "code review between tasks" fez o agente rodar uma única revisão, quando o corpo pedia duas; sem o resumo, o agente leu o corpo e seguiu as duas etapas. A lição dele: um resumo do workflow vira atalho, e o agente pula o corpo. Relato (um autor, um experimento descrito).

### 3.3 Terceira pessoa ou imperativo

- **O que é:** a BP manda escrever em terceira pessoa ("Processes Excel files..."), nunca "I can help" nem "You can use". A AS manda usar frase imperativa dirigida ao agente ("Use this skill when..."). O SP pede as duas coisas: começar com "Use when..." e manter terceira pessoa.
- **Por que existe:** BP: a description é injetada no system prompt e um ponto de vista inconsistente atrapalha a descoberta. AS: o agente está decidindo se age, então a description deve dizer quando agir.
- **Fonte:** BP, AS, SP.
- **Confiança:** confirmado para as duas formas, que não são idênticas. O padrão "Faz X. Use when Y." (BP nos exemplos, e o AGENTS.md deste repo) cobre as duas.

### 3.4 Ser "pushy"

- **O que é:** listar de forma explícita os contextos em que a skill se aplica, inclusive quando o usuário não cita o domínio ("even if they don't explicitly mention...").
- **Por que existe:** o SC afirma que hoje o Claude tende a "undertrigger", ou seja, deixa de usar a skill quando ela ajudaria.
- **Fonte:** SC (Write the SKILL.md), AS (Err on the side of being pushy).
- **Confiança:** confirmado.
- **Tensão:** Matt Pocock trata cada palavra de um ponteiro sempre carregado como custo em todo turno e manda podar mais que o corpo (ver 3.6).

### 3.5 Caso de uso principal primeiro

- **O que é:** o caso principal vai na frente da description.
- **Por que existe:** no Claude Code, description e when_to_use somados são cortados em 1.536 caracteres na listagem. Com muitas skills, o Claude Code também tira descriptions inteiras para caber num orçamento de cerca de 1% do context window, começando pelas skills menos usadas. O que está no fim pode sumir.
- **Fonte:** CC (Frontmatter reference; Skill descriptions are cut short). O limite da SPEC é 1.024 caracteres.
- **Confiança:** confirmado.

### 3.6 Uma palavra-chave por branch, sem sinônimos

- **O que é:** pôr a leading word na frente; um gatilho por branch distinto (sinônimos que renomeiam o mesmo caso são um branch escrito duas vezes); tirar da description a identidade que o corpo já carrega.
- **Por que existe:** a description é contexto pago em todo turno. A palavra que o usuário de fato usa nos prompts, no código e na documentação dispara a skill com mais confiança do que uma lista de sinônimos.
- **Fonte:** MP (Context pointers; Leading words).
- **Confiança:** relato.
- **Divergência:** o SP pede o contrário em keyword coverage: incluir sinônimos ("timeout/hang/freeze"), mensagens de erro e sintomas. Relato também.

### 3.7 Descrever a intenção do usuário, não a implementação

- **O que é:** escrever o que o usuário quer conseguir, não a mecânica interna da skill. O SP diz algo parecido: descrever o problema (race condition), e não o sintoma específico de uma linguagem (setTimeout), salvo quando a skill é mesmo de uma tecnologia.
- **Por que existe:** o agente compara a description com o que o usuário pediu.
- **Fonte:** AS (Focus on user intent), SP.
- **Confiança:** confirmado.

### 3.8 Skills simples demais não disparam

- **O que é:** pedidos de um passo ("leia este PDF") podem não disparar a skill mesmo com a description perfeita, porque o agente resolve sozinho.
- **Por que existe:** o agente só consulta skills quando a tarefa pede conhecimento ou capacidade além do básico. Isso muda como se escrevem os testes de gatilho (ver 6.5).
- **Fonte:** AS (How skill triggering works), SC.
- **Confiança:** confirmado.

## 4. Graus de liberdade e tom das instruções

### 4.1 Especificidade proporcional à fragilidade

- **O que é:** liberdade alta (texto e heurísticas) quando várias abordagens servem; média (pseudocódigo ou script com parâmetros) quando existe um padrão preferido; baixa (script exato, "não mude o comando") quando a operação é frágil ou a sequência é obrigatória. A BP usa a imagem de uma ponte estreita com abismo dos dois lados contra um campo aberto. A AS acrescenta que cada parte da skill é calibrada separadamente.
- **Por que existe:** instrução rígida demais atrapalha tarefas que dependem de contexto; instrução solta demais quebra operações frágeis.
- **Fonte:** BP (Set appropriate degrees of freedom), AS (Calibrating control).
- **Confiança:** confirmado.

### 4.2 Um padrão, não um cardápio

- **O que é:** escolher uma ferramenta ou abordagem padrão e citar a alternativa só como saída de emergência ("use pdfplumber; para PDF escaneado, pdf2image com pytesseract").
- **Por que existe:** listar opções equivalentes deixa o agente na dúvida, e ele gasta passos testando várias.
- **Fonte:** BP (Avoid offering too many options), AS (Provide defaults, not menus).
- **Confiança:** confirmado.

### 4.3 Ensinar o método, não a resposta

- **O que é:** a skill ensina como abordar uma classe de problemas, não o que produzir num caso específico.
- **Por que existe:** a skill vai rodar em prompts que o autor não previu. Uma resposta específica só serve para aquele caso.
- **Fonte:** AS (Favor procedures over declarations); SC (Generalize from the feedback); MP (FAQ do doc: skill escrita a partir de uma única execução sai específica demais, por isso o pedido de abstrair de propósito).
- **Confiança:** confirmado.

### 4.4 Só o que o modelo não sabe

- **O que é:** partir do princípio de que o modelo já é capaz e cortar toda explicação que ele não precisa. Perguntas de teste: "o agente erraria sem esta instrução?" (AS) e "esta frase muda o comportamento em relação ao padrão?" (MP, teste do no-op).
- **Por que existe:** explicação redundante custa contexto e dilui a atenção. A AS observa que skills exaustivas demais podem atrapalhar, porque o agente segue instruções que não se aplicam à tarefa.
- **Fonte:** BP (Concise is key), AS (Add what the agent lacks; Aim for moderate detail), CC, MP (Pruning), SP (Token efficiency).
- **Confiança:** confirmado, e também convenção.
- **Complemento de Matt Pocock:** o ambiente (package.json, configs, --help) já é fonte da verdade; repetir isso na skill é um cache que envelhece. Vale guardar o que o agente não acharia sozinho: a convenção não escrita, o motivo de uma escolha, a pegadinha. O SP diz o mesmo ao mandar consultar --help em vez de listar flags. Relato em cada fonte, convergente.

### 4.5 Explicar o porquê ou dar a ordem

- **O que é:** o SC e a AS mandam explicar o motivo em vez de usar ALWAYS e NEVER em caixa alta; para o SC, caixa alta é "a yellow flag". A CC diz o oposto para o corpo: "State what to do rather than narrating how or why", porque cada linha é custo recorrente. No exemplo de iteração da BP, o Claude A sugere trocar "always filter" por "MUST filter".
- **Por que existe:** SC e AS: o modelo entende o propósito e decide melhor em situações que a regra não previu. CC: economia de contexto.
- **Fonte:** SC (Writing Style; Explain the why), AS (Iterating on the skill), CC (Types of skill content), BP (Iterating on existing Skills).
- **Confiança:** confirmado, mas com orientações oficiais em tensão.

### 4.6 Positivo em vez de proibição, e quando proibir

- **O que é:** Matt Pocock diz que proibir ("não faça X") põe X no contexto e o torna mais provável. A alternativa é escrever o comportamento desejado. A proibição só se justifica como guardrail que não dá para escrever de forma positiva, e mesmo assim acompanhada do alvo positivo. O SP chega a uma regra mais fina, que chama de Match the Form to the Failure. Para um agente que conhece a regra e a quebra sob pressão: proibição, tabela de racionalizações e red flags. Para saída com formato errado: receita positiva do que a saída é. Para elemento que falta: um campo obrigatório no template. Para comportamento condicional: uma condição observável, e não uma regra com exceções.
- **Por que existe:** o SP relata testes de redação em que a versão com proibição gerou mais do conteúdo indesejado que a versão com receita, e que acrescentar uma cláusula de nuance ("a não ser que importe") deixou a receita instável.
- **Fonte:** MP (Leading words, parágrafo Negation), SP (Match the Form to the Failure).
- **Confiança:** relato (dois autores convergem na parte sobre formato; só o SP defende proibição para skills de disciplina).

### 4.7 Leading words

- **O que é:** usar uma palavra compacta que o modelo já conhece do pré-treino (tight, red, tracer bullet) e repeti-la como token, em vez de explicar a ideia em frases. Serve no corpo (execução) e na description (invocação).
- **Por que existe:** a palavra aproveita conhecimento que o modelo já tem e economiza tokens. Uma palavra inventada não traz esse conhecimento, então precisa de definição.
- **Fonte:** MP (Leading words).
- **Confiança:** relato.

### 4.8 Critérios de conclusão

- **O que é:** todo step termina numa condição verificável de pronto. Quanto mais exigente o critério ("todo model alterado considerado"), mais trabalho de investigação o agente faz.
- **Por que existe:** um critério vago convida a concluir antes da hora, porque os passos seguintes, visíveis, puxam o agente para frente. A solução preferida é deixar o critério nítido; dividir a sequência só ajuda se houver um limite real de contexto (subagent ou handoff).
- **Fonte:** MP (Steps and completion criteria). A BP trata o mesmo problema com checklists e feedback loops (validar, corrigir, repetir).
- **Confiança:** confirmado para checklist e validation loop (BP, AS); relato para a teoria de critérios de conclusão.

### 4.9 Padrões de conteúdo citados pela doc oficial

- **Template de saída:** é mais confiável que descrever o formato em prosa, porque o agente imita estruturas concretas. Confirmado (BP, AS, SC).
- **Exemplos de entrada e saída:** passam estilo e nível de detalhe melhor que descrições. Confirmado (BP, SC). O SP acrescenta "um exemplo excelente vale mais que vários medianos" e nada de exemplo em cinco linguagens. Relato.
- **Seção de gotchas:** fatos do ambiente que contrariam o que seria razoável supor; para a AS, é muitas vezes o conteúdo de maior valor. Fica no SKILL.md, porque o agente pode não perceber o gatilho para abrir outro arquivo. Confirmado (AS).
- **Plan-validate-execute:** para operações em lote ou destrutivas, gerar um plano estruturado, validar com script e só então executar. Confirmado (BP, AS).
- **Terminologia consistente:** um termo por conceito ao longo da skill. Confirmado (BP). Matt Pocock chega ao mesmo ponto pelo single source of truth.

## 5. Invocação: modelo ou usuário

### 5.1 Padrão: os dois podem invocar

- **O que é:** sem configuração, o usuário digita /nome e o modelo carrega a skill quando acha relevante.
- **Fonte:** CC (Control who invokes a skill).
- **Confiança:** confirmado.

### 5.2 disable-model-invocation: true

- **O que é:** só o usuário invoca. A description sai do contexto do modelo.
- **Por que existe:** para workflows com efeito colateral ou cujo momento o usuário quer controlar (/commit, /deploy). Nas palavras da CC, não se quer o Claude decidindo fazer deploy porque o código "parece pronto". Também zera o custo de contexto da description.
- **Fonte:** CC; MP (SKILL-MECHANICS.md, invocation.md).
- **Confiança:** confirmado.
- **Leitura de Matt Pocock:** a escolha troca uma carga pela outra. Model-invoked paga context load permanente para ganhar descoberta. User-invoked não custa contexto, mas custa cognitive load, porque o humano vira o índice e precisa lembrar que a skill existe. Daí a regra dele: só deixar model-invoked se o agente ou outra skill precisa alcançá-la sozinho; nos user-invoked, a description vira resumo de uma linha para humanos, sem lista de gatilhos. Quando há muitas user-invoked, ele usa uma router skill que lista as outras. Relato.
- **Consequência:** uma skill user-invoked não pode ser chamada por outra skill (CC: o bloqueio vale para chamadas do modelo; MP: "it can never reach another user-invoked skill"). Confirmado.

### 5.3 user-invocable: false

- **O que é:** só o modelo invoca; a skill some do menu /.
- **Por que existe:** conhecimento de fundo que não faz sentido como comando (o exemplo da CC é legacy-system-context).
- **Fonte:** CC.
- **Confiança:** confirmado (específico do Claude Code).

### 5.4 Reference content e task content

- **O que é:** a CC separa skills de referência (convenções, estilo, que rodam inline junto da conversa) de skills de tarefa (passos de uma ação, muitas vezes invocadas à mão). O SP divide em technique, pattern e reference. Matt Pocock separa steps de reference dentro de qualquer documento.
- **Por que existe:** o tipo indica como invocar e como testar (ver 6.4).
- **Fonte:** CC, SP, MP.
- **Confiança:** confirmado (CC); as outras taxonomias são relato.

### 5.5 Campos só do Claude Code

- **O que é:** disable-model-invocation, user-invocable, context: fork, hooks, paths, model, effort, when_to_use e outros são extensões do Claude Code. No upload para o claude.ai, na Skills API e no package_skill.py, campos fora dos seis da SPEC (name, description, license, compatibility, metadata, allowed-tools) dão erro na hora.
- **Por que existe:** a SPEC é o mínimo portátil; cada cliente pode estender.
- **Fonte:** CC (Using skill frontmatter outside Claude Code), SPEC.
- **Confiança:** confirmado.

### 5.6 O corpo fica no contexto e pode ser cortado

- **O que é:** no Claude Code, a skill invocada entra uma vez e não é relida. Depois de uma compactação, só os primeiros 5.000 tokens de cada skill voltam, num orçamento total de 25.000.
- **Por que existe:** é como o harness administra contexto. Consequências que a CC tira disso: escrever instruções que valem para a tarefa inteira ("rode os testes depois de cada edição", e não "rode os testes"), pôr o mais importante no topo e transformar em hook a regra que precisa valer sempre.
- **Fonte:** CC (Skill content lifecycle; Claude stops following a skill).
- **Confiança:** confirmado.
- **Paralelo:** o SP diz para não criar skill para restrição mecânica que dá para checar com regex ou validação, e automatizar em vez disso. Relato, convergente com a CC.

### 5.7 context: fork

- **O que é:** roda a skill num subagent que não vê o histórico da conversa.
- **Por que existe:** isola tarefas longas. A CC avisa que só faz sentido para skill com tarefa explícita; uma skill só de diretrizes devolve nada útil.
- **Fonte:** CC (Run skills in a subagent).
- **Confiança:** confirmado.

### 5.8 Como uma skill chama outra

- **O que é:** o SP usa marcadores como "REQUIRED SUB-SKILL: Use superpowers:x" e proíbe links com @, que carregam o arquivo na hora. Matt Pocock manda escrever "Call the Skill tool with X", uma chamada por skill, e nunca links do tipo ../outra-skill/ARQUIVO.md. O ADR 0002 deste repo já decidiu chamar por nome.
- **Por que existe:** só a pasta da skill é instalada, então caminhos para outra skill quebram. Matt afirma que nomear a ferramenta aumenta a taxa de acerto em relação a soltar um /nome no texto.
- **Fonte:** SP (Cross-Referencing Other Skills), MP (invocation.md).
- **Confiança:** convenção (os dois chamam por nome); a forma exata é relato.

## 6. Evals e como testar uma skill

### 6.1 Evals antes da documentação

- **O que é:** rodar o Claude sem a skill em tarefas representativas, anotar onde falha, criar três cenários que cobrem essas falhas, medir o baseline e só então escrever o mínimo para passar.
- **Por que existe:** para resolver problemas reais, e não imaginados. A skill sai menor e com efeito mensurável.
- **Fonte:** BP (Build evaluations first), ENG (Start with evaluation).
- **Confiança:** confirmado.
- **Versão da comunidade:** o SP leva isso ao extremo como TDD de documentação, com a Iron Law "NO SKILL WITHOUT A FAILING TEST FIRST": skill escrita antes do teste deve ser apagada, e a regra vale também para edições. O princípio central dele: quem não viu o agente falhar sem a skill não sabe se a skill ensina a coisa certa. Relato.

### 6.2 Comparar com e sem a skill, em contexto limpo

- **O que é:** cada prompt roda duas vezes: com a skill e sem ela (ou com a versão anterior, se for melhoria). Cada rodada começa numa sessão ou subagent novo.
- **Por que existe:** ver a skill disparar mostra que o Claude a achou, não que ela funcionou (CC). O contexto que sobra de quando a skill foi escrita esconde lacunas nas instruções. Sem baseline, não dá para saber se a skill acrescenta algo; a AS diz que, se o agente já faz bem a tarefa sem a skill, a skill talvez não agregue nada.
- **Fonte:** CC (Evaluate and iterate on a skill), AS (Running evals), SC (Step 1), SP (RED phase).
- **Confiança:** confirmado, e também convenção.

### 6.3 Formatos de eval (não são intercambiáveis)

- **AS e SC:** evals/evals.json dentro da pasta da skill, com skill_name e uma lista de evals (id, prompt, expected_output, files e, depois, assertions). Os resultados ficam num workspace irmão (nome-workspace/iteration-N/eval-nome/with_skill e without_skill), com grading.json, timing.json e benchmark.json. Confirmado (AS, CC cita como formato do skill-creator).
- **BP:** outro JSON de exemplo (skills, query, files, expected_behavior), com a observação de que não existe hoje um jeito embutido de rodar esses evals. Confirmado, mas com formato diferente do da AS.
- **claude plugin eval:** para skills distribuídas em plugin. Roda cada prompt isolado com e sem o plugin, usa graders e sai com erro abaixo de um limiar, o que serve para CI. A CC diz com todas as letras que esse formato e o do skill-creator "aren't interchangeable". Confirmado.
- **SP:** pressure scenarios rodados com subagents, sem arquivo de formato fixo; os resultados viram tabela de racionalizações. Relato.
- **MP:** nenhum eval automatizado. O teste é rodar o documento à mão e usar o vocabulário de falhas (duplicação, sediment, no-op) como diagnóstico. Relato.

### 6.4 Assertions e revisão humana

- **O que é:** assertions são afirmações verificáveis sobre a saída ("o arquivo é JSON válido", "o gráfico tem os eixos rotulados"), escritas depois de ver a primeira rodada. A correção exige evidência concreta para dar PASS. O que dá para checar por código vira script. Estilo e qualidade subjetiva ficam para revisão humana, registrada em feedback.json; feedback vazio quer dizer que estava bom.
- **Por que existe:** muitas vezes só se sabe o que é bom depois de ver a saída. Assertion vaga não dá para corrigir, e assertion rígida demais reprova saída certa. Assertions só checam o que alguém pensou em escrever; o humano pega o resto.
- **Fonte:** AS (Writing assertions; Grading; Reviewing results with a human), SC (Step 2; Step 4).
- **Confiança:** confirmado.
- **Relevante para a skill de voz:** o SC diz que skills de saída subjetiva (estilo de escrita, arte) muitas vezes nem precisam de casos de teste, e deixa a decisão com o usuário. A AS diz que essas qualidades devem ser julgadas por um humano, sem forçar assertions.

### 6.5 Testar o gatilho separado da saída

- **O que é:** cerca de 20 queries, 8 a 10 que devem disparar e 8 a 10 que não devem. Os negativos que valem são os near-misses, que dividem palavras-chave com a skill mas pedem outra coisa. Cada query roda umas 3 vezes para medir uma trigger rate, com divisão fixa de 60% treino e 40% validação. A melhor description é escolhida pela validação, não pela última iteração.
- **Por que existe:** o modelo não é determinístico, então uma rodada só engana. Otimizar contra todas as queries faz a description decorar as frases do teste. Negativos óbvios ("escreva um fibonacci" para uma skill de PDF) não testam nada.
- **Fonte:** AS (Optimizing descriptions), SC (Description Optimization; o script run_loop.py automatiza o ciclo e precisa do claude -p), CC (Troubleshooting sugere um grader tool_used: Skill para plugins).
- **Confiança:** confirmado.

### 6.6 Testar conforme o tipo de skill

- **O que é:** o SP testa cada tipo de um jeito. Skills de disciplina: pressure scenarios com três ou mais pressões combinadas (tempo, custo afundado, autoridade, cansaço). Skills de técnica: aplicação e variações. Skills de padrão: reconhecer quando se aplica e quando não. Skills de referência: achar a informação e usá-la certo.
- **Por que existe:** uma skill de disciplina pode passar em perguntas teóricas e falhar quando há pressão para cortar caminho.
- **Fonte:** SP (Testing All Skill Types; testing-skills-with-subagents.md).
- **Confiança:** relato.

### 6.7 Micro-testes de redação

- **O que é:** antes do cenário completo, testar só a redação: uma amostra por chamada em contexto novo, sempre com um controle sem a instrução, 5 ou mais repetições por variante e leitura manual de cada acerto.
- **Por que existe:** cenários completos são lentos e caros. Se o controle não mostra a falha, não há o que corrigir. Variância é métrica: se cinco repetições dão cinco interpretações, a redação não está amarrando o comportamento.
- **Fonte:** SP (Micro-Test Wording Before Full Scenarios).
- **Confiança:** relato.

### 6.8 Testar em todos os modelos previstos

- **O que é:** testar com Haiku (a skill guia o suficiente?), Sonnet e Opus (a skill explica demais?).
- **Por que existe:** a skill complementa o modelo, então o efeito muda com o modelo.
- **Fonte:** BP (Test with all models you plan to use; checklist).
- **Confiança:** confirmado. Nenhuma fonte da comunidade analisada trata disso. Matt Pocock (FAQ do doc) diz que reescrever para cada modelo novo costuma ser só mais uma passada de no-op e que ajustar demais a um modelo é armadilha própria. Relato.

### 6.9 Custo também é resultado

- **O que é:** registrar tokens e tempo de cada rodada e comparar o delta com o ganho em pass rate.
- **Por que existe:** uma skill que melhora 50 pontos e soma 13 segundos é diferente de uma que dobra os tokens para ganhar 2 pontos.
- **Fonte:** AS (Capturing timing data; Aggregating results), SC (Step 3).
- **Confiança:** confirmado.

## 7. Iteração

### 7.1 Claude A escreve, Claude B usa

- **O que é:** uma instância (A) ajuda a escrever e refinar a skill; outra, nova e com a skill carregada (B), faz tarefas reais. O autor observa B e leva o que viu de volta para A.
- **Por que existe:** A entende o que um agente precisa, o humano traz o domínio e B revela as lacunas no uso real, e não em suposições.
- **Fonte:** BP (Develop Skills iteratively with Claude), ENG (Iterate with Claude).
- **Confiança:** confirmado.

### 7.2 Começar de expertise real

- **O que é:** fazer a tarefa de verdade com o agente e extrair da sessão os passos que funcionaram, as correções feitas, os formatos e o contexto que foi preciso dar. Ou sintetizar a skill a partir de material do projeto (runbooks, comentários de review, histórico de correções).
- **Por que existe:** uma skill gerada só com o conhecimento geral do modelo sai genérica ("handle errors appropriately").
- **Fonte:** AS (Start from real expertise), BP (Complete a task without a Skill), CC (criar a skill quando você se pega colando as mesmas instruções várias vezes, ou quando uma seção do CLAUDE.md virou procedimento).
- **Confiança:** confirmado. O AGENTS.md deste repo já adota isso ("only after doing the work by hand a few times").

### 7.3 Ler os transcripts, não só a saída

- **O que é:** olhar o caminho que o agente fez: arquivos lidos fora da ordem, referências ignoradas, um arquivo lido sempre (talvez devesse estar no SKILL.md), arquivo nunca aberto (talvez sobre), passos improdutivos.
- **Por que existe:** os transcripts mostram por que algo deu errado. As causas comuns de desperdício que a AS lista: instrução vaga demais, instrução que não se aplica à tarefa (e que o agente segue mesmo assim) e opções demais sem um padrão.
- **Fonte:** BP (Observe how Claude navigates Skills), AS (Refine with real execution), SC (Keep the prompt lean).
- **Confiança:** confirmado.

### 7.4 Generalizar, enxugar, explicar

- **O que é:** ao corrigir, atacar a causa e não remendar o exemplo; tirar o que não está fazendo diferença; se a taxa de acerto empaca enquanto as regras aumentam, testar remover regras. Se nada funciona, tentar uma formulação estruturalmente diferente em vez de pequenos ajustes.
- **Por que existe:** a skill vai rodar em muitos prompts além dos casos de teste, e skill presa demais aos exemplos não serve.
- **Fonte:** SC (How to think about improvements), AS (Iterating on the skill; The optimization loop).
- **Confiança:** confirmado.

### 7.5 Cada correção vira gotcha

- **O que é:** quando você precisa corrigir o agente, a correção entra na seção de gotchas.
- **Por que existe:** é o caminho mais direto de melhoria contínua.
- **Fonte:** AS (Gotchas sections).
- **Confiança:** confirmado.
- **Paralelo:** o SP faz o mesmo com racionalizações. Cada desculpa nova que o agente usa vira linha na tabela e em red flags, e o teste roda de novo até a skill ficar "bulletproof". Relato.

### 7.6 Quando parar

- **O que é:** quando o usuário está satisfeito, quando o feedback vem vazio ou quando as iterações param de melhorar. Na otimização de description, cinco iterações costumam bastar.
- **Fonte:** SC (The iteration loop), AS.
- **Confiança:** confirmado.
- **Visão de Matt Pocock:** o documento está pronto quando funciona e você não acha mais duplicação, sediment nem no-op. Um sinal de que está funcionando: o documento fica mais curto à medida que melhora. Relato.

### 7.7 Podar sempre

- **O que é:** single source of truth (cada significado num lugar só), checar se cada linha ainda é relevante, caçar no-ops frase por frase e apagar a frase inteira quando ela falha.
- **Por que existe:** sem disciplina de poda, Matt Pocock diz que o destino natural é o sediment: camadas velhas que ficam porque acrescentar parece seguro e remover parece arriscado. Para ele, duplicação é o sinal mais confiável de que o documento nunca foi testado.
- **Fonte:** MP (Pruning).
- **Confiança:** relato. A ideia geral de manter a skill enxuta é confirmada (SC, AS).

## 8. Anti-padrões

| Anti-padrão | Por que é ruim | Fonte | Confiança |
| - | - | - | - |
| Description vaga ("Helps with documents") | não diferencia a skill entre dezenas de outras | BP, SPEC | confirmado |
| Description em primeira ou segunda pessoa | atrapalha a descoberta, porque vai no system prompt | BP, SP | confirmado |
| Description que resume o workflow | o agente segue o resumo e pula o corpo | SP | relato |
| Referências aninhadas | o agente lê aos pedaços e fica com informação incompleta | BP, SPEC | confirmado |
| Explicar o que o modelo já sabe | custa contexto e dilui a atenção | BP, AS, MP, SP | confirmado |
| Muitas opções equivalentes | o agente fica indeciso e testa várias | BP, AS | confirmado |
| Informação com data ("antes de agosto de 2025, use...") | envelhece; o certo é uma seção de padrões antigos | BP | confirmado |
| Terminologia inconsistente | atrapalha o agente a seguir a instrução | BP | confirmado |
| Caminho com barra invertida | quebra em sistemas Unix | BP | confirmado |
| Script que joga o erro para o Claude resolver | o script deve tratar o erro sozinho | BP | confirmado |
| Constantes sem justificativa ("voodoo constants") | se o autor não sabe o valor, o agente também não | BP | confirmado |
| Supor que a dependência está instalada | falha em ambientes sem rede ou sem o pacote | BP | confirmado |
| Nome de ferramenta MCP sem o servidor | "tool not found" quando há vários servidores | BP | confirmado |
| Nome vago (helper, utils) ou palavra reservada (claude, anthropic) | não diz o que a skill faz; palavra reservada é proibida | BP | confirmado |
| ALWAYS e NEVER em caixa alta sem motivo | regra rígida decide mal fora do previsto | SC, AS | confirmado (com a tensão de 4.5) |
| Ajustes que só servem aos casos de teste | a skill falha em prompts novos | SC, AS | confirmado |
| Proibição para corrigir formato de saída | aumenta o conteúdo indesejado | SP, MP | relato |
| Cláusulas de nuance e de exceção | reabrem a negociação; exceção não limita o alcance da regra | SP | relato |
| Exemplo narrativo ("na sessão de 03/10 descobrimos...") | específico demais, não se reaproveita | SP | relato |
| Exemplos em várias linguagens | qualidade mediana e manutenção cara | SP | relato |
| Link com @ para outra skill | carrega o arquivo na hora e queima contexto | SP | relato |
| Criar várias skills em lote sem testar cada uma | equivale a publicar código sem teste | SP | relato |
| Duplicação, sediment, sprawl | custam manutenção e atenção; o documento perde relevância | MP | relato |
| context: fork numa skill só de diretrizes | o subagent recebe diretrizes sem tarefa e não devolve nada útil | CC | confirmado |
| Skill com malware ou intenção escondida | quebra o "principle of lack of surprise" | SC | relato (first-party) |

## 9. Onde as fontes concordam e onde divergem

### Concordam

- **A description dispara a skill e o corpo só entra depois.** Todas as fontes partem disso (SPEC, BP, AS, CC, SC, MP, SP, VL, SW).
- **SKILL.md curto e detalhe em arquivos de um nível**, cada um linkado com a condição de leitura (SPEC, BP, AS, CC, SC, VL; MP pelo conceito de context pointer).
- **Cortar o que o modelo já sabe.** BP ("Claude is already very smart"), AS, CC, MP (no-op), SP (token efficiency).
- **Começar pela falha observada.** BP e ENG (evals primeiro), AS (expertise real), SP (RED antes de GREEN), CC (criar quando você se repete) e o próprio AGENTS.md deste repo.
- **Comparar com e sem a skill, em contexto limpo** (CC, AS, SC, SP). É o ponto de maior convergência entre doc oficial e comunidade.
- **Generalizar em vez de decorar os casos de teste** (SC, AS, MP).
- **Script para o que é determinístico, texto para o que exige julgamento** (BP, AS, VL, SP, CC com hooks).

### Divergem

1. **O que vai na description.** Doc oficial: o que faz e quando usar (BP, SPEC). SP: só quando usar, nunca o processo. SC e AS: ser pushy. MP: podar, um gatilho por branch, sem identidade repetida. O AGENTS.md deste repo segue a forma oficial ("<what it does>. Use when <triggers>.").
2. **Sinônimos na description.** SP pede cobertura de sinônimos e sintomas; MP manda juntar sinônimos num gatilho só. Os dois são relato e se opõem.
3. **Pessoa gramatical.** BP: terceira pessoa. AS: imperativo dirigido ao agente ("Use this skill when..."). Na prática, "Faz X. Use when Y." atende às duas.
4. **Tom: porquê ou ordem.** SC e AS: explicar o porquê, evitar MUST. CC: dizer o que fazer sem narrar como nem por quê. BP: no exemplo, aceita "MUST filter". SP: MUST, Iron Law e tabelas de racionalização para disciplina, receita positiva para formato. MP: positivo sempre, proibição só como guardrail. O SP oferece um critério de conciliação (a forma depende do tipo de falha), mas é relato.
5. **Tamanho.** SPEC e BP: menos de 500 linhas e 5.000 tokens. SP: centenas de palavras. MP: sem número, mas com sprawl como modo de falha.
6. **Formato de eval.** Dentro da própria Anthropic há três: evals.json da AS e do SC, o JSON de exemplo da BP e o claude plugin eval (que a CC declara incompatível com o do SC). O SP usa pressure scenarios; MP não usa eval automatizado.
7. **Evals para skills subjetivas.** SC: muitas vezes dispensáveis, e quem decide é o usuário. AS: revisão humana no lugar de assertions. SP: nenhuma skill sem teste que falhe antes, edições incluídas.
8. **Precisa de uma skill para escrever skills?** BP: o Claude já entende o formato e não precisa de uma skill de escrita de skills. MP (FAQ): pedir ao modelo que escreva a própria skill dá um texto verboso, e a revisão com a referência é onde está o valor. O SC e o SP existem justamente como skills de escrita.
9. **Convenção de projeto é skill?** CC: criar skill quando uma seção do CLAUDE.md virou procedimento. SP: convenção específica de projeto vai no arquivo de instruções, não em skill.
10. **Nomes.** BP prefere gerúndio (processing-pdfs) e aceita substantivo ou ação. As skills da própria Anthropic usam quase todas substantivo (pdf, docx, skill-creator, mcp-builder). SP usa verbo ou gerúndio (writing-plans, systematic-debugging). MP mistura (grilling, diagnosing-bugs, to-spec, triage). VL usa substantivo (react-best-practices, deploy-to-vercel). A SPEC não fala de forma, só de caracteres.
11. **Chamar outra skill.** SP usa um marcador REQUIRED com o nome qualificado; MP usa "Call the Skill tool with X". A doc oficial não trata disso. Todos concordam em não usar caminho.
12. **Testar por modelo.** Só a BP pede para testar com Haiku, Sonnet e Opus; MP alerta contra ajustar demais a um modelo.

## 10. Licença do skill-creator

Fatos verificados em 2026-10-01:

- A pasta [skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) do anthropics/skills tem um LICENSE.txt com o texto completo da **Apache License 2.0** e a linha "Copyright 2026 Anthropic, PBC". A cópia local (marketplace anthropic-agent-skills) tem o mesmo texto.
- O README do repositório diz que muitas skills são open source (Apache 2.0). As de documento (docx, pdf, pptx, xlsx) são "source-available, not open source". O skill-creator não está nesse grupo.
- Não existe arquivo NOTICE na pasta do skill-creator. Na raiz do repo há um THIRD_PARTY_NOTICES.md para componentes de terceiros (imageio e outros), que não fazem parte do skill-creator.

O que a Apache 2.0 permite (seções 2 a 4): reproduzir, criar obras derivadas, exibir, sublicenciar e distribuir o trabalho e as derivadas, com ou sem modificação, inclusive para uso comercial. A permissão é perpétua, mundial, gratuita e irrevogável, e inclui licença de patente (que termina para quem processar alguém alegando violação de patente pelo trabalho).

Condições para redistribuir (seção 4):

1. Entregar a quem recebe uma cópia da licença.
2. Marcar de forma visível os arquivos modificados, dizendo que foram alterados.
3. Manter nos arquivos derivados os avisos de copyright, patente, marca e atribuição do original.
4. Se houver arquivo NOTICE, levar junto os avisos dele (não se aplica aqui, porque não há NOTICE).

Limites: não dá direito de usar nomes ou marcas da Anthropic além do uso razoável para indicar a origem (seção 6), e vem sem garantia (seções 7 e 8). As mudanças próprias podem ter outra licença (fim da seção 4), mas o trecho copiado continua Apache 2.0.

Para este repo (MIT): trechos do skill-creator podem entrar, desde que mantidas as condições acima (cópia da licença, aviso de alteração e atribuição) para esses arquivos. Usar as ideias, descritas com palavras próprias, não depende da licença, e é o que o AGENTS.md já pede para material de terceiros. Isto é leitura do texto da licença, não parecer jurídico; a decisão de copiar ou só referenciar fica para o ticket de desenho.

## 11. Perguntas abertas para o ticket de desenho

Nomes:

- Qual o nome da skill de criação? O AGENTS.md exige gerúndio mais objeto e um nome único fora do repo. Nomes já usados localmente ou na comunidade: skill-creator, writing-skills (SP), writing-for-agents (MP), creating-skills (exemplo do SP).
- A regra de gerúndio do AGENTS.md vale mesmo quando a referência oficial usa substantivo nos próprios nomes?

Escopo:

- A skill de criação encapsula o fluxo inteiro (pesquisa, evals, escrita, checklist da BP) ou orquestra outras skills pelo nome (writing-for-agents, skill-creator, research), conforme o ADR 0002?
- Model-invoked ou user-invoked? Pela leitura de MP, depende de outra skill ou o agente precisar alcançá-la sozinho.
- A description segue a forma oficial ("Faz X. Use when Y.") ou a do SP (só quando usar)? Em que medida entram gatilhos em pt-BR?
- Qual política de tom adotar: explicar o porquê (SC, AS), ordem curta (CC) ou forma conforme o tipo de falha (SP)?
- Copiar trechos do skill-creator (Apache 2.0, com avisos) ou só referenciar pelo nome e descrever com palavras próprias?
- Como tratar campos só do Claude Code (declarar em compatibility, como já diz o AGENTS.md)?

Formato de evals:

- Qual formato usar: evals.json da AS e do SC, o JSON da BP, claude plugin eval (que exige plugin) ou pressure scenarios do SP? São incompatíveis entre si.
- Onde os evals ficam? A AS os põe em evals/ dentro da pasta da skill, mas essa pasta é instalada junto pelo npx skills. Vale verificar se isso é desejável num repo público.
- Como avaliar skills subjetivas (voz, roteiro): só revisão humana com feedback registrado, assertions para as partes objetivas (formato, tamanho, regra de conteúdo público), ou as duas coisas?
- Testar gatilho (20 queries, trigger rate) e saída separadamente para toda skill, ou só para as model-invoked?
- Testar em mais de um modelo, como pede a BP?
- Quantas rodadas por cenário (3 na AS, 5 ou mais nos micro-testes do SP) e quem roda: subagent no Claude Code ou script com claude -p?
