# Exemplos

Fala real do eusouosalmo, de vídeos publicados. A edição foi mínima: erros da transcrição automática corrigidos, muletas cortadas, travessões trocados por ponto ou vírgula, nomes de pessoas e dados pessoais removidos. Os exemplos mostram a mecânica da voz; o assunto de cada um não é repertório a repetir.

Só há exemplos do registro falado. O registro escrito ganha exemplo quando existir texto real publicado.

## Sumário

- [Abertura com cena](#abertura-com-cena)
- [Metáfora que explica](#metáfora-que-explica)
- [Erro real com número real](#erro-real-com-número-real)
- [Analogia que ancora uma opinião](#analogia-que-ancora-uma-opinião)
- [Bordões no lugar certo](#bordões-no-lugar-certo)
- [Roteiro inteiro: explicando uma ferramenta](#roteiro-inteiro-explicando-uma-ferramenta)
- [Roteiro inteiro: resposta a seguidor](#roteiro-inteiro-resposta-a-seguidor)
- [Anti-exemplos](#anti-exemplos)

## Abertura com cena

Vídeo piloto do YouTube.

> Macho, bora lá. Eu tava aqui outro dia fazendo o almoço e daí me veio uma ideia na cabeça que eu nunca mais consegui tirar. Eu tive muitas ideias e nunca executei nenhuma delas.

A cena (fazendo o almoço) vem antes da ideia. O bordão abre, uma vez.

## Metáfora que explica

Vídeo piloto. A metáfora volta no fim do vídeo e, quando volta, explica o termo para quem não é dev.

> E aí eu comecei a pensar na vida como se ela fosse um git graph. Sabe aquele gráfico de branch do teu projeto, onde cada decisão é uma branch nova? E aí eu percebi que na vida tiveram várias branches que eu deixei de criar.

> Eu não sei se tu sabe como funciona o Git, mas uma branch só passa a existir se tu criar ela. E ela só avança se tu der o primeiro commit.

## Erro real com número real

Vídeo piloto. O erro é contado sem disfarce, com o tempo que custou.

> No primeiro teste, o drone deu um 180 e se espatifou no chão. Foi hélice para tudo que era lado. E aí, sabe qual era o problema? Eu tinha invertido os fios do motor. E o pior é que eu só fui descobrir isso três meses depois, porque pedi mais hélices da China, que era mais barato, e fiquei esperando esse tempo todo para chegar.

## Analogia que ancora uma opinião

Reel respondendo se é sustentável as empresas darem tanta IA de graça. A opinião vem com número (vinte dólares) e com um caso que o público já viveu (Uber e 99).

> De maneira direta: não é sustentável no longo prazo. O que a gente paga hoje, algo em torno de vinte dólares no plano mais barato, não cobre o custo real de uma GPU rodando num data center. O que tá rolando é subsídio. As big techs têm vários investidores e queimam bilhões de dólares para a gente criar o hábito de usar IA. É muito parecido com Uber e 99: assim que lançaram, a corrida era praticamente de graça. Hoje a gente paga.
>
> Então o cara aproveita essa festa aí enquanto pode, aproveita para aprender e construir, mas sabendo que uma hora ou outra a conta vai chegar.

## Bordões no lugar certo

Reel sobre usar agentes orientados a spec. Cada bordão aparece uma vez, numa virada da fala.

> E a quarta etapa é, antes de qualquer commit, revisar tudo que foi implementado. Se está de acordo com os contratos, se faz sentido no contexto. Tudo certo? É só mandar a bala.
>
> Aí, só para dar nome aos bois: esse fluxo é um conjunto de skills criado por um engenheiro de software.

## Roteiro inteiro: explicando uma ferramenta

O roteiro mais trabalhado nas palavras do próprio eusouosalmo: a referência principal da voz. Texto do roteiro, gravado e publicado (a transcrição distorce os nomes técnicos). Explica dentro de um exemplo concreto (o jogo), separa o que a empresa diz do que está provado e fecha com uma pergunta.

> Essa IA joga Doom em tempo real. E não sabe escrever uma frase.
>
> Ela se chama Jev, da Typesafe AI. O fundador é um ex-pesquisador da OpenAI que diz ter co-inventado o ChatGPT. E o Jev não conversa. Ele só decide.
>
> Pensa num jogo. A cada instante, o código precisa decidir: atirar, desviar, abrir a porta. Se tu pergunta isso pra uma LLM, ela escreve um textão. E o teu código precisa achar a decisão no meio dele. É lento e é caro. E ainda tem outro problema: às vezes a LLM inventa uma opção que nem existe, ou quebra o formato. É pra isso que existe o structured output.
>
> O Jev pula essa etapa. Tu entrega o estado do jogo e as opções possíveis, e ele devolve só a decisão, com a probabilidade. Tipo assim: "atirar, 92%".
>
> Segundo a empresa, isso é de 40 a 200 vezes mais rápido. É por isso que dá pra decidir 10 vezes por segundo no Doom, por uns 7 dólares a hora.
>
> E não é só jogo. Pra quem programa, é um if inteligente: classificar um ticket de suporte, decidir se uma resposta precisa de um modelo maior, escolher em qual botão clicar. O código continua sendo teu. Tu define as opções e o que fazer com aquele 92%.
>
> Mas calma. A empresa diz que o Jev não alucina. Isso quer dizer que ele nunca inventa uma opção fora da lista e o formato nunca quebra. Não quer dizer que ele sempre acerta. Ele ainda pode mandar atirar na hora errada. E até agora, não tem paper. Os testes foram feitos pela própria empresa.
>
> E aí, qual decisão do teu software tu passaria pra uma IA que responde quase instantaneamente?

## Roteiro inteiro: resposta a seguidor

Texto escrito para ser falado, gravado e publicado. Começa pela resposta, conta a história de uma noite, explica o termo técnico (teste que falha primeiro) e fecha pedindo a experiência de quem assiste.

> Pergunta: modo em loop funciona bem em desenvolvimento com specs SDD?
>
> Macho, funciona bem... mas não é o loop em si que resolve o problema. É o que vem antes dele e o que vem depois.
>
> Pra contextualizar: de domingo pra segunda, eu tava cansado mas queria fechar um escopo que eu tava codando. Já tinha usado a skill de grill nesse problema, que é pedir para a inteligência artificial me entrevistar com perguntas criadas a partir de vários ângulos do contexto do problema. Depois rodei as skills que transformam nosso contexto em especificações, e então faltava só codar.
>
> Aí pensei: e se o Claude codasse sozinho enquanto eu dormia? Foi aí que rodei um loop estilo Ralph, mas com duas travas. Primeiro: ele não podia commitar nada. Bloqueei git de escrita, para que eu pudesse revisar de maneira mais fácil.
>
> A segunda trava: cada etapa só virava concluída se passasse nos testes que eu mandei ele criar, e o teste precisava falhar primeiro, antes do código existir. Só depois ele codava até o teste passar. E o porquê disso é que se o teste já passa antes de tu escrever qualquer código, ele não presta, pois não está testando nada. É um teste furado, que vai passar sempre, independente do que tu escreva. Isso daí é o TDD clássico. E ainda tem um segundo Claude, com o contexto limpo, revisando o diff atrás dele antes do próximo ciclo pegar a próxima etapa.
>
> Na prática, o checklist morava na própria etapa. Já vinha com os critérios escritos, e só virava concluída quando os testes batiam com eles.
>
> Foi assim que funcionou aqui. Se tu já tá testando algo parecido, me manda como ficou o teu.

## Anti-exemplos

Trechos de rascunhos escritos sem esta skill, a partir das mesmas anotações dos roteiros acima, ao lado do que foi de fato gravado.

| Rascunho | Gravado |
|---|---|
| "Funciona. Mas o loop sozinho não resolve nada: o que importa é o que vem antes e o que vem depois dele." | "Macho, funciona bem... mas não é o loop em si que resolve o problema. É o que vem antes dele e o que vem depois." |
| "E você, já testou algo parecido? Conta aqui nos comentários como ficou." | "Se tu já tá testando algo parecido, me manda como ficou o teu." |
| Blocos com rótulo e minutagem: "Trava 1", "(25 a 50s)", "Texto na tela: grill, specs, etapas" | A história de uma noite, contada em sequência |
| "E antes do próximo ciclo, um segundo Claude, com o contexto limpo, revisa o diff. Ele não tem o viés de quem escreveu o código." (a segunda frase não estava nas anotações) | "E ainda tem um segundo Claude, com o contexto limpo, revisando o diff atrás dele antes do próximo ciclo pegar a próxima etapa." |
