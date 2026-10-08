# O que separa arquitetura de design de software

Resumo: nenhuma fonte primária trata arquitetura e design como coisas de natureza diferente. Todas dizem, cada uma com suas palavras, que arquitetura é um tipo de design; a briga é sobre onde fica a linha e quem a traça. Robert C. Martin diz que não há linha nenhuma, é tudo um contínuo. Martin Fowler, citando Ralph Johnson, diz que a linha é social: arquitetura é o que os desenvolvedores experientes consideram importante. Mark Richards e Neal Ford dizem que é um espectro, e dão critérios para posicionar cada decisão nele. O SEI e a ISO/IEC/IEEE 42010 dão critérios mais objetivos: arquitetura é o que é fundamental e visível de fora dos elementos; o detalhe privado de um elemento é design ou implementação. O ponto em que quase todos convergem é o custo de mudar: quanto mais cara e mais espalhada a consequência de uma decisão, mais ela é arquitetura. Pesquisa de 2026-10-08 para o ticket [#29](https://github.com/eusouosalmo/skills/issues/29) (parte do #17).

## 1. Fontes

| Sigla | Fonte | Tipo |
| - | - | - |
| WNA | Martin Fowler, [Who Needs an Architect?](https://martinfowler.com/ieeeSoftware/whoNeedsArchitect.pdf), coluna Design da IEEE Software, julho/agosto de 2003 | primária |
| MFG | Martin Fowler, [Software Architecture Guide](https://martinfowler.com/architecture/) | primária |
| SAM | Mark Richards, [Software Architecture Monday, lição 167: Architecture vs. Design](https://www.developertoarchitect.com/lessons/lesson167.html), 14/08/2023 (vídeo; li a transcrição automática do YouTube) | primária |
| FSA | Mark Richards e Neal Ford, Fundamentals of Software Architecture (O'Reilly, 1a ed. 2020), cap. 2, seção "Architecture Versus Design" | primária (livro pago, só paráfrase) |
| HFSA | Raju Gandhi, Mark Richards e Neal Ford, Head First Software Architecture (O'Reilly, 2024), cap. 1 | primária (livro pago; conferido só por trechos citados em terceiros) |
| CA | Robert C. Martin, Clean Architecture (Prentice Hall, 2017), cap. 1 "What Is Design and Architecture?" (p. 3 e 4) e cap. 15 "What Is Architecture?" | primária (livro pago, só paráfrase, de memória da leitura) |
| SCR | Robert C. Martin, [Screaming Architecture](https://blog.cleancoder.com/uncle-bob/2011/09/30/Screaming-Architecture.html), blog, 30/09/2011 | primária |
| UBV | Robert C. Martin, [What is the goal of software architecture?](https://www.youtube.com/watch?v=p0pVSNhCFak), trecho de palestra republicado por terceiro (canal Dev Tools Made Simple) | primária (fala do autor; corte de terceiro, palestra de origem não identificada) |
| SEI | SEI/Carnegie Mellon, [What is your definition of software architecture?](https://www.sei.cmu.edu/library/what-is-your-definition-of-software-architecture/) ([PDF](https://www.sei.cmu.edu/documents/2544/2010_010_001_513810.pdf)): definições de Software Architecture in Practice (Bass, Clements, Kazman), Documenting Software Architectures (Clements et al.), Garlan e Shaw, Perry e Wolf | primária |
| ISO | [ISO/IEC/IEEE 42010, Defining architecture](http://www.iso-architecture.org/42010/defining-architecture.html), site mantido pelos editores da norma: definição da edição 2011 e comentário | primária (o texto da norma é pago; o site é dos editores) |
| EDN | Amnon H. Eden, [The Locality Criterion: Defining Software Architecture](https://eden-study.org/?p=2380), palestra ao ISO/IEC JTC1/SC7/WG42, 11/11/2024; e [Strategic Versus Tactical Design](https://eden-study.org/?p=1468), HICSS 2005 | primária (resumos nas páginas do autor; não li os artigos completos) |
| BCH | Grady Booch, post "On design" (blog no IBM developerWorks, 2006), reproduzido em Buschmann, Henney e Schmidt, Pattern-Oriented Software Architecture vol. 5 (2007), p. 214 | secundária: o original saiu do ar e não consegui abrir uma cópia arquivada |

## 2. O que cada fonte diz

### Robert C. Martin (CA, SCR, UBV)

- **Não há diferença.** No cap. 1 de Clean Architecture, Martin diz que a separação usual (arquitetura como o alto nível, design como o detalhe) não se sustenta: os detalhes de baixo nível e a estrutura de alto nível fazem parte do mesmo todo, sem uma linha clara entre eles. Usa a analogia da planta de uma casa, que mostra tanto a forma geral quanto onde vai cada tomada (CA, p. 3 e 4).
- **Um objetivo só para os dois.** O objetivo da arquitetura é reduzir o esforço humano necessário para construir e manter o sistema; a qualidade do design se mede pelo esforço para atender o cliente, e se esse esforço cresce com o tempo, "the design and the architecture are bad" (UBV, mesma ideia do cap. 1 de CA). Ele usa as duas palavras juntas, como uma coisa só.
- **Arquitetura é adiar decisão.** Banco de dados, web e frameworks são detalhes; uma boa arquitetura deixa essas escolhas para depois e mostra os casos de uso do sistema, não as ferramentas (SCR; desenvolvido no cap. 15 de CA, onde o arquiteto continua programando e a meta é manter opções abertas pelo maior tempo possível).

### Martin Fowler e Ralph Johnson (WNA, MFG)

- **Arquitetura é o que o time acha importante.** Fowler começa com uma provocação: arquitetura é a palavra que se usa quando se quer falar de design e fazê-lo parecer importante. Depois adota a definição de Johnson: arquitetura é o entendimento compartilhado que os desenvolvedores experientes têm do design do sistema, e um componente é significativo "because the expert developers say so" (WNA). É uma construção social.
- **O mesmo item muda de lado conforme o sistema.** Exemplo de Johnson: numa aplicação corporativa, a persistência no Oracle entra no desenho da arquitetura; num sistema de imagens médicas, o mesmo Oracle não entra, porque a complexidade está em analisar as imagens, não em guardá-las (WNA).
- **Rejeita "decisão tomada cedo".** Johnson diz que arquitetura são as decisões que você gostaria de acertar cedo, não as que são tomadas cedo; e você não tem mais chance de acertá-las do que qualquer outra. Fowler conclui: arquitetura são as coisas que as pessoas percebem como difíceis de mudar (WNA).
- **O arquiteto deve eliminar arquitetura.** Se arquitetura é o que é difícil de mudar, tornar algo fácil de mudar tira esse algo da arquitetura. O exemplo é o esquema do banco: com migrações evolutivas, ele deixou de ser arquitetural. Uma das tarefas mais importantes do arquiteto é remover irreversibilidade (WNA).
- **Arquitetura e programação andam juntas.** Fowler desconfia do termo justamente porque sugere uma separação da programação; boa arquitetura está "deeply intertwined with programming" (MFG).

### Mark Richards e Neal Ford (SAM, FSA, HFSA)

- **Há diferença, mas é um espectro, não uma escolha binária.** Richards dá quatro critérios para posicionar uma decisão (SAM):
  1. Mexe na estrutura do sistema (componentes, acoplamento entre eles, unidades de deploy, comunicação, bancos) ou só no código-fonte?
  2. É estratégica ou tática? Teste prático: quantas pessoas participam e quanto tempo leva para decidir. Estratégica envolve muita gente e semanas ou meses; tática, uma ou duas pessoas em uma hora ou um dia.
  3. Quanto esforço exige para construir ou mudar?
  4. Os trade-offs são significativos ou pequenos?
- **Exemplos dele:** adotar microsserviços fica no extremo da arquitetura; usar o padrão Strategy numa parte do código fica no extremo do design; quebrar o serviço de pagamento em um serviço por meio de pagamento cai no meio, puxando para arquitetura, e é onde mora a maior parte das decisões reais (SAM).
- **Por que importa:** decide quem tem a responsabilidade final pela decisão (arquiteto ou time de desenvolvimento, sempre depois de colaborar) e indica o impacto da decisão (SAM).
- **No livro de 2020:** a seção "Architecture Versus Design" do cap. 2 critica o modelo tradicional, em que o arquiteto decide e entrega para o time implementar numa via de mão única, e defende arquiteto e desenvolvedores no mesmo time, com comunicação nos dois sentidos (FSA). O Head First, de 2024, traz o espectro estratégico e tático com uma analogia de casa: o tamanho da casa condiciona os cômodos, a luminária não condiciona a mesa (HFSA, conferido por citações).

### SEI (SEI)

- **Arquitetura é um nível de design.** Garlan e Shaw chamam de "the software architecture level of design" os problemas que vão além de algoritmos e estruturas de dados: organização geral, protocolos de comunicação, distribuição física, escala e desempenho. Perry e Wolf escrevem "architectural (or, if you will, design) elements" (SEI).
- **O critério é a interface.** Em Software Architecture in Practice, arquitetura são as estruturas do sistema, seus elementos, as propriedades visíveis de fora desses elementos e as relações entre eles. "Visível de fora" é o que um elemento pode supor de outro: serviços oferecidos, desempenho, tratamento de falhas. A arquitetura cuida do lado público da interface; os detalhes privados, que dizem respeito só à implementação interna, não são arquiteturais (SEI).
- **Todo sistema tem arquitetura**, boa ou ruim, documentada ou não (SEI).

### ISO/IEC/IEEE 42010 (ISO)

- **Definição da edição 2011:** arquitetura são os conceitos ou propriedades fundamentais de um sistema no seu ambiente, expressos nos seus elementos, nas relações e nos princípios do seu design e evolução. Ou seja, não tudo sobre o sistema, só o essencial, e a definição contém a palavra design: arquitetura inclui os princípios que governam o design (ISO).
- **Arquitetura não é documento.** A norma separa a arquitetura (abstrata) da descrição de arquitetura (o artefato). Confundir as duas é comum (ISO).
- **Fora contra dentro:** o comentário dos editores registra uma diferença muito citada: arquitetura olha para fora, o sistema no seu ambiente; design olha para dentro, depois que as fronteiras do sistema estão definidas (ISO).

### Amnon Eden (EDN)

- **Critério formal de localidade.** Uma afirmação é local se continua verdadeira quando o programa cresce. Afirmações arquiteturais são não locais: o sistema pode violá-las só por crescer. Escolha de paradigma, estilo arquitetural ou framework é estratégica e não local, e deve ser feita cedo; padrão de projeto, refatoração e idioma de linguagem são táticos e locais, e podem esperar (EDN).
- Eden apresentou o critério em 2024 ao grupo da ISO que escreve a 42024 (fundamentos de arquitetura), em apoio à distinção entre arquitetura e design que essa norma faz (EDN).

### Grady Booch (BCH, não verificado no original)

- A frase mais repetida sobre o tema é atribuída a ele: toda arquitetura é design, mas nem todo design é arquitetura; arquitetura são as decisões de design significativas, e o significado se mede pelo custo de mudar (BCH). Só consegui confirmar pela reprodução em terceiros; o post original não abriu.

## 3. Onde concordam (confirmado)

- **Arquitetura é design.** SEI (Garlan e Shaw, Perry e Wolf), ISO (princípios de design dentro da definição), Martin (contínuo), Fowler (design "inflado"), Richards (espectro) e, segundo as reproduções, Booch. Nenhuma fonte trata como duas atividades de natureza diferente.
- **Não é tudo; é o fundamental.** ISO ("não necessariamente tudo, mas o essencial"), SEI (detalhe privado não é arquitetura), Fowler (o importante), Richards (o extremo estratégico do espectro).
- **Custo de mudança como sinal.** Fowler (difícil de mudar), Richards (esforço e trade-offs), Martin (esforço para manter), Eden (afirmação que quebra com o crescimento), Booch (custo de mudar, não verificado).

## 4. Onde discordam (confirmado)

| Questão | Posições |
| - | - |
| Existe fronteira? | Martin: não, é um contínuo (CA). Richards: sim, mas gradual (SAM). SEI, ISO e Eden: sim, com critério definido (interface pública, ambiente, localidade). |
| O critério é objetivo ou social? | Objetivo: SEI (visível de fora), ISO (fundamental, voltado para o ambiente), Eden (localidade). Social: Johnson e Fowler, é o que os experientes acham importante, e o mesmo banco pode ser arquitetura num sistema e não no outro (WNA). |
| Decidir cedo ou tarde? | Eden: decisões estratégicas devem ser tomadas cedo (EDN). Johnson: "cedo" não define nada, você não acerta mais por decidir antes (WNA). Martin: adiar banco, web e framework é o próprio trabalho da arquitetura (SCR, CA). Fowler: melhor ainda é tornar a decisão barata de mudar, e ela deixa de ser arquitetura (WNA). |
| Quem decide? | Richards: o arquiteto responde pelo lado da arquitetura, o time pelo lado do design (SAM). Fowler: o arquiteto é um guia que forma o time; seu valor é inversamente proporcional ao número de decisões que toma (WNA). Martin: o arquiteto é um programador que continua programando (CA, cap. 15). |

## 5. Inferências

- **Por que eusouosalmo não achou a diferença clara nos dois livros:** porque os dois livros respondem a perguntas diferentes. Clean Architecture nega a fronteira para defender que o mesmo cuidado vale do método à camada; Fundamentals mantém a fronteira para responder quem decide. Lidos juntos, parecem se contradizer; na verdade, um fala do objetivo, o outro da responsabilidade. Inferência minha, a partir de CA e SAM.
- **A fronteira se move.** Juntando Fowler (tornar fácil de mudar tira da arquitetura) e Johnson (o mesmo Oracle muda de lado), a mesma decisão pode ser arquitetura num projeto e design em outro, e pode deixar de ser arquitetura no mesmo projeto. Isso explica por que nenhuma lista fixa ("banco é arquitetura, classe é design") funciona.
- **Os critérios objetivos e o de custo apontam para o mesmo lugar.** O que é visível de fora de um elemento (SEI) ou não local (Eden) é justamente o que fica caro mudar, porque a mudança se espalha para quem depende daquilo. A interface pública é cara de mudar; o detalhe privado, não. Inferência minha.

## 6. A distinção em três frases (para vídeo curto)

Arquitetura é design; a diferença é de grau, não de natureza. Quanto mais cara de desfazer e quanto mais partes do sistema uma decisão afeta, mais ela é arquitetura: usar o padrão Strategy numa classe é design, quebrar o serviço de pagamento em cinco serviços é arquitetura. E a linha se move: o que o time consegue tornar barato de mudar deixa de ser arquitetura.

Exemplo concreto para o vídeo: o banco de dados. Num sistema de cadastro ele é arquitetura, porque tudo gira em torno dele; num sistema de análise de imagens médicas, o mesmo banco é um detalhe que quase ninguém do time toca (WNA). E se o time tem migrações automatizadas, até o esquema do banco deixa de ser arquitetura (WNA).

## 7. Ângulos de vídeo

Ganchos são candidatos, a ajustar com a skill `writing-short-video-scripts` e a voz de eusouosalmo.

| Ângulo | Fonte | Gancho candidato |
| - | - | - |
| O Uncle Bob diz que não existe diferença, e o Mark Richards diz que existe. Os dois estão certos, porque respondem a perguntas diferentes. | CA, SAM | "Li Clean Architecture e Fundamentals of Software Architecture e eles discordam numa coisa básica: se arquitetura e design são diferentes." |
| A pergunta que separa: quanto custa desfazer isso? | WNA, SAM, BCH | "Tem uma pergunta só que te diz se uma decisão é arquitetura ou design." |
| O mesmo banco de dados é arquitetura num sistema e detalhe em outro. | WNA | "Banco de dados é arquitetura? Depende, e o exemplo do Ralph Johnson mostra por quê." |
| O melhor arquiteto diminui a arquitetura. | WNA | "Segundo o Martin Fowler, um dos trabalhos mais importantes do arquiteto é se livrar da arquitetura." |
| Strategy, microsserviços e o meio do caminho, onde vive quase toda decisão. | SAM | "Usar o padrão Strategy é design. Adotar microsserviços é arquitetura. E separar o serviço de pagamento?" |
| Quem decide: o espectro serve para saber de quem é a responsabilidade. | SAM, WNA | "Saber a diferença entre arquitetura e design não é teoria: é saber se a decisão é sua ou do arquiteto." |
| Arquitetura não é o diagrama. | ISO, SEI | "Seu sistema tem arquitetura mesmo que ninguém nunca tenha desenhado ela." |

## 8. Perguntas em aberto

1. **Páginas dos livros.** As referências a Clean Architecture (cap. 1, p. 3 e 4; cap. 15) e a Fundamentals (cap. 2) são paráfrases da leitura, não conferidas no texto nesta pesquisa. eusouosalmo tem os dois livros e pode conferir antes de citar num vídeo.
2. **Fundamentals, 2a edição (2025).** Um podcast indica que o cap. 2 da 2a edição trata arquitetura contra design; não verifiquei se ela adota o espectro da lição 167.
3. **Booch no original.** A frase "toda arquitetura é design, mas nem todo design é arquitetura" e o custo de mudança como medida só foram conferidos em reproduções. Falta abrir o post de 2006 arquivado ou a p. 214 do POSA vol. 5.
4. **ISO/IEC/IEEE 42010:2022.** Usei a definição da edição 2011, confirmada no site dos editores. A redação da edição 2022 (que fala em entidade, não sistema) não foi conferida, e a ISO/IEC/IEEE 42024, que trataria a distinção diretamente, não foi lida.
5. **Eden e Kazman, ICSE 2003.** O artigo "Architecture, Design, Implementation", que propõe os critérios de intenção e localidade para separar os três níveis, foi citado só a partir das páginas do autor.
6. **Origem do trecho do Uncle Bob (UBV).** O corte vem de um canal de terceiros, sem indicar a palestra de origem.
