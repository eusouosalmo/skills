# Analogia na explicação e animação sincronizada à fala

Resumo: o catálogo do mapa marcou como novas, por falta de base nas pesquisas do repo, as técnicas de analogia e boa parte das de animação e densidade. Esta nota procura a base primária de cada técnica marcada "sim" nessas três seções. Na analogia, a base é sólida para o mecanismo geral: o que se transfere é a estrutura de relações, não a aparência (teoria de structure-mapping de Gentner); comparar dois casos alinhados ensina mais que estudar um caso só (meta-análise de Alfieri e colegas); quem ouve uma analogia raramente faz o mapeamento sozinho, então o vídeo precisa dizer onde cada peça cai (Gick e Holyoak); e a analogia simples que ajuda no começo tende a ser levada além do limite, então vale dizer onde ela quebra (Spiro e colegas; o modelo de Glynn). Dos seis tipos de analogia marcados "sim", três têm base primária próxima (troca de uma peça, analogia em fila, um objeto em dois estados), dois têm base fraca ou disputada (mundo-metáfora, máquina como colega) e um não tem base primária específica (caso-limite literal). Na animação, a base é sólida para três pontos: animação ganha de imagem estática sobretudo quando a mudança é o conteúdo (meta-análises de Höffler e Leutner e de Berney e Bétrancourt, com a reanálise de Ploetzner); transição animada ganha de corte seco quando a pessoa precisa seguir um objeto de um estado ao outro (Heer e Robertson); e cor que acompanha a causa, sincronizada com o evento, ganha de seta e de nenhuma pista (Boucheix e Lowe). O desenho traço a traço tem base, mas com uma condição que o catálogo não registra: o efeito apareceu quando a mão de quem desenha estava visível, não com o traço animado sozinho (Fiorella e Mayer). Tela de impacto, contador como relógio, dado real para quem pausa, código como prova e fonte como print não têm base primária encontrada. Quase toda a evidência vem de estudantes em aulas de laboratório; a passagem para Reels é inferência e está marcada. Pesquisa de 2026-10-10, complementar a [roteiro-de-video.md](roteiro-de-video.md), [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md) e [texto-na-tela.md](texto-na-tela.md). Não decide nada; a seção 7 resume o que muda para os tickets de melhoria.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [O que as pesquisas do repo já cobrem](#2-o-que-as-pesquisas-do-repo-já-cobrem)
3. [Analogia](#3-analogia)
4. [Animação](#4-animação)
5. [Sinalização por cor](#5-sinalização-por-cor)
6. [Densidade de informação](#6-densidade-de-informação)
7. [Quadro por técnica e o que muda para os tickets](#7-quadro-por-técnica-e-o-que-muda-para-os-tickets)

## 1. Fontes e método

As perguntas, do ticket [Pesquisa de base: analogia na explicação e animação sincronizada à fala](https://github.com/eusouosalmo/skills/issues/55): o que as fontes primárias dizem sobre (a) analogia na explicação, seus tipos, quando ajuda e quando atrapalha; e (b) animação sincronizada à fala, com transformação contínua no lugar do corte, um objeto por vez contra painel denso, e sinalização por cor. A lista de técnicas vem das seções Analogia, Animação e Densidade do catálogo do mapa ([ticket da síntese](https://github.com/eusouosalmo/skills/issues/30)). Os reels de referência são citados pelo link; os padrões estão descritos com palavras minhas.

Pesquisa acadêmica sobre analogia (quando li só o resumo ou uma fonte secundária, está dito):

| Sigla | Fonte |
| - | - |
| GEN | Gentner, D. (1983). [Structure-mapping: a theoretical framework for analogy](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf). Cognitive Science 7, 155 a 170. Li o resumo e a descrição do princípio de sistematicidade no [resumo do grupo de Gentner](https://www.qrg.northwestern.edu/ideas/smeidea.htm). |
| CG | Clement, C. A. e Gentner, D. (1991). [Systematicity as a selection constraint in analogical mapping](https://groups.psych.northwestern.edu/gentner/papers/ClementGentner91.pdf). Cognitive Science 15, 89 a 132. Li o resumo. |
| MG | Markman, A. B. e Gentner, D. (1993). [Splitting the differences: a structural alignment view of similarity](https://groups.psych.northwestern.edu/gentner/papers/MarkmanGentner93b.pdf). Journal of Memory and Language 32, 517 a 535. Li o resumo. |
| GLT | Gentner, D., Loewenstein, J. e Thompson, L. (2003). [Learning and transfer: a general role for analogical encoding](https://dedregentner.owlstown.net/publications/38525-learning-and-transfer-a-general-role-for-analogical-encoding). Journal of Educational Psychology 95(2), 393 a 408. Li o resumo. |
| GH | Gick, M. L. e Holyoak, K. J. (1980). [Analogical problem solving](https://deepblue.lib.umich.edu/handle/2027.42/23210). Cognitive Psychology 12, 306 a 355; e (1983) [Schema induction and analogical transfer](https://www.gwern.net/doc/psychology/1983-gick.pdf). Cognitive Psychology 15, 1 a 38. Li o resumo de 1980 e o artigo de 1983, que recapitula os números de 1980. Universitários. |
| ANS | Alfieri, L., Nokes-Malach, T. J. e Schunn, C. D. (2013). [Learning through case comparisons: a meta-analytic review](https://doi.org/10.1080/00461520.2013.775712). Educational Psychologist 48(2), 87 a 113. 57 experimentos, 336 testes. Li o resumo; o tamanho de efeito (d de cerca de 0,50) vem de um resumo de terceiros e não foi conferido no artigo. |
| SPI | Spiro, R. J., Feltovich, P. J., Coulson, R. L. e Anderson, D. K. (1989). [Multiple analogies for complex concepts: antidotes for analogy-induced misconception in advanced knowledge acquisition](https://www.cambridge.org/core/books/similarity-and-analogical-reasoning/multiple-analogies-for-complex-concepts-antidotes-for-analogyinduced-misconception-in-advanced-knowledge-acquisition/FF07DBE3F194DB258119713D3000E730). Em Vosniadou e Ortony (org.), Similarity and Analogical Reasoning, cap. 18. Li o resumo. Capítulo teórico com casos de medicina, não experimento controlado. |
| GLY | Glynn, S. M. (1991). Explaining science concepts: a teaching-with-analogies model. Em Glynn, Yeany e Britton (org.), The Psychology of Learning Science, 219 a 240. Não li; os seis passos do modelo conforme [Yener (2012)](https://www.eduhk.hk/apfslt/v13_issue1/yener/page2.htm). |
| HT | Harrison, A. G. e Treagust, D. F. (2006). [Teaching and learning with analogies: friend or foe?](https://acquire.cqu.edu.au/articles/chapter/Teaching_and_learning_with_analogies_friend_or_foe/13440575) Em Aubusson, Harrison e Ritchie (org.), Metaphor and Analogy in Science Education. Não li; conforme o registro e citações. |
| RZH | Richland, L. E., Zur, O. e Holyoak, K. J. (2007). [Cognitive supports for analogies in the mathematics classroom](https://pubmed.ncbi.nlm.nih.gov/17525320). Science 316, 1128 a 1129. Análise de vídeos de aula do TIMSS 1999. Não há resumo no PubMed; li a cobertura secundária. Estudo observacional. |
| CLE | Clement, J. (1993). [Using bridging analogies and anchoring intuitions to deal with students' preconceptions in physics](https://doi.org/10.1002/tea.3660301007). Journal of Research in Science Teaching 30(10), 1241 a 1257. Não li o artigo; a definição de caso-âncora conforme [Stephens e Clement (2008)](https://www.srri.umass.edu/sites/srri/files/NARST08StepClemAnchors/index.pdf). |
| SD | Sopory, P. e Dillard, J. P. (2002). [The persuasive effects of metaphor: a meta-analysis](https://pure.psu.edu/en/publications/the-persuasive-effects-of-metaphor-a-meta-analysis/). Human Communication Research 28(3), 382 a 419. Li o resumo. |
| THI | Thibodeau, P. H. (2016). [Extended metaphors are the home runs of persuasion: don't fumble the phrase](https://digitalcommons.oberlin.edu/faculty_schol/2125). Metaphor and Symbol 31(2), 53 a 72. Li o resumo. |
| SRB | Steen, G. J., Reijnierse, W. G. e Burgers, C. (2014). [When do natural language metaphors influence reasoning? A follow-up study to Thibodeau and Boroditsky (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4260786/). PLoS ONE 9(12): e113536. Li o resumo. |
| RBKS | Reijnierse, W. G., Burgers, C., Krennmayr, T. e Steen, G. J. (2015). How viruses and beasts affect our opinions (or not): the role of extendedness in metaphorical framing. Dois experimentos, 354 e 361 participantes. Li o [resumo publicado pelo laboratório dos autores](https://metaphorlab.org/new-article-on-the-role-of-extendedness-in-metaphorical-framing). |
| BBV | Brugman, B. C., Burgers, C. e Vis, B. (2019). [Metaphorical framing in political discourse through words vs. concepts: a meta-analysis](https://research-portal.uu.nl/en/publications/metaphorical-framing-in-political-discourse-through-words-vs-conc/). Language and Cognition 11(1), 41 a 65. 91 estudos, 34.783 participantes. Li o resumo. |
| ZG | Zohar, A. e Ginossar, S. (1998). [Lifting the taboo regarding teleology and anthropomorphism in biology education: heretical suggestions](https://en-anatzohar.huji.ac.il/publications/lifting-taboo-regarding-teleology-and-anthropomorphism-biology). Science Education 82(6). Li o resumo. Alunos de ensino médio. |
| BSD | Brom, C., Stárková, T. e D'Mello, S. K. (2018). [How effective is emotional design? A meta-analysis on facial anthropomorphisms and pleasant colors during multimedia learning](https://artemis.ms.mff.cuni.cz/main/papers/emodesign_manuscript_1rev_180928_FINAL_norev.pdf). Educational Research Review 25, 100 a 119. 33 amostras, 2.924 participantes. Li o resumo do manuscrito dos autores. |
| BAN | Banas, J. A., Dunbar, N., Rodriguez, D. e Liu, S. (2011). [A review of humor in educational settings: four decades of research](https://doi.org/10.1080/03634523.2010.496867). Communication Education 60(1), 115 a 144. Não li; conforme resumos secundários. |
| TP | Tennyson, R. D. e Park, O. (1980). [The teaching of concepts: a review of instructional design research literature](https://journals.sagepub.com/toc/rera/50/1). Review of Educational Research 50(1), 55 a 70. Li o resumo; os princípios de exemplos divergentes conforme fonte secundária. |

Pesquisa acadêmica sobre animação, cor e densidade:

| Sigla | Fonte |
| - | - |
| HL | Höffler, T. N. e Leutner, D. (2007). [Instructional animation versus static pictures: a meta-analysis](https://wikicap.ulb.be/images/e/ef/Hoffler_Leutner_2007.pdf). Learning and Instruction 17(6), 722 a 738. 26 estudos, 76 comparações. Li o resumo. |
| BB | Berney, S. e Bétrancourt, M. (2016). [Does animation enhance learning? A meta-analysis](https://archive-ouverte.unige.ch/unige:92234). Computers & Education 101, 150 a 167. 61 estudos, 7.036 participantes, 140 comparações. Li o resumo. |
| TMB | Tversky, B., Morrison, J. B. e Bétrancourt, M. (2002). [Animation: can it facilitate?](https://www.uky.edu/~gmswan3/575/Tversky_2002.pdf) International Journal of Human-Computer Studies 57, 247 a 262. Revisão. Li a introdução e a seção sobre animação. |
| PBB | Ploetzner, R., Berney, S. e Bétrancourt, M. (2020), reanálise dos dados de BB; e (2021) [When learning from animations is more successful than learning from static pictures: learning the specifics of change](https://link.springer.com/article/10.1007/s11251-021-09541-w). Instructional Science 49. Li os resumos. |
| HR | Heer, J. e Robertson, G. (2007). [Animated transitions in statistical data graphics](https://homes.cs.washington.edu/~jheer/files/2007-AnimatedTrans-InfoVis.pdf). IEEE Transactions on Visualization and Computer Graphics 13(6), 1240 a 1247. 24 adultos que usam gráficos no trabalho. Li o artigo. |
| ROC | Rensink, R. A., O'Regan, J. K. e Clark, J. J. (1997). [To see or not to see: the need for attention to perceive changes in scenes](https://homepage.villanova.edu/diego.fernandezduque/Teaching/CognitivePsychology/Lectures_and_Labs/s3Attention/sReading/Rensink_etal_97.pdf). Psychological Science 8, 368 a 373. Li o [resumo de 1996](https://www2.psych.ubc.ca/~rensink/publications/abs.96.2.html). |
| MZ | Magliano, J. P. e Zacks, J. M. (2011). [The impact of continuity editing in narrative film on event segmentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3208769). Cognitive Science 35(8), 1489 a 1517. Li o resumo. |
| FM | Fiorella, L. e Mayer, R. E. (2016). Effects of observing the instructor draw diagrams on learning from multimedia messages. Journal of Educational Psychology 108(4), 528 a 546. Não li o artigo; experimentos e números conforme a [tese de Fiorella (2015)](https://escholarship.org/uc/item/55v7s9t1), na qual ele se baseia, e um [texto de divulgação de Fiorella](https://learningscientists.org/blog/2017/1/24-1) sobre o estudo. |
| TM | Türkay, S. e Mouton, S. (2016). [The educational impact of whiteboard animations: an experiment using popular social science lessons](https://www.vpal.harvard.edu/publications/educational-impact-whiteboard-animations-experiment-using-popular-social-science). Anais do MIT LINC. 568 participantes do Mechanical Turk. Li o resumo. Artigo de congresso, não revista. |
| WLMS | Wong, A., Leahy, W., Marcus, N. e Sweller, J. (2012). Cognitive load theory, the transient information effect and e-learning. Learning and Instruction 22, 449 a 457; e Leahy, W. e Sweller, J. (2011), Applied Cognitive Psychology 25, 943 a 951. Não li; conforme a [replicação com crianças](https://lead.ube.fr/wp-content/uploads/2023/09/001246-reducing-the-transience-effect-of-animations-does-not-always-lead-to-better-performance-in-children-learning-a-complex-hand-procedure.pdf) que os discute. |
| KACS | Kalyuga, S., Ayres, P., Chandler, P. e Sweller, J. (2003). [The expertise reversal effect](https://ro.uow.edu.au/edupapers/136). Educational Psychologist 38(1), 23 a 31. Li o resumo. |
| MC | Mayer, R. E. e Chandler, P. (2001). When learning is just a click away: does simple user interaction foster deeper understanding of multimedia messages? Journal of Educational Psychology 93(2), 390 a 397. [doi:10.1037/0022-0663.93.2.390](https://doi.org/10.1037/0022-0663.93.2.390). Não li; conforme MAY e um [trabalho que descreve o desenho](https://cogsci.ucsd.edu/undergraduates/honors-program/Sheel,-Shreya_Segmenting-in-Multimedia-Learning_Final.pdf). |
| CJ | Chun, M. M. e Jiang, Y. (1998). Contextual cueing: implicit learning and memory of visual context guides spatial attention. Cognitive Psychology 36, 28 a 71. [doi:10.1006/cogp.1998.0681](https://doi.org/10.1006/cogp.1998.0681). Não li; conforme revisões que o citam. |
| OKKC | Ozcelik, E., Karakus, T., Kursun, E. e Cagiltay, K. (2009). [An eye-tracking study of how color coding affects multimedia learning](https://open.metu.edu.tr/handle/11511/28595). Computers & Education 53(2), 445 a 453. 52 participantes. Li o resumo. |
| BL | Boucheix, J.-M. e Lowe, R. K. (2010). [An eye tracking comparison of external pointing cues and internal continuous cues in learning with complex animations](https://lead.ube.fr/wp-content/uploads/2023/09/000191-an-eye-tracking-comparison-of-external-pointing-cues-and-internal-continuous-cues-in-learning-with-complex-animations.pdf). Learning and Instruction 20(2), 123 a 135. Li o resumo. |
| DK | de Koning, B. B., Tabbers, H. K., Rikers, R. M. J. P. e Paas, F. (2009). [Towards a framework for attention cueing in instructional animations](https://link.springer.com/article/10.1007/s10648-009-9098-7). Educational Psychology Review 21, 113 a 140. Revisão. Li o resumo. |
| WCAG | W3C, [Understanding Success Criterion 2.3.1: Three Flashes or Below Threshold](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html) (WCAG 2.2). Norma de acessibilidade, não estudo. |

Siglas que já estão nas notas anteriores e são reusadas aqui: MAY (Mayer e Fiorella, 2014), SBNR (Schneider e colegas, 2018), YJ (Yantis e Jonides), REY (Rey, 2012), definidas em [texto-na-tela.md](texto-na-tela.md) e [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md).

Níveis de confiança, os mesmos das notas anteriores:

- **Confirmado:** estudo primário ou meta-análise que testa o mecanismo.
- **Relato:** prático com dados próprios, guia, artigo de congresso, estudo observacional, ou estudo que só li por fonte secundária fraca.
- **Inferência:** conclusão minha a partir de um achado confirmado, para uma situação que o estudo não testou.
- **Sem base primária:** procurei e não achei estudo que teste a técnica nem o mecanismo direto dela.

Ressalvas de método:

- **População:** quase todos os estudos são com universitários aprendendo um processo (raio, freio, mecanismo de piano, negociação) numa aula curta de laboratório, com teste logo depois. O espectador de Reels não está estudando e pode sair a qualquer momento. Achado confirmado aplicado ao Reel é sempre inferência.
- **Medida:** os estudos medem lembrança e transferência, não retenção de audiência. Nenhum estudo encontrado mede se uma técnica de analogia ou de animação segura o espectador no vídeo. O catálogo mede desempenho em múltiplo da mediana do perfil, que é a outra metade da pergunta e não é coberta aqui.
- **Analogia em texto, não em vídeo:** os estudos de analogia usam texto escrito ou aula falada sem animação. Nenhum estudo encontrado testa analogia desenhada e animada no ritmo da fala.
- **Leitura parcial:** vários artigos foram lidos só pelo resumo (indicado na tabela). Os números que vêm de resumo de terceiros estão marcados.

## 2. O que as pesquisas do repo já cobrem

Antes do que é novo, o que já tem base no repo e não é repetido aqui:

- **Entrar na palavra (contiguidade no tempo):** [texto-na-tela.md](texto-na-tela.md), seção 4.5 (MAY: animação e narração juntas ganharam em 9 de 9 testes, d mediano 1,22). Cobre a técnica "animação nasce na palavra", que o catálogo marcou "já". A seção 5 desta nota acrescenta uma confirmação específica de animação (BL, experimento 2).
- **Sinalização em geral e o orçamento do destaque:** [texto-na-tela.md](texto-na-tela.md), seções 4.1 a 4.4 (SBNR: cor ajuda, piscar atrapalha; destaque só funciona se for raro). [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), seção 3.7.
- **Coerência e detalhe sedutor:** [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), seção 3.3 (MAY, 23 de 23 testes; REY). É a base contra o "dado real para quem pausa" quando o dado não serve à ideia (seção 6.3 desta nota).
- **Cadeia causal:** [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), seção 3.2. É a mesma propriedade que torna uma analogia em fila mapeável (seção 3.3 desta nota).
- **Concreto e específico prende mais que abstrato; expectativa violada:** [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), seções 2.4 e 2.6. É a vizinhança mais próxima do caso-limite literal (seção 3.7).
- **Conhecimento prévio muda o que ajuda:** [psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), seção 3.6 (reverse cohesion). A seção 6.1 desta nota liga isso ao efeito de inversão por expertise (KACS).
- **Orçamento de texto grande e ritmo de eventos:** [texto-na-tela.md](texto-na-tela.md), seção 4.3, e os números do catálogo. Ficam fora desta nota (o catálogo marcou "já?").

Nenhuma das três notas trata analogia, metáfora, transição animada contra corte, desenho ao vivo, cor que segue a causa ou densidade de painel. Isso é o que segue.

## 3. Analogia

### 3.1 O mecanismo: o que se transfere é a estrutura de relações

- **O que é:** GEN define analogia como o mapeamento de um sistema de relações de um domínio-base para um domínio-alvo. Mapeiam-se as relações entre objetos, não os atributos dos objetos; e, entre as relações, prefere-se o sistema conectado (relações ligadas por relações de ordem mais alta, como causa) ao fato isolado. É o princípio de sistematicidade. CG testou o princípio: as pessoas escolheram o par que fazia parte de um sistema maior de relações, e as previsões que fizeram seguiram a estrutura causal da base.
- **Por que importa:** dá o critério para escolher a base de uma analogia. A boa base não é a que "parece" com o conceito; é a que tem as mesmas relações causais. Um restaurante explica uma fila de requisições porque a relação "pedido espera a cozinha liberar" é a mesma, não porque prato e pacote se parecem.
- **Confiança:** confirmado (laboratório, texto).

### 3.2 Quando ajuda e quando atrapalha

Quatro achados valem para todos os tipos do catálogo:

1. **Quem ouve raramente faz o mapeamento sozinho.** GH: com uma história militar análoga lida antes, cerca de 30% dos universitários acharam a solução do problema médico sem dica, contra cerca de 75% quando alguém disse que a história servia, e cerca de 10% sem história nenhuma. A analogia funcionou quando a ligação foi apontada. GH (1983) acrescentou que dois análogos, comparados, produzem um esquema geral que transfere melhor que um análogo só, e que o princípio dito em palavras ou desenhado, inútil com um análogo, ajudou quando veio junto de dois. Confiança: confirmado. Para o roteiro: a analogia precisa dizer em voz alta qual peça da base corresponde a qual peça do conceito; deixar o espectador inferir é a condição dos 30%.
2. **Comparar dois casos alinhados ensina mais que estudar um.** ANS, meta-análise de 57 experimentos: atividades de comparação deram mais aprendizagem que o estudo de um caso por vez, com efeito moderado (d de cerca de 0,50, número não conferido no artigo). Pelo resumo de terceiros, destacar as semelhanças ajudou mais que destacar semelhanças e diferenças juntas, e dar o princípio depois da comparação ajudou mais que antes. GLT: comparar dois casos de negociação levou à transferência muito mais que ler os mesmos dois casos separados. MG: numa comparação, as diferenças notadas são as alinháveis, ligadas à estrutura comum; diferenças sem relação com o que é comum passam despercebidas. Confiança: confirmado.
3. **A analogia simples fica, e é levada além do limite.** SPI argumenta, com casos de estudantes de medicina, que uma analogia simples que dá a primeira noção de um conceito complexo vira obstáculo depois, porque o aprendiz tende a limitar o entendimento aos aspectos da primeira analogia; o antídoto proposto é usar mais de uma analogia para o mesmo conceito, cada uma cobrindo o que a outra deixa errado. O modelo de ensino com analogias de GLY tem seis passos, e o quinto é dizer onde a analogia quebra; HT relatam que os professores pulam passos na prática e propõem uma versão mais curta que mantém o passo das diferenças. Confiança: SPI é argumento teórico com casos, não experimento (relato forte); o passo de dizer onde quebra é recomendação de modelo didático com estudos de sala de aula que li só por fonte secundária (relato).
4. **Apoio visual ajuda a comparar.** RZH compararam aulas de matemática filmadas: os professores dos EUA usaram tantas analogias quanto os de Hong Kong e do Japão, mas com menos apoio ao raciocínio, como deixar a base visível enquanto se fala do alvo, desenhar os dois lado a lado e apontar com gesto a correspondência. Confiança: relato (estudo observacional; mostra a diferença de prática, não prova que o apoio causa a aprendizagem). É, porém, exatamente o que uma cena animada pode fazer: manter a base na tela enquanto o alvo entra.

Sobre metáfora como recurso de persuasão (não de ensino), SD acharam efeito pequeno da metáfora sobre a mudança de atitude (r = 0,07), que sobe para r = 0,42 nas condições ótimas: uma metáfora só, não estendida, nova, com alvo familiar e no começo da mensagem. A explicação com mais apoio foi a de que a metáfora organiza o argumento. A metáfora não mudou a competência percebida de quem fala. Confiança: confirmado (meta-análise, li o resumo).

### 3.3 Analogia em fila

- **Técnica do catálogo:** um processo cotidiano cujas etapas dão um conceito cada ([DaxaKNvhqGh](https://www.instagram.com/reel/DaxaKNvhqGh/)).
- **Base:** o princípio de sistematicidade (GEN, CG). Uma fila de etapas ligadas por causa é um sistema de relações; o mapeamento etapa por etapa transfere o sistema, não só cada peça. É a mesma propriedade que a pesquisa do repo já confirmou para a escada no roteiro ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 3.2). O risco vem de GH e SPI: cada etapa precisa ter a correspondência dita (senão o espectador não mapeia), e a fila inteira convida a estender a base para etapas que não correspondem.
- **Confiança:** confirmado para o mecanismo; a forma em vídeo é inferência.
- **Para a skill:** a fila funciona quando as etapas da base são causa umas das outras, como as do conceito. Uma fila de etapas paralelas (uma lista) perde a vantagem. Dizer a correspondência em cada etapa e, no fim, a etapa em que a base não serve.

### 3.4 Troca de uma peça

- **Técnica do catálogo:** uma cena familiar com conclusão óbvia; troca-se um elemento e a conclusão se transfere ([Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DbdpctKxaUd](https://www.instagram.com/reel/DbdpctKxaUd/)).
- **Base:** é a estratégia de caso-âncora de CLE: começar por uma situação em que a intuição do aluno já acerta (a âncora) e chegar ao caso difícil por casos-ponte, cada um com distância menor. A troca de uma peça é a ponte mais curta possível. MG explicam por que funciona: a diferença única entre duas cenas alinhadas é uma diferença alinhável, a que a comparação faz notar. ANS e GLT dão a vantagem da comparação de dois casos sobre um caso só.
- **Confiança:** confirmado para comparação e diferença alinhável (laboratório); a estratégia de âncora e ponte é de sala de aula de física, lida por fonte secundária (relato forte).
- **Para a skill:** as duas cenas precisam ter a mesma estrutura e diferir em uma peça só; com mais de uma diferença, a comparação já não aponta para o conceito.

### 3.5 Um objeto, dois estados

- **Técnica do catálogo:** dois termos que se confundem viram o mesmo objeto em dois momentos ([DbdpctKxaUd](https://www.instagram.com/reel/DbdpctKxaUd/)).
- **Base:** é a comparação de dois casos alinhados ao máximo: mesmo objeto, então todas as diferenças são alinháveis e a única que sobra é a que separa os termos (MG, ANS). Do lado da animação, mostrar a passagem de um estado ao outro é o caso em que animação ganha de imagem estática, porque a mudança é o conteúdo (seção 4.3).
- **Confiança:** inferência a partir de achados confirmados; nenhum estudo testa esta forma.
- **Para a skill:** os dois estados devem aparecer lado a lado ou em sequência sem corte, para a comparação ser possível (RZH; seção 4.1).

### 3.6 Mundo-metáfora

- **Técnica do catálogo:** a metáfora é dita uma vez e vira o cenário; a fala segue literal ([DeMxXXwM3K1](https://www.instagram.com/reel/DeMxXXwM3K1/)). eusouosalmo a ligou ao exemplo das cores da criptografia.
- **Base:** disputada. A favor de estender a metáfora: THI achou que levar a metáfora até a solução proposta aumentou o efeito de enquadramento, e só quando a solução era coerente com a metáfora; BBV, meta-análise de 91 estudos, achou efeito maior quando a metáfora enquadra o conceito do que quando é só uma palavra. Contra: SD acharam o maior efeito com metáfora não estendida; RBKS não acharam efeito consistente ao aumentar o número de frases metafóricas; SRB não replicaram o efeito do estudo original de enquadramento que THI estende. Todos esses estudos medem persuasão por texto, não aprendizagem nem imagem.
- **O que a técnica tem de diferente:** a metáfora estendida aqui é visual, não verbal. A fala literal mantém o termo técnico (o que GH e GLY pedem: a correspondência dita), e o cenário mantém a base visível (o apoio de RZH). Essa combinação não tem estudo.
- **Confiança:** sem base primária para a forma; a evidência sobre metáfora estendida em texto é mista. O risco de SPI vale em dobro: o cenário fixo convida a estender a base para partes do conceito em que ela não serve.
- **Para a skill:** se usar, mostrar em algum momento onde o cenário deixa de corresponder.

### 3.7 Máquina como colega

- **Técnica do catálogo:** o sistema explicado como um tipo humano conhecido ([Db4GJGZDgRz](https://www.instagram.com/reel/Db4GJGZDgRz/); invertida em [DdcVdIPAK3v](https://www.instagram.com/reel/DdcVdIPAK3v/)). O catálogo a marca como humor dentro da explicação.
- **Base:** fraca. Antropomorfismo em explicação de ciência é estudado sobretudo em biologia: ZG acharam que alunos de ensino médio que aceitam frases antropomórficas não raciocinam necessariamente de forma antropomórfica, e que os alunos relatam que essas frases ajudam a entender; outros autores ligam o antropomorfismo a concepções erradas, em estudos que li só por fonte secundária. BSD, meta-análise de emotional design, acharam efeito positivo de rostos em elementos gráficos e cores agradáveis sobre retenção (d = 0,39) e transferência (d = 0,33), mas isso é rosto desenhado num objeto, não o sistema descrito como pessoa. BAN, revisão sobre humor em sala, conclui que humor aumenta atenção e interesse e que o humor ligado ao conteúdo é o que pode ajudar a lembrar (lida por resumo secundário).
- **Confiança:** relato. Nenhum estudo testa explicar um sistema técnico como um tipo humano.
- **Para a skill:** o risco é o de SPI e da biologia: o espectador atribui ao sistema intenção que ele não tem. Funciona quando o traço humano corresponde a uma relação real do sistema (o colega que responde sem verificar corresponde ao cache que devolve dado velho), não a um traço só engraçado.

### 3.8 Caso-limite literal

- **Técnica do catálogo:** não é analogia; um objeto cotidiano que é de fato uma instância do conceito, levado ao extremo ([Ddjvq7TMpuD](https://www.instagram.com/reel/Ddjvq7TMpuD/)).
- **Base:** sem base primária específica. A vizinhança mais próxima: a pesquisa de ensino de conceitos (TP) recomenda exemplos divergentes, que variam os atributos irrelevantes para mostrar que o conceito vale mesmo longe do caso típico (princípio lido por fonte secundária); e as notas do repo já confirmam que o concreto prende mais que o abstrato e que a expectativa violada puxa a busca de explicação ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 2.4 e 2.6).
- **Confiança:** sem base primária; o mecanismo vizinho é relato (TP) e confirmado (notas do repo).
- **Para a skill:** como não é analogia, não sofre o risco de mapeamento errado; o cuidado é que o caso seja de fato uma instância do conceito, verificável.

## 4. Animação

### 4.1 Animação contra imagem estática: o efeito é pequeno e depende do que muda

- **O que é:** HL, 26 estudos: animação ganhou de imagem estática com efeito médio (d = 0,37), um pouco maior quando a animação representa o próprio conteúdo em vez de enfeitar (d = 0,40), maior em vídeo realista (d = 0,76) e em conhecimento de procedimento motor (d = 1,06). BB, 61 estudos: efeito menor (g = 0,23), maior com narração junto (g = 0,34). TMB, antes das duas, argumentaram que quase todas as vitórias da animação vinham de comparações desiguais (a animação tinha mais informação ou interatividade) e que, por isso, a animação precisa obedecer a dois princípios: congruência (a forma do gráfico corresponde à forma do conceito; mudança se mostra com mudança) e apreensão (a animação precisa ser percebida com precisão; muitas são rápidas ou complexas demais). TMB também notam que muitos processos contínuos são pensados como sequência de passos discretos. A reanálise de PBB achou que a animação ganha quando a mudança em si é difícil e relevante para aprender; com mudanças simples, quem vê imagens estáticas anima mentalmente sozinho. No experimento de 2021, a animação ganhou para identificar movimentos e as imagens estáticas ganharam para identificar a disposição das peças.
- **Por que importa:** é o contrapeso de todas as técnicas de animação. Animar ajuda quando o que se anima é a mudança que a fala explica; animar o resto custa sem render.
- **Confiança:** confirmado (meta-análises).

### 4.2 Transformação contínua no lugar do corte

- **Técnica do catálogo:** o objeto de uma cena vira o da próxima, sem corte, ou a câmera anda num cenário fixo ([Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DeAVwyDp-LI](https://www.instagram.com/reel/DeAVwyDp-LI/), [DeJ15MDlY8y](https://www.instagram.com/reel/DeJ15MDlY8y/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeMxXXwM3K1](https://www.instagram.com/reel/DeMxXXwM3K1/), [DeCf1khst4y](https://www.instagram.com/reel/DeCf1khst4y/)).
- **Base:** HR é o teste mais próximo. Adultos acompanharam objetos marcados durante a mudança de um gráfico para outro (barras para rosca, dispersão para barras, reordenação), com transição estática (o gráfico novo substitui o antigo de uma vez, como num corte) ou animada. No experimento de rastrear objetos, a transição animada foi significativamente melhor que a estática em todas as condições; a animação em etapas (uma mudança por vez: primeiro a posição, depois a forma) foi melhor que a animação direta na maioria. No de estimar mudança de valor, a animação ganhou na maioria das condições, com exceções. Os participantes preferiram a animação em etapas, depois a direta, por último a estática. HR derivam princípios: manter o gráfico válido durante a transição, manter os mesmos mapeamentos, agrupar movimentos parecidos, evitar sobreposição, mudar uma coisa por etapa. ROC explicam por que o corte perde: com uma interrupção breve entre a cena original e a modificada, mudanças grandes passam despercebidas por muitos segundos, porque só se percebe a mudança no item em que a atenção está no momento em que ele muda. MZ dão o limite do argumento: no cinema, cortes com a ação contínua quase não alteram como o espectador divide a história em eventos; o que marca um novo evento é a quebra da ação.
- **Confiança:** confirmado para rastrear objetos de um estado ao outro (adultos, gráficos, laboratório); a aplicação ao Reel é inferência. O corte não é ruim em si (MZ); ele custa quando a explicação depende de o espectador ver qual objeto virou qual.
- **Para a skill:** usar transformação contínua quando a fala diz que A virou B ou que A causou mudança em B; usar corte quando começa um evento novo. Numa transformação complexa, uma mudança por etapa (HR).

### 4.3 Objeto que muda de forma é a explicação

- **Técnica do catálogo:** cada conceito é uma transformação visível do objeto ([Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DeJ15MDlY8y](https://www.instagram.com/reel/DeJ15MDlY8y/)).
- **Base:** é o caso exato em que a animação ganha (seção 4.1): congruência de TMB (mudança mostrada como mudança), animação representacional em HL, mudança relevante e não trivial em PBB.
- **Confiança:** confirmado (meta-análises e reanálise); a reanálise de PBB se descreve como heurística e foi testada em um experimento só.
- **Para a skill:** a transformação vale quando a mudança é o que o espectador precisa entender e não é óbvia; se a mudança é simples, uma imagem antes e depois basta (PBB).

### 4.4 Palco fixo

- **Técnica do catálogo:** um diagrama ou mundo fica na tela e cada conceito é uma mudança dentro dele ([DeAVwyDp-LI](https://www.instagram.com/reel/DeAVwyDp-LI/), [DeMxXXwM3K1](https://www.instagram.com/reel/DeMxXXwM3K1/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeNUYLkRWsz](https://www.instagram.com/reel/DeNUYLkRWsz/)).
- **Base:** sem estudo da técnica; três achados vizinhos a sustentam. ROC: uma mudança é vista quando acontece à vista, no item que tem a atenção; num palco fixo, o resto não muda e a mudança é o único movimento (é também o que torna a entrada brusca eficaz, YJ em [texto-na-tela.md](texto-na-tela.md), 4.4). HR: manter os mesmos mapeamentos durante a transição. CJ: um arranjo espacial repetido torna a busca mais rápida, aprendido sem a pessoa perceber.
- **Confiança:** inferência a partir de achados confirmados.

### 4.5 Desenho traço a traço

- **Técnica do catálogo:** o objeto se desenha na frente de quem assiste, com lápis visível na versão lousa ([Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DeKo7zLTrcd](https://www.instagram.com/reel/DeKo7zLTrcd/), [DeAVwyDp-LI](https://www.instagram.com/reel/DeAVwyDp-LI/)).
- **Base:** FM, cinco experimentos com uma aula curta em vídeo sobre efeito Doppler. Ver o professor desenhar o diagrama, com a mesma narração, deu melhor transferência que ver o diagrama já pronto: com o corpo inteiro do professor, só para quem sabia pouco do assunto (d = 0,58); com só a mão visível, para todos (d = 0,35). Sem a mão visível, o desenho que se faz sozinho não teve vantagem significativa; e diagramas de computador animados para imitar o desenho também não ganharam significativamente dos estáticos (d = 0,33, não significativo). Os autores atribuem o efeito em parte à sinalização e à contiguidade no tempo e em parte à mão como pista social. TM, com 568 participantes online, acharam vantagem de vídeo de lousa animada em aprendizagem e em prazer relatado (artigo de congresso, li o resumo).
- **Confiança:** confirmado que ver desenhar ajuda quando a mão aparece; o traço que se desenha sozinho não teve efeito significativo. Li os números pela tese, não pelo artigo.
- **Onde muda o catálogo:** o catálogo manda o lápis e o traço tremido para o design system como estilo. Pela evidência, a mão (ou o lápis, que é o substituto mais próximo da mão numa animação) é a parte que carrega o efeito, não um detalhe de estilo. Se um lápis desenhado faz o papel da mão é inferência sem teste.

### 4.6 Tela de impacto

- **Técnica do catálogo:** menos de 1 s de tela inteira na cor de destaque, só no clímax ([DeAVwyDp-LI](https://www.instagram.com/reel/DeAVwyDp-LI/), [DeNUYLkRWsz](https://www.instagram.com/reel/DeNUYLkRWsz/)).
- **Base:** sem base primária. Vizinhança: a entrada brusca puxa a atenção (YJ) e o destaque só funciona se for raro ([texto-na-tela.md](texto-na-tela.md), 4.3 e 4.4), o que concorda com "só no clímax"; piscar como destaque teve efeito negativo em SBNR, o que pesa contra repetir. Limite de segurança, não de eficácia: WCAG 2.3.1 proíbe mais de três flashes por segundo acima do limiar e trata o vermelho saturado com limite próprio.
- **Confiança:** sem base primária para o efeito; o limite de flashes é norma.
- **Para a skill:** uma vez por vídeo, nunca em sequência rápida, evitando vermelho saturado em tela inteira.

### 4.7 Contador como relógio

- **Técnica do catálogo:** um número que corre junto com a animação e diz o que a fala não diz ([Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DdrHAI1MrFb](https://www.instagram.com/reel/DdrHAI1MrFb/), [DeMxXXwM3K1](https://www.instagram.com/reel/DeMxXXwM3K1/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeNUYLkRWsz](https://www.instagram.com/reel/DeNUYLkRWsz/)).
- **Base:** sem base primária para contadores. Duas inferências a partir do que já está no repo: como o número diz o que a fala não diz, ele não é redundante no sentido de MAY ([texto-na-tela.md](texto-na-tela.md), 2.1); e informação que muda rápido demais para ser lida é o caso do efeito de informação transitória (WLMS), então o número precisa parar no valor que importa.
- **Confiança:** sem base primária.

## 5. Sinalização por cor

O catálogo trata cor em dois lugares: a técnica "destaque que segue a causa" (marcada "não") e a lista para o design system ("cor com significado", uma cor por conceito reservada no vídeo inteiro, em 14 das 18 fichas). A pergunta do ticket inclui sinalização por cor.

- **O que é:** SBNR já mostrou que destaque por cor tem efeito positivo ([texto-na-tela.md](texto-na-tela.md), 4.4). OKKC, com eye tracking: o mesmo material com cor ligando a parte do texto à parte da figura deu melhor retenção e transferência que sem cor; os olhos acharam mais depressa a informação correspondente. BL é o estudo mais próximo de "destaque que segue a causa": numa animação de um mecanismo de piano, uma cor que se espalha pelas peças seguindo o caminho da causa ganhou de setas e de nenhuma pista na compreensão; no segundo experimento, a pista sincronizada com o evento ganhou da mesma pista fora de sincronia. DK, revisão, concluem que pistas de atenção ajudam a selecionar o que olhar numa animação e às vezes melhoram a aprendizagem; pistas que mostram organização e relação ainda pedem estudo. BSD acharam efeito positivo de cores agradáveis junto com rostos (retenção d = 0,39), mas a cor ali é emocional, não de sinalização.
- **Confiança:** confirmado que cor que liga elementos e cor que segue a causa, em sincronia, ajudam (laboratório, animações de mecanismo). A regra de reservar uma cor por conceito no vídeo inteiro é inferência a partir de OKKC (a cor funciona porque liga sempre as mesmas coisas) e do orçamento do destaque ([texto-na-tela.md](texto-na-tela.md), 4.3).
- **Onde muda o catálogo:** "destaque que segue a causa" está marcado "não" para teste, mas é a técnica de animação com a base primária mais direta desta nota (BL). Vale reconsiderar a marcação.

## 6. Densidade de informação

### 6.1 Dois regimes de densidade

- **Técnica do catálogo:** um objeto por cena quase sem texto ([Ddwk5EoAGMT](https://www.instagram.com/reel/Ddwk5EoAGMT/), [DeAVwyDp-LI](https://www.instagram.com/reel/DeAVwyDp-LI/), [DeJ15MDlY8y](https://www.instagram.com/reel/DeJ15MDlY8y/)) ou painel denso com zonas fixas ([DdrHAI1MrFb](https://www.instagram.com/reel/DdrHAI1MrFb/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeCf1khst4y](https://www.instagram.com/reel/DeCf1khst4y/)); os dois dão pico.
- **Base:** os princípios confirmados favorecem o regime de um objeto por cena num vídeo que roda sozinho: coerência ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 3.3) e efeito de informação transitória (WLMS: em animação, o que some antes de ser processado se perde; trechos longos de animação perderam a vantagem sobre imagens estáticas numa tarefa de dobradura, embora uma replicação com crianças não tenha achado o mesmo). Dois achados explicam como o painel denso pode funcionar também: MC acharam que dividir a aula em trechos que o aprendiz avança quando quer melhorou a transferência (não a lembrança), e quem pausa um Reel está controlando o ritmo; KACS mostram que o que ajuda o iniciante pode atrapalhar quem já sabe, e vice-versa, então um painel denso que o iniciante ignora pode ser o que prende o experiente.
- **Confiança:** confirmado para os princípios; a leitura de que o painel denso funciona porque quem quer pausa, e porque o detalhe não é preciso para seguir a fala, é inferência.
- **Para a skill:** no painel denso, a fala e o elemento que muda precisam bastar para entender sem pausar; o resto é camada para quem pausa. O meio-termo que o catálogo condena (rótulo da palavra dita, sem desenho do que acontece) é o pior dos dois: denso sem ser útil a quem pausa, e redundante com a fala ([texto-na-tela.md](texto-na-tela.md), 2.1).

### 6.2 Zonas fixas

- **Técnica do catálogo:** cada tipo de informação tem sempre o mesmo lugar (barra de progresso, cartão de capítulo, conteúdo, legenda) ([DdrHAI1MrFb](https://www.instagram.com/reel/DdrHAI1MrFb/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeCf1khst4y](https://www.instagram.com/reel/DeCf1khst4y/), [DeMxXXwM3K1](https://www.instagram.com/reel/DeMxXXwM3K1/), [DeNUYLkRWsz](https://www.instagram.com/reel/DeNUYLkRWsz/)).
- **Base:** sem estudo da técnica em vídeo. CJ: um arranjo repetido acelera a busca sem a pessoa perceber; HR: manter os mesmos mapeamentos entre estados; ROC: o que não muda libera a atenção para o que muda.
- **Confiança:** inferência a partir de achados confirmados.

### 6.3 Dado real para quem pausa

- **Técnica do catálogo:** interface verossímil, cabeçalho, hexadecimal, terminal ou código, coerentes entre si ([DdrHAI1MrFb](https://www.instagram.com/reel/DdrHAI1MrFb/), [Dd5BEPjI72b](https://www.instagram.com/reel/Dd5BEPjI72b/), [DeCf1khst4y](https://www.instagram.com/reel/DeCf1khst4y/), [DeNUYLkRWsz](https://www.instagram.com/reel/DeNUYLkRWsz/)). eusouosalmo decidiu que vale o custo.
- **Base:** sem base primária para o benefício. O que existe pesa contra quando o dado não serve à ideia: coerência e detalhe sedutor ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 3.3). O d = 0,76 de HL para animação realista é sobre o realismo de mostrar o próprio processo (vídeo), não sobre acrescentar dado de fundo, e não serve de base aqui.
- **Confiança:** sem base primária; a ressalva de coerência é confirmada.
- **Para a skill:** o dado real fica em zona secundária, sem movimento, e nunca disputa com o elemento que a fala explica naquele instante.

### 6.4 Código como prova ou sintoma

- **Técnica do catálogo:** uma linha que causa o problema, ou o código ruim digitado e marcado ([DbHPFy1s7ia](https://www.instagram.com/reel/DbHPFy1s7ia/), [DeKo7zLTrcd](https://www.instagram.com/reel/DeKo7zLTrcd/)).
- **Base:** sem base primária específica. É uma instância de duas coisas já confirmadas no repo: o concreto prende mais que o abstrato ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 2.6) e o rótulo perto do que se refere (contiguidade no espaço, [texto-na-tela.md](texto-na-tela.md), 4.5). Digitar o código no ritmo da fala é parente do desenho traço a traço (seção 4.5), com a mesma ressalva: sem mão visível, o efeito não foi significativo em FM.
- **Confiança:** sem base primária; vizinhança confirmada.

### 6.5 Fonte como print legível

- **Técnica do catálogo:** print real da fonte quando o dado vem da internet, sempre legível, nunca como selo ([DdcN3aKvW2C](https://www.instagram.com/reel/DdcN3aKvW2C/), [Ddjvq7TMpuD](https://www.instagram.com/reel/Ddjvq7TMpuD/)).
- **Base:** sem base primária encontrada sobre print de fonte em vídeo. A regra de eusouosalmo (legível, nunca selo) concorda com dois pontos do repo: um print ilegível não informa e vira enfeite, o que a coerência desaconselha ([psicologia-do-roteiro-curto.md](psicologia-do-roteiro-curto.md), 3.3); e a credibilidade vem de competência e confiabilidade, e o engano descoberto quebra a confiança (mesma nota, 5.1 e 5.3), o que pesa a favor de a fonte ser verificável.
- **Confiança:** sem base primária; inferência.

## 7. Quadro por técnica e o que muda para os tickets

Todas as técnicas marcadas "sim" nas seções Analogia, Animação e Densidade do catálogo:

| técnica | seção do catálogo | base primária | nível | já no repo? |
| - | - | - | - | - |
| troca de uma peça | Analogia | caso-âncora e ponte (CLE); diferença alinhável (MG); comparação de casos (ANS, GLT) | confirmado (mecanismo); relato forte (CLE) | novo |
| analogia em fila | Analogia | sistematicidade (GEN, CG); mapeamento dito (GH) | confirmado (mecanismo) | novo; liga a `psicologia` 3.2 |
| um objeto, dois estados | Analogia | diferença alinhável (MG); comparação (ANS); animação da mudança (PBB) | inferência | novo |
| mundo-metáfora | Analogia | metáfora estendida em texto: mista (THI, BBV a favor; SD, RBKS, SRB contra) | sem base primária para a forma visual | novo |
| máquina como colega | Analogia | antropomorfismo (ZG); emotional design (BSD); humor (BAN) | relato | novo |
| caso-limite literal | Analogia | exemplos divergentes (TP), por fonte secundária | sem base primária | vizinho de `psicologia` 2.4 e 2.6 |
| transformação contínua | Animação | transição animada contra estática (HR); cegueira à mudança (ROC); limite: cortes com ação contínua (MZ) | confirmado (rastrear objetos) | novo |
| palco fixo | Animação | ROC, HR, CJ | inferência | novo |
| objeto que muda de forma | Animação | congruência (TMB); animação representacional (HL); mudança relevante (PBB) | confirmado | novo |
| desenho traço a traço | Animação | ver desenhar com a mão visível (FM); lousa animada (TM) | confirmado com condição (mão visível) | novo |
| tela de impacto | Animação | nenhuma; vizinhos YJ, SBNR; limite WCAG 2.3.1 | sem base primária | vizinho de `texto` 4.3 e 4.4 |
| contador como relógio | Animação | nenhuma; vizinhos MAY (redundância), WLMS | sem base primária | vizinho de `texto` 2.1 |
| dois regimes de densidade | Densidade | coerência; informação transitória (WLMS); ritmo do aprendiz (MC); inversão por expertise (KACS) | confirmado (princípios); inferência (os dois regimes) | parte em `psicologia` 3.3 |
| zonas fixas | Densidade | CJ, HR, ROC | inferência | novo |
| dado real para quem pausa | Densidade | nenhuma a favor; coerência contra quando não serve | sem base primária | `psicologia` 3.3 (contra) |
| código como prova ou sintoma | Densidade | nenhuma específica; concreto, contiguidade | sem base primária | vizinho de `psicologia` 2.6, `texto` 4.5 |
| fonte como print legível | Densidade | nenhuma | sem base primária | vizinho de `psicologia` 3.3, 5.1 |

Fora do "sim", mas com achado: "destaque que segue a causa" (marcado "não") tem base confirmada (BL, OKKC); "família de analogias" (marcado "não") é diferente das múltiplas analogias de SPI e GH, que são várias bases para o mesmo conceito, enquanto a família é uma base para vários conceitos; "afirmação riscada" fica com o [ticket 54](https://github.com/eusouosalmo/skills/issues/54).

O que muda para os tickets de melhoria:

1. **Analogia na skill de roteiro:** a analogia diz em voz alta a correspondência de cada peça (GH), escolhe a base pela relação causal e não pela aparência (GEN), e diz onde a base quebra (GLY, SPI). Os três tipos com base mais firme são troca de uma peça, analogia em fila e um objeto em dois estados.
2. **Na `reel-motion`:** transformação contínua quando a fala liga um estado ao outro, corte quando começa um evento novo (HR, MZ); uma mudança por etapa nas transformações complexas (HR); manter a base da analogia visível enquanto o alvo entra (RZH).
3. **Desenho traço a traço:** a mão ou o lápis visível faz parte da técnica, não do estilo (FM).
4. **Cor:** reconsiderar "destaque que segue a causa" para teste (BL); a cor que segue a causa entra sincronizada com a palavra (BL, experimento 2).
5. **Sem base primária:** tela de impacto, contador, dado real, código como prova, fonte como print e caso-limite literal ficam como observação das referências. As baselines dos tickets de melhoria são a única evidência que vão ter.
