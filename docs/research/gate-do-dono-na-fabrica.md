# Gate do dono na fábrica

Resumo: o gate é um job curto no workflow, sem modelo e sem segredo, que só deixa a run seguir quando três coisas valem no payload do evento `issues: labeled`: o label é `agent:implement`, quem o pôs (`github.event.sender.login`, conferido também contra `github.actor`) é o login do dono, e o autor da issue tem `author_association` igual a `OWNER` ou `COLLABORATOR` (mais `MEMBER` se o repo for de organização). Comentários entram no contexto do agente só filtrados por autor, e o token do agente não ganha ferramenta que leia a thread inteira. Isso protege contra disparo por terceiros e contra issue escrita por estranho; não protege contra comentário injetado se o agente puder buscar a thread sozinho, nem contra o que estiver em código, dependência ou página externa que o agente leia. Interaction limits só existem em repo público e expiram (máximo de 6 meses, sem renovação automática documentada): são apoio, não controle. Pesquisa de 2026-11-10 para o ticket [#105](https://github.com/eusouosalmo/skills/issues/105), mapa [#103](https://github.com/eusouosalmo/skills/issues/103). Fecha a pendência 3 da seção 11.9 de [fabrica-de-software.md](fabrica-de-software.md) e detalha a seção 11.4.

## 1. Fontes

| Sigla | Fonte | Tipo |
| - | - | - |
| HOOK | [Webhook events and payloads](https://docs.github.com/en/webhooks/webhook-events-and-payloads), propriedade `sender` e eventos `issues` e `issue_comment` | primária |
| CTX | [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts), `github.actor`, `github.triggering_actor`, `github.event` | primária |
| EVT | [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), `issues` e `issue_comment` | primária |
| GQL | [GraphQL reference: Issues](https://docs.github.com/en/graphql/reference/issues), enum `CommentAuthorAssociation` | primária |
| REST | [REST: Get an issue](https://docs.github.com/en/rest/issues/issues#get-an-issue), campo `author_association` | primária |
| ROLES | [Repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) | primária |
| PERS | [Permission levels for a personal account repository](https://docs.github.com/en/account-and-profile/reference/permission-levels-for-a-personal-account-repository) | primária |
| LIM | [Limiting interactions in your repository](https://docs.github.com/en/communities/moderating-comments-and-conversations/limiting-interactions-in-your-repository) | primária |
| LIMU | [Limiting interactions for your personal account](https://docs.github.com/en/communities/moderating-comments-and-conversations/limiting-interactions-for-your-personal-account) | primária |
| LIMAPI | [REST: repository interactions](https://docs.github.com/en/rest/interactions/repos) | primária |
| SEC | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) | primária |
| CCA | [claude-code-action: action.yml](https://github.com/anthropics/claude-code-action/blob/main/action.yml) e [docs/security.md](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md), branch `main` em 2026-11-10 | primária |

## 2. Confirmado pela doc

### 2.1 Quem disparou o evento

- **`sender`** é, na maioria dos payloads, o usuário que disparou o evento. Quando o GitHub não consegue resolver um usuário, ele preenche `sender` com a conta placeholder `ghost`, e a doc pede para não supor que `sender` sempre identifica uma pessoa e para tratar o `ghost` em qualquer lógica de segurança (HOOK).
- No evento `issues` com ação `labeled`, o payload traz o objeto `label` (sem descrição na doc) além de `issue` e `sender`. O `issue_comment` traz só `comment` e `issue` como campos próprios (HOOK).
- **`github.actor`** é quem disparou a run inicial; **`github.triggering_actor`** é quem iniciou esta run. Num re-run os dois podem diferir, e o re-run usa os privilégios de `github.actor` (CTX).
- `issues` e `issue_comment` só disparam workflow que exista no branch padrão, e por padrão todas as atividades disparam, então o filtro `types: [labeled]` precisa estar explícito (EVT).
- Eventos causados pelo `GITHUB_TOKEN` não criam runs novas, salvo `workflow_dispatch` e `repository_dispatch` (EVT). Ou seja, quando a fábrica mexe em `agent:in-progress` com o token padrão, isso não redispara nada.

### 2.2 `author_association`

Valores do enum, com o sentido que a doc dá (GQL; o REST lista os mesmos oito valores):

| Valor | Sentido |
| - | - |
| `OWNER` | dono do repositório |
| `MEMBER` | membro da organização dona do repositório |
| `COLLABORATOR` | foi convidado para colaborar no repositório |
| `CONTRIBUTOR` | já fez commit no repositório |
| `FIRST_TIME_CONTRIBUTOR` | nunca fez commit no repositório |
| `FIRST_TIMER` | nunca fez commit no GitHub |
| `MANNEQUIN` | placeholder de usuário não reivindicado |
| `NONE` | sem associação com o repositório |

O campo aparece no objeto `issue` e no objeto `comment` (REST). `CONTRIBUTOR` não serve de filtro: basta um PR mesclado no passado para ganhá-lo.

### 2.3 Quem pode aplicar label

- **Repo de organização:** aplicar e remover label exige Triage, Write, Maintain ou Admin; Read não pode. Criar, editar e apagar label exige Write ou acima (ROLES).
- **Repo de conta pessoal:** só existem dono e colaboradores, e colaborador pode gerenciar labels de issues e PRs (PERS). A doc não fala de quem não é colaborador, mas também não lhe dá papel algum.
- Vale igual para repo público e privado: o que muda num público é que qualquer um lê, abre issue e comenta, não quem aplica label.
- **claude-code-action:** só aceita gatilho de quem tem write access, conferido em eventos de issue, PR, comentário e review. Triage aplica label mas não tem write, então seria barrado. `allowed_non_write_users` contorna essa checagem e a doc chama isso de risco significativo (CCA).

### 2.4 Comentários

- O claude-code-action tem `include_comments_by_actor` (lista de quem pode ter o comentário passado ao Claude; vazio inclui todos) e `exclude_comments_by_actor`; a exclusão vence. A doc recomenda o primeiro em repo público para reduzir entrada não confiável (CCA).
- O action remove comentários HTML, caracteres invisíveis, alt text de imagem, atributos ocultos e entidades HTML, mas avisa que podem surgir técnicas novas de bypass (CCA).
- Texto de evento (título, corpo, comentário) nunca vai direto para `run:`; a forma preferida é passar por variável de ambiente intermediária (SEC).

### 2.5 Interaction limits

- **Só em repo público** (LIM, LIMAPI). Em repo privado não há o recurso, e nem é preciso: só colaboradores enxergam o repo.
- **Grupos:** usuários existentes (barra contas com menos de 24 horas sem contribuição), contribuidores anteriores (barra quem nunca contribuiu para o branch padrão) e colaboradores (barra quem não tem write). Colaboradores ficam isentos dos três (LIM).
- **O que barra:** comentar, abrir issue e criar PR; no nível da conta também reações e edição de comentário e título (LIMU).
- **Durações:** 24 horas, 3 dias, 1 semana, 1 mês ou 6 meses; na API, `one_day` (padrão), `three_days`, `one_week`, `one_month`, `six_months`, e a resposta traz `expires_at` (LIM, LIMAPI).
- **Expiração:** passado o prazo, a atividade volta ao normal. A doc não fala de renovação automática nem de estender um limite ativo (LIM, LIMAPI).
- **Nível da conta:** um limite na conta pessoal vale para todos os repos públicos dela e, enquanto estiver ativo, o limite por repo não pode ser mudado; a API responde 409 (LIMU, LIMAPI).
- Mudar o limite pela API exige owner ou admin (LIMAPI).

## 3. Desenho do gate (inferência sobre a doc)

1. **Job `gate` antes do job do agente**, com `permissions: {}` ou só `issues: read`, sem segredo da Anthropic e sem checkout. O job do agente usa `needs: gate`. Assim, se a condição falhar, nada com credencial chega a rodar.
2. **Condição, toda lida do payload, nada do texto:**
   - `github.event.action == 'labeled'` e `github.event.label.name == 'agent:implement'`;
   - `github.event.sender.login` igual ao login do dono, e igual a `github.actor`; se algum dos dois for `ghost`, recusa;
   - `github.event.issue.author_association` em `OWNER` ou `COLLABORATOR` (e `MEMBER` em repo de organização);
   - a issue já tem `ready-for-agent` (regra do mapa #103), conferida em `github.event.issue.labels`.
   O login do dono fica numa variável do repo (`vars`), não em segredo, para a mesma regra servir a outro repo. Em repo de conta pessoal, `github.repository_owner` também serve, mas o mesmo workflow em repo de organização daria o nome da org, por isso a variável.
3. **Re-run.** Um re-run reaproveita o payload original e roda com os privilégios de `github.actor` (CTX). Re-run já exige write access, então não abre porta nova; o gate pode registrar `github.triggering_actor` no log e recusar se ele não for o dono, para manter a regra literal.
4. **Snapshot do texto.** O payload guarda a issue como estava no momento do label. O agente deve trabalhar com o corpo desse payload, gravado em arquivo pelo gate, e não buscar a issue de novo: assim uma edição feita depois do label não entra na run. Como só o autor e quem tem acesso de escrita editam a issue, e o autor já passou pelo filtro, o ganho é pequeno, mas o custo também.
5. **Comentários.** `include_comments_by_actor` com o login do dono (e, se quiser, colaboradores nomeados). Se o agente roda com `claude -p` em vez do action, o gate monta o contexto com a API e filtra por `comment.author_association` ou por login, e o agente não recebe `gh issue view --comments` nem o MCP do GitHub com leitura de comentários. O filtro do action vale para o que ele passa no prompt; se o agente tiver uma ferramenta que leia a thread, ele lê tudo de novo. Essa última frase é inferência, não está na doc.

## 4. O que protege e o que não protege

### 4.1 Perfil `github`, repo público

**Protege:**

- Disparo por terceiros: quem não é colaborador não aplica label (ROLES, PERS), e o gate ainda exige que o `sender` seja o dono, o que barra também colaboradores e bots.
- Issue escrita por estranho: o filtro de `author_association` recusa `NONE`, `CONTRIBUTOR` e os demais antes do modelo rodar.
- Comentário de estranho no prompt: barrado pelo filtro por autor, desde que o agente não tenha como buscar a thread.
- Segredo exposto por run não autorizada: o job do agente nem começa.

**Não protege:**

- Prompt injection que vem de outro lugar: código e dependências do repo, páginas que o agente busca, saída de comando. O gate controla quem dispara, não o que o agente lê depois.
- Erro do próprio dono: label posto numa issue que cita texto de terceiro, ou que linka algo externo.
- Log público: em repo público o log do Actions é visível; o gate não esconde o que o agente imprime (seção 11.3 da nota principal).
- Ruído: interaction limits seguram spam de issue e comentário por até 6 meses, mas expiram; renovar é tarefa manual ou de um workflow agendado que chame a API (inferência; a doc não documenta renovação). O gate não depende deles.

### 4.2 Perfil `local`

- Em repo público o perfil é recusado (seção 11.3 da nota principal, a partir do aviso do GitHub de que self-hosted quase nunca deve servir a repo público, SEC). A pergunta só existe em repo privado.
- **Repo privado:** só colaboradores leem, abrem issue, comentam e aplicam label, e interaction limits não existem. O gate continua útil como regra explícita (só o dono dispara, mesmo com outros colaboradores), e é ainda mais importante aqui porque a máquina não é descartável: uma run indevida roda no PC do usuário, e self-hosted pode ficar comprometido de forma persistente por código não confiável (SEC). O gate não substitui o isolamento da `factory-runner` (usuário próprio, container por run).
- O que não protege é o mesmo do perfil `github`, mais o fato de que tudo que o agente executar fica na máquina do usuário se o isolamento falhar.

## 5. Lacunas

- A doc não diz se um limite de interação ativo pode ser estendido nem se um novo `PUT` substitui o anterior; testar antes de automatizar a renovação.
- `COLLABORATOR` é descrito como "foi convidado"; a doc não diz se um convite pendente já conta. Com o gate exigindo o dono no `sender`, isso só afeta o autor da issue.
- A doc do webhook não descreve o campo `label` do evento `labeled`; o uso de `github.event.label.name` é o que os exemplos da comunidade fazem, a conferir no primeiro teste.
