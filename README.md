# Skills do eusouosalmo

Skills que ensinam o seu agente de IA (Claude Code, Codex, Cursor e outros) a fazer bem dois trabalhos: criar e proteger o código de um projeto com IA, e produzir vídeo curto do roteiro ao reel pronto.

Cada skill nasceu de um trabalho que eu fiz na mão algumas vezes, e é testada contra o mesmo agente sem ela: só fica o que muda o resultado.

[Read in English](README.en.md)

## Começar em três passos

1. Instale:

   ```bash
   npx skills@latest add eusouosalmo/skills
   ```

   O instalador pergunta quais skills e em quais agentes. Prefere o plugin do Claude Code, que é versionado? Veja [outras formas de instalar](#outras-formas-de-instalar).

2. Vai usar as skills de reel? Rode `/setup-eusouosalmo-skills` uma vez. Ela acha as suas pastas (reels, roteiros, estilo, CapCut) e guarda os caminhos, para nenhuma skill perguntar de novo.

3. Peça em linguagem normal. O agente escolhe a skill pelo pedido:

   - "escreve um roteiro de reel sobre índice no Postgres a partir dessas notas"
   - "corta os brutos da pasta desse reel e tira as tomadas ruins"
   - "o agente esqueceu de novo de rodar os testes, transforma isso numa skill"

## Skills

### Vídeo curto, do roteiro ao post

Na ordem em que entram num reel. Todas entregam o resultado em português.

1. [reel-script](skills/content/reel-script/SKILL.md) (beta): escreve o roteiro a partir das suas anotações, com gancho, um CTA falado, texto de teleprompter cronometrado e os prints das fontes para a edição.
2. [reel-cut](skills/content/reel-cut/SKILL.md) (beta): junta os brutos num corte seco, escolhendo a tomada de cada fala e tirando bastidor e pausas longas, com uma tabela de tomadas aprovada antes do render.
3. [reel-motion](skills/content/reel-motion/SKILL.md) (beta): decide quais trechos viram animação e renderiza as cenas e os overlays de adesivos, sincronizados com cada palavra falada.
4. [reel-finish](skills/content/reel-finish/SKILL.md) (draft): monta o reel pronto, como projeto do CapCut ou como mp4 final sem CapCut, com legenda, sons, punch-ins e tela dividida no estilo de um projeto seu.
5. [post-caption](skills/content/post-caption/SKILL.md) (draft): escreve a legenda do post para Instagram, TikTok, YouTube Shorts ou LinkedIn, com um pedido, crédito da fonte e hashtags dentro do limite da plataforma.

E as que trabalham em volta dessa sequência:

- [reel-edit](skills/content/reel-edit/SKILL.md) (draft): faz a edição inteira, dos brutos ao reel pronto, chamando reel-cut, reel-motion e reel-finish em ordem, com a sua aprovação entre elas.
- [eusouosalmo-voice](skills/content/eusouosalmo-voice/SKILL.md) (draft): escreve e revisa texto na minha voz, falada ou escrita conforme o canal. Serve de modelo para criar a skill da sua voz.
- [setup-eusouosalmo-skills](skills/content/setup-eusouosalmo-skills/SKILL.md) (beta): configura o kit numa máquina uma vez, achando as pastas e os arquivos que as skills leem.

### Engenharia com IA

- [skill-forge](skills/harness/skill-forge/SKILL.md) (beta): cria ou corrige uma skill a partir de uma falha que você viu acontecer, conferida com evals contra o agente sem a skill.
- [git-guardrails](skills/harness/git-guardrails/SKILL.md) (draft): instala, por projeto, um hook que impede o agente de rodar git destrutivo, com perfis interativo e AFK.

**Status:** `beta` e `stable` são instaladas pelos dois caminhos. `draft` ainda está em teste e fica só no repositório, para ler ou copiar.

## Por que estas skills

Gerar código ficou barato. O que ainda diferencia um software é a engenharia em volta: arquitetura, testes e o harness que mantém o agente nos trilhos. Com conteúdo é igual: o agente escreve um roteiro em segundos, mas ele sai genérico, com fato sem fonte e gancho fraco.

Uma skill aqui é o que eu aprendi corrigindo o agente, escrito para ele não errar de novo. Elas são pequenas e combináveis: leia, faça fork e adapte para a sua stack e a sua voz.

Eu mostro como construo com IA no [Instagram](https://www.instagram.com/eusouosalmo/), no [YouTube](https://www.youtube.com/@eusouosalmo) e em [eusouosalmo.dev](https://eusouosalmo.dev).

## Outras formas de instalar

Há dois caminhos. Escolha um: a mesma skill instalada pelos dois carrega duas vezes, uma como `<nome>` e outra como `eusouosalmo-skills:<nome>`.

<details>
<summary>npx skills, para qualquer agente (sem versão)</summary>

Instala e atualiza a partir do último commit do `main`. Para uma skill só, acrescente `--skill <nome>`. Para atualizar ou remover:

```bash
npx skills@latest update
npx skills@latest remove <nome>
```

</details>

<details>
<summary>Plugin do Claude Code (versionado)</summary>

Você fica numa release até atualizar. Cada release e o changelog dela estão em [Releases](https://github.com/eusouosalmo/skills/releases).

```bash
claude plugin marketplace add eusouosalmo/skills
claude plugin install eusouosalmo-skills@eusouosalmo
```

As skills aparecem como `eusouosalmo-skills:<nome>`. Para atualizar, atualize o marketplace e depois o plugin (ou ligue a atualização automática do `eusouosalmo` em `/plugin`, Marketplaces):

```bash
claude plugin marketplace update eusouosalmo
claude plugin update eusouosalmo-skills@eusouosalmo
```

Para remover o plugin, ou o marketplace junto com o plugin:

```bash
claude plugin uninstall eusouosalmo-skills@eusouosalmo
claude plugin marketplace remove eusouosalmo
```

</details>

## Como o repositório funciona

Toda skill segue a [especificação Agent Skills](https://agentskills.io/specification). As instruções são escritas em inglês; as skills de conteúdo entregam o resultado em português. As convenções (nomes, maturidade, língua) estão no [AGENTS.md](AGENTS.md), e o porquê de cada uma em [docs/adr](docs/adr). A estrutura deve muito às [skills do Matt Pocock](https://github.com/mattpocock/skills).

## Licença

[MIT](LICENSE)
