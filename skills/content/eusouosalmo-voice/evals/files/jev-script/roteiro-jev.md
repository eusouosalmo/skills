Essa IA joga Doom em tempo real. E não sabe escrever uma frase.

Ela se chama Jev, da Typesafe AI. O fundador é um ex-pesquisador da OpenAI que diz ter co-inventado o ChatGPT. E o Jev não conversa. Ele só decide.

Pensa num jogo. A cada instante, o código precisa decidir: atirar, desviar, abrir a porta. Se tu pergunta isso pra uma LLM, ela escreve um textão. E o teu código precisa achar a decisão no meio dele. É lento e é caro. E ainda tem outro problema: às vezes a LLM inventa uma opção que nem existe, ou quebra o formato. É pra isso que existe o structured output.
O Jev pula essa etapa. Tu entrega o estado do jogo e as opções possíveis, e ele devolve só a decisão, com a probabilidade. Tipo assim: "atirar, 92%". Nada de texto.
Segundo a empresa, isso é de 40 a 200 vezes mais rápido. É por isso que dá pra decidir 10 vezes por segundo no Doom, por uns 7 dólares a hora.

E não é só jogo. Pra quem programa, é um if inteligente: classificar um ticket de suporte, decidir se uma resposta precisa de um modelo maior, escolher em qual botão clicar. O código continua sendo teu. Tu define as opções e o que fazer com aquele 92%.

Mas calma. A empresa diz que o Jev não alucina. Isso quer dizer que ele nunca inventa uma opção fora da lista e o formato nunca quebra. Não quer dizer que ele sempre acerta. Ele ainda pode mandar atirar na hora errada. E até agora, não tem paper. Os testes foram feitos pela própria empresa.

E aí, qual decisão do teu software tu passaria pra uma IA que responde quase instantaneamente?
