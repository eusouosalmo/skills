# Edição de vídeo com IA: do bruto ao Reel pronto

Resumo: hoje a edição de um talking-head vertical passa por quatro etapas manuais no CapCut (juntar os brutos, tirar takes ruins e silêncios, gerar legenda, acabamento com transições, zoom de abertura e efeitos sonoros), com a skill `reel-motion` no meio para as cenas de motion. A comunidade já resolve bem a primeira etapa, o corte bruto: todas as ferramentas maduras detectam silêncio por energia do áudio e retake por similaridade de texto entre frases vizinhas, mantendo o último take. Os limiares variam pouco (silêncio a partir de 0,15 a 1 s; similaridade de 0,6 a 0,85) e nenhuma traz lista de hesitações em pt-BR que preste. Onde todas falham é no gosto: ritmo, escolha de efeito sonoro, transição e zoom ficam ou em regras fixas sem fonte ("algo muda a cada 3 a 5 s") ou de fora; o único dado com vídeos curtos reais, correlacional, aponta que estímulo moderado engaja mais que excesso, e nenhuma fonte trata do punch-in em tela dividida, que a pesquisa de atenção sugere puxar o olho para o rosto e longe do diagrama. Um benchmark de 2026 com editores humanos confirma o padrão: os agentes passam nos testes técnicos e perdem no de qualidade, cortam num ritmo mais lento que o editor de referência e dizem que acertaram em 93% das execuções. Para o formato do CapCut, escrever um draft funciona na prática, mas o formato não é documentado, muda a cada versão e as versões 8.7 e 9.x passaram a recusar drafts criados fora do app; o caminho que funcionou foi criar o projeto vazio no CapCut, fechar o app e escrever dentro dele. Nenhuma biblioteca tem teste com CapCut 9.6 para Windows nem menciona o arquivo crypto_key_store.dat. Pesquisa de 2026-10-15. Não decide nada; a seção 5 propõe o desenho.

## Sumário

1. [Fontes e método](#1-fontes-e-método)
2. [Comunidade](#2-comunidade)
3. [Fundamentação acadêmica e de plataforma](#3-fundamentação-acadêmica-e-de-plataforma)
4. [Formato do projeto CapCut](#4-formato-do-projeto-capcut)
5. [Implicações para o desenho](#5-implicações-para-o-desenho)

## 1. Fontes e método

A situação estudada: vários arquivos brutos gravados em sequência, com retakes de frases incompletas ou erradas; o corte é feito no CapCut 9.6 para Windows, a legenda é gerada no CapCut, as cenas de motion saem da skill `reel-motion` (HTML renderizado, temporizado por timestamps de palavra do Whisper) e o acabamento volta ao CapCut. A pergunta: como transformar isso num pipeline de edição completo feito por agente, e onde ficam as aprovações do autor.

Para cada repositório, li o README e o código-fonte (clone raso em 2026-10-15), e não só a descrição. Estrelas e datas são as da API do GitHub nesse dia. Os limiares citados vêm do código, com o arquivo indicado. Cada achado leva um status: **Confirmado (fonte primária)** quando li a fonte que é dona da afirmação (código, artigo, documentação oficial); **Anedótico / não verificado** quando é relato de autor de ferramenta sem dado, alegação de marketing ou algo que li só por fonte secundária.

Comunidade (todas lidas no código):

| Sigla | Repositório | O que é | Licença | Estrelas, criação |
| - | - | - | - | - |
| VV | [vincentventalon/claude-code-video-editing-skill](https://github.com/vincentventalon/claude-code-video-editing-skill) | Skill de corte bruto, um script Python | MIT | 5, 2026-09 |
| YA | [yerinsabraham/video-edit-skill](https://github.com/yerinsabraham/video-edit-skill) | Skill de edição completa, 40 scripts, v0.9.2 | Apache-2.0 | 1, 2026-10 |
| KF | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 42 ferramentas FFmpeg com contrato e MCP, v2.10.1 | MIT | 1.957, 2026-09 |
| GW | [griffinwooldridge/talking-head-editor](https://github.com/griffinwooldridge/talking-head-editor) | Skill de corte, voz, legenda e motion graphics | MIT (arquivo LICENSE) | 4, 2026-10 |
| AE | [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | CLI de corte por silêncio, com skills | Unlicense | 5.526, 2020-04 |
| AW | [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | Lista de 180 repositórios de vídeo para agentes | sem licença declarada | 655, 2026-09 |
| LC | [louisedesadeleer/cut-video](https://github.com/louisedesadeleer/cut-video) | Skill de corte com alinhamento forçado (MFA) | MIT | 109, 2026-05 |
| HY | [hassancs91/claude-youtube-editor](https://github.com/hassancs91/claude-youtube-editor) | Pipeline de seis skills para YouTube, com passe de SFX | MIT | 332, 2026-07 |
| SC | [YeJe-cpu/SeeCut](https://github.com/YeJe-cpu/SeeCut) | Edição com revisão por modelo que assiste vídeo, saída em draft do JianYing | PolyForm Noncommercial 1.0.0 | 319, 2026-09 |
| SM | [mrbuslov/capcut-ai-editor](https://github.com/mrbuslov/capcut-ai-editor) | MCP que corta silêncio e take repetido dentro do projeto CapCut | MIT | 120, 2026-02 |

Formato CapCut (lidos no código e na documentação do repositório):

| Sigla | Repositório | Licença | Estrelas, versão |
| - | - | - | - |
| PCC | [GuanYixuan/pyCapCut](https://github.com/GuanYixuan/pyCapCut) | nenhum arquivo de licença; a API do GitHub devolve licença nula | 705, 0.0.3 |
| PJY | [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) | Apache-2.0 | 4.573, 0.3.1 |
| CLI | [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli) | MIT | 899, 0.29.0 |
| VCA | [sun-guannan/VectCutAPI](https://github.com/sun-guannan/VectCutAPI) | Apache-2.0 | 2.303 |
| MCP | [JmsLdrn/capcut-mcp](https://github.com/JmsLdrn/capcut-mcp) | MIT | 9 |
| SHI | [zxypro1/capcut-shell-inject](https://github.com/zxypro1/capcut-shell-inject) | MIT | 1 |

Pesquisa acadêmica e plataformas (fonte primária; quando li só o resumo ou uma fonte secundária, está dito):

| Sigla | Fonte |
| - | - |
| BLA | Berthouzoz, F., Li, W. e Agrawala, M. (2012). [Tools for placing cuts and transitions in interview video](http://vis.berkeley.edu/papers/vidtrans/). ACM TOG 31(4), SIGGRAPH 2012, 67:1 a 67:8. [doi:10.1145/2185520.2185563](https://doi.org/10.1145/2185520.2185563). Li o artigo ([PDF](http://vis.berkeley.edu/papers/vidtrans/vidtrans.pdf)). |
| RUB | Rubin, S., Berthouzoz, F., Mysore, G., Li, W. e Agrawala, M. (2013). [Content-based tools for editing audio stories](http://vis.berkeley.edu/papers/audiostories/). UIST 2013. Li o artigo ([PDF](http://vis.berkeley.edu/papers/audiostories/audiostories.pdf)). |
| LDTA | Leake, M., Davis, A., Truong, A. e Agrawala, M. (2017). [Computational video editing for dialogue-driven scenes](https://graphics.stanford.edu/papers/roughcut/). ACM TOG 36(4), SIGGRAPH 2017. Li o resumo na página do projeto. |
| LAVE | Wang, B. et al. (2024). [LAVE: LLM-powered agent assistance and language augmentation for video editing](https://arxiv.org/abs/2402.10294). IUI 2024. Li o resumo. |
| EXE | Tilekbay, B. et al. (2024). [ExpressEdit: video editing with natural language and sketching](https://arxiv.org/abs/2403.17693). IUI 2024. Li o resumo. |
| TLK | Benharrak, K., Peng, P. e Pavel, A. (2025). [TalkLess: blending extractive and abstractive speech summarization for editing speech to preserve content and style](https://arxiv.org/abs/2507.15202). UIST 2025. Li o resumo. |
| TLB | Gupta, G., Arora, N. e Tankala, P. K. (2026). [Timeline-Bench: evaluating agents on realistic video-editing tasks, from raw footage to final cut](https://arxiv.org/abs/2609.35143). Preprint, em revisão. Li a versão HTML. |
| CV | Campione, E. e Véronis, J. (2002). [A large-scale multilingual study of silent pause duration](https://www.isca-archive.org/speechprosody_2002/campione02_speechprosody.pdf). Speech Prosody 2002. Li o resumo e o início do artigo. |
| MCD | MacGregor, L. J., Corley, M. e Donaldson, D. I. (2010). [Listening to the sound of silence: disfluent silent pauses in speech have consequences for listeners](https://research-portal.st-andrews.ac.uk/en/publications/listening-to-the-sound-of-silence-disfluent-silent-pauses-in-spee/). Neuropsychologia 48(14), 3982 a 3992. Li só trechos do resumo. |
| GER | Gernsbacher, M. A. (2015). [Video captions benefit everyone](https://pmc.ncbi.nlm.nih.gov/articles/PMC5214590/). Policy Insights from the Behavioral and Brain Sciences 2(1), 195 a 202. Li o resumo (PubMed 28066803). |
| LZ | Lang, A., Zhou, S., Schwartz, N., Bolls, P. D. e Potter, R. F. (2000). [The effects of edits on arousal, attention, and memory for television messages](https://scholars.cityu.edu.hk/en/publications/the-effects-of-edits-on-arousal-attention-and-memory-for-televisi/). Journal of Broadcasting & Electronic Media 44(1), 94 a 109. Li o resumo. |
| LBPK | Lang, A., Bolls, P., Potter, R. F. e Kawahara, K. (1999). The effects of production pacing and arousing content on the information processing of television messages. Journal of Broadcasting & Electronic Media 43(4), 451 a 475. Não li; conforme [Niederdeppe (2005)](https://www.uky.edu/~ngrant/CJT780/readings/Day%2010/Niederdeppe2005.pdf), que o resume. |
| PLB | Potter, R. F., Lang, A. e Bolls, P. D. (2008). Identifying structural features of audio: orienting responses during radio messages and their impact on recognition. Journal of Media Psychology 20(4), 168 a 177. Não li; conforme a [revisão no Journal of Cognition](https://journalofcognition.org/articles/43) que o cita. |
| NNG | Pernice, K. (2017). [The talking-head video 2.0: findings from eyetracking research](https://www.nngroup.com/articles/talking-head-video/). Nielsen Norman Group. Estudo de usabilidade sem número de participantes publicado. |
| DSC | Descript, [Shorten word gaps](https://help.descript.com/hc/en-us/articles/10164807277453-Shorten-word-gaps) e [Underlord](https://help.descript.com/hc/en-us/articles/36803785502221-Underlord-beta-Your-AI-co-editor-in-Descript). Documentação oficial. |
| YT-VOL | YouTube Help, [Control video volume on your device](https://support.google.com/youtube/answer/14106294?hl=en&co=GENIE.Platform%3DDesktop). Documentação oficial. |
| KPS | Kizilcec, R. F., Papadopoulos, K. e Sritanyaratana, L. (2014). Showing face in video instruction: effects on information retention, visual attention, and affect. CHI 2014, 2095 a 2102. [doi:10.1145/2556288.2557207](https://doi.org/10.1145/2556288.2557207). Não li; conforme o resumo que KBG faz do próprio estudo. |
| KBG | Kizilcec, R. F., Bailenson, J. N. e Gomez, C. J. (2015). [The instructor's face in video instruction: evidence from two large-scale field studies](https://vhil.stanford.edu/publications/learning/instructors-face-video-instruction-evidence-two-large-scale-field-studies). Journal of Educational Psychology 107(3), 724 a 739. [doi:10.1037/edu0000013](https://doi.org/10.1037/edu0000013). Li o artigo. |
| WA | Wang, J. e Antonenko, P. D. (2017). [Instructor presence in instructional video: effects on visual attention, recall, and perceived learning](https://kb.wisconsin.edu/images/group455/121077/1-s2.0-S0747563217300638-main.pdf). Computers in Human Behavior 71, 79 a 89. [doi:10.1016/j.chb.2017.01.049](https://doi.org/10.1016/j.chb.2017.01.049). Li o artigo. |
| ZXPY | Zhang, Y., Xu, K., Pi, Z. e Yang, J. (2022). [Instructor's position affects learning from video lectures in Chinese context: an eye-tracking study](https://ideas.repec.org/a/taf/tbitxx/v41y2022i9p1988-1997.html). Behaviour & Information Technology 41(9), 1988 a 1997. Li o resumo. |
| PH | Pi, Z. e Hong, J. (2016). [Learning process and learning outcomes of video podcasts including the instructor and PPT slides: a Chinese case](https://doi.org/10.1080/14703297.2015.1060133). Innovations in Education and Teaching International 53(2), 135 a 144. Não consegui ler nem o resumo (página do editor fechada). |
| YJ | Yantis, S. e Jonides, J. (1984). [Abrupt visual onsets and selective attention: evidence from visual search](https://doi.org/10.1037/0096-1523.10.5.601). JEP: Human Perception and Performance 10(5), 601 a 621; e Yantis e Jonides (1990), [Abrupt visual onsets and selective attention: voluntary versus automatic allocation](https://doi.org/10.1037/0096-1523.16.1.121), mesma revista, 16(1), 121 a 134. Li os resumos (Europe PMC). |
| FS | Franconeri, S. L. e Simons, D. J. (2003). [Moving and looming stimuli capture attention](https://doi.org/10.3758/bf03194829). Perception & Psychophysics 65(7), 999 a 1010. Li o resumo (Europe PMC). |
| GLTS | Glaser, M., Lengyel, D., Toulouse, C. e Schwan, S. (2017). [Designing computer-based learning contents: influence of digital zoom on attention](https://doi.org/10.1007/s11423-016-9495-9). Educational Technology Research and Development 65(5), 1135 a 1151. Li só trechos do resumo citados em buscas; o artigo é fechado. |
| MM | Moreno, R. e Mayer, R. E. (2000). [A coherence effect in multimedia learning: the case for minimizing irrelevant sounds in the design of multimedia instructional messages](https://tecfa.unige.ch/tecfa/teaching/methodo/Moreno_Mayer00.pdf). Journal of Educational Psychology 92(1), 117 a 125. Li o artigo. |
| VDB | Van der Burg, E., Olivers, C. N. L., Bronkhorst, A. W. e Theeuwes, J. (2008). [Pip and pop: nonspatial auditory signals improve spatial visual search](https://doi.org/10.1037/0096-1523.34.5.1053). JEP: Human Perception and Performance 34(5), 1053 a 1065. Li o resumo (Europe PMC). |
| MSV | Xue, H., Zhang, J., Wang, X., Kim, D. D. e Song, Y. (2026). [A computational model of message sensation value in short video multimodal features that predicts sensory and behavioral engagement](https://arxiv.org/abs/2604.19995). Preprint. Li o artigo. |
| SKR | Škripcová, L. (2026). [Watching TikTok: an eye-tracking study of visual attention paid to short-form videos](https://communicationtoday.sk/watching-tiktok-an-eye-tracking-study-of-visual-attention-paid-to-short-form-videos/). Communication Today 17(1). Li o resumo na página da revista. |
| TT-QT | TikTok for Business, [Level up your creative to captivate your audience](https://ads.tiktok.com/business/creativecenter/quicktok/online/Level-up_your_creative_to_captivate_your_audience/pc/en) (QuickTok, 2022-12-19). Documentação oficial para anunciantes. |

As notas [texto-na-tela.md](texto-na-tela.md) (legenda e texto sobreposto) e [analogia-e-animacao-sincronizada.md](analogia-e-animacao-sincronizada.md) (corte contra transformação contínua) já cobrem parte da seção 3; o que está lá não é repetido aqui.

## 2. Comunidade

### 2.1 vincentventalon/claude-code-video-editing-skill (VV)

- **Como divide o pipeline:** um comando só (`scripts/edit_video.py`) junta os clipes, divide o áudio em "ilhas" de som entre silêncios, transcreve cada ilha com whisper.cpp, descarta ilhas sem fala, só hesitação ou que são falso começo, renderiza o mp4 e escreve `.txt`, `.srt` e `edited.takes.tsv` com cada ilha, mantida ou não, e o texto dela.
- **Determinístico contra julgamento:** o script decide sozinho os cortes óbvios. O SKILL.md manda o agente "ler os takes como um editor" no `.tsv` e procurar o que o script não vê: frase abandonada e dita de novo com outras palavras, fragmento solto. O agente corrige com `--cut A:B` e `--protect A:B`, sem retranscrever. Regra explícita: "In doubt, keep", porque uma repetição que fica custa um segundo passe e uma frase perdida custa o vídeo.
- **Aprovação:** nenhuma etapa formal; o agente entrega o vídeo, o que cortou e por quê, e os trechos "to check".
- **Silêncio e retake (no código):** silêncio a partir de 0,22 s a -32 dB separa ilhas e é cortado; sobram 0,05 s antes e 0,07 s depois de cada ilha, então a pausa final fica perto de 0,12 s. Falso começo: um trecho cujo texto é o começo do que vem logo depois (similaridade de sequência ≥ 0,74 no início da frase seguinte, janela de 10 s e até 6 ilhas); o comentário no código diz que o 0,74 foi medido em gravação real ("true false starts 0.75-1.00, a sentence that simply goes on with a similar opening 0.71"). Para ilhas vizinhas, também conta as três primeiras palavras iguais ou similaridade ≥ 0,85. Mantém o último take. Corte com fade de 10 ms para não estalar, alinhado ao frame.
- **Legenda:** SRT de até 8 palavras por bloco, sem queimar no vídeo.
- **Saída:** mp4 (H.264 CRF 20, AAC 192k), SRT e TSV. Sem EDL, sem draft de editor.
- **Idioma:** listas de hesitação e de palavras de ligação só para fr, en, es e de. Em pt-BR, a detecção de "só hesitação" não funciona e a de falso começo perde o tratamento das palavras de entrada ("então", "e").
- **Maturidade:** o README diz que é o motor de corte simplificado do pipeline pessoal do autor (1.400 linhas e trinta scripts), usado num vídeo por dia desde agosto de 2026. O que não faz: legenda queimada, capa, música, b-roll.
- **Status:** Confirmado (fonte primária) para o código; o uso diário é Anedótico / não verificado.

### 2.2 yerinsabraham/video-edit-skill (YA)

- **Como divide:** um orquestrador (`edit.py`) em 8 passos (ingest, transcribe, takes, look, assemble, autoedit, render, qa), com retomada a partir de qualquer passo (`--from`). Cada nota do autor vira um comando mapeado numa tabela ("captions bigger" vira `captions.py --size 1.2`).
- **Determinístico contra julgamento:** quase tudo é regra fixa em `editing-rules.md`, aplicada sem perguntar: punch-in de 1,15 a 1,2x numa palavra-chave, push-in lento de 1,0 a 1,1x, nunca dois punch-ins seguidos, zoom máximo de 1,25x; "a visual change every 3-5 seconds"; whoosh quando um gráfico entra, pop em logo, SFX de 12 a 20 dB abaixo da voz, nunca mais de um SFX por meio segundo; mix normalizado a -14 LUFS para vídeo curto. O texto atribui as regras a "studying edits that hold attention", sem fonte.
- **Aprovação:** opcional. Com clipes fora de ordem, roda `--until takes`, mostra a ordem das falas e a tabela de takes e espera; no caso normal, renderiza e depois relata.
- **Retake e silêncio (`takes.py`, `edl.py`):** divide cada clipe em orações pela pontuação do Whisper, agrupa orações com similaridade ≥ 0,62 como takes da mesma fala, escolhe por pontuação (penaliza hesitação, palavra repetida em seguida, pausa interna > 0,9 s e oração cortada) e, no empate, o take gravado por último. Pausa entre falas até 0,5 s fica, acima disso vira corte; folga de 0,08 s. Também move o CTA para o fim automaticamente.
- **Legenda:** queimada, palavra por palavra, com "looks" prontos.
- **Saída:** mp4 e um EDL em texto simples (`export_nle.py`), sem draft de editor.
- **Idioma:** o modelo padrão de transcrição é `small.en` (só inglês) e as hesitações estão em inglês.
- **Maturidade:** v0.9.2, criado em 2026-10-04, uma estrela.
- **Status:** Confirmado (fonte primária) para o código e as regras; a eficácia das regras de ritmo e SFX é Anedótica / não verificada.

### 2.3 kajisho5/ffmpeg-skill (KF)

- **Como divide:** é "as mãos", não "o cérebro", nas palavras do README: corta, mede e exporta, e devolve JSON. Não decide o que cortar nem aprova entrega; isso fica para outros repositórios do mesmo autor.
- **Determinístico contra julgamento:** tudo determinístico. Cada ferramenta é um script com argumentos tipados, nenhuma string de shell nem filtergraph vindo do agente, e um contrato legível por máquina derivado do próprio argparse.
- **Silêncio:** `silence.py` com -35 dBFS, silêncio mínimo de 0,6 s e margem de 0,15 s de cada lado. Remoção de hesitação opcional com transcrição local. Não detecta retake.
- **Legenda:** queimada, com animação e karaokê; o texto dado é queimado como está, sem reescrever.
- **Saída:** mp4 com presets por plataforma. A tabela de plataformas põe Reels, Shorts e TikTok a -14 LUFS e -1 dBTP, sem citar fonte.
- **Idioma:** hesitações em pt só "é" e "hum".
- **Maturidade:** a mais testada da lista: CI com FFmpeg 5.1 a 9, Python 3.9 e 3.13, 53 demos reproduzíveis.
- **Status:** Confirmado (fonte primária).

### 2.4 griffinwooldridge/talking-head-editor (GW)

- **Como divide:** voz (DeepFilterNet, EQ e -14 LUFS), transcrição, escolha de take, corte, plano de motion graphics, reenquadramento, cenas como código (HyperFrames), legenda e composição.
- **Determinístico contra julgamento:** o agente lê o transcript numerado e escreve `keep.json` à mão, com faixas de índices de palavra: mantém o último take completo, tira falso começo, "..." no fim, falas repetidas, hesitação e o que foi dito para a equipe. Pode reordenar. O corte em si é determinístico.
- **Silêncio (`references/cutting.md`):** dentro de uma faixa mantida, qualquer pausa acima de 0,15 s sai e vira cerca de 0,09 s (0,03 s antes e 0,06 s depois). O ponto de saída anda além do fim que o Whisper marca até o nível ficar 12 dB acima do ruído por 30 ms, e olha mais 250 ms por uma sílaba final fraca que volta depois de uma queda ("-ence", "-ts"); o ponto de entrada volta até 150 ms em consoantes aspiradas. Quando dois pedaços vizinhos pulam de posição, põe punch-in ou motion graphic por cima da emenda.
- **Aprovação:** o passo 8 manda retranscrever o vídeo final e comparar com o `keep.json` (nenhuma palavra faltando ou dobrada) e olhar cada emenda; não há pausa formal para o autor.
- **Legenda:** HTML renderizado com alpha, temporizado por palavra.
- **Saída:** mp4. Padrão 1920x1080, idioma fixo em inglês no código (`language='en'`, modelo `small.en`).
- **Maturidade:** criado em 2026-10-08, quatro estrelas.
- **Status:** Confirmado (fonte primária).

### 2.5 WyattBlue/auto-editor (AE)

- **Como divide:** CLI que marca cada trecho como ativo ou inativo (por áudio, movimento ou legenda) e aplica uma ação a cada classe (cortar, acelerar, mudar volume, zoom).
- **Determinístico:** todo. Não há julgamento de agente; as quatro skills do repositório ensinam a usar a CLI.
- **Silêncio:** padrão `audio:threshold=0.04` (4% da amplitude) e margem de 0,2 s antes e depois. `--edit subtitle` corta pelo conteúdo da fala, por palavra ou regex, depois de transcrever com o subcomando `whisper` (whisper.cpp ou Parakeet).
- **Retake:** não detecta.
- **Saída:** mídia renderizada, ou projeto para Premiere (XML FCP7), DaVinci Resolve e Final Cut Pro (FCPXML), Shotcut (MLT), Kdenlive, ou clipes separados. Não exporta para CapCut.
- **Maturidade:** desde 2020, 5.526 estrelas, versão 31.7.3, atualizado em 2026-10-14.
- **Status:** Confirmado (fonte primária).

### 2.6 Outros da lista awesome-claude-video-skills (AW)

A lista tem 41 repositórios de edição. Os mais próximos do caso, lidos no README e no SKILL.md:

- **louisedesadeleer/cut-video (LC).** Corta por fronteiras de palavra do Montreal Forced Aligner, com precisão de 10 a 20 ms segundo o autor, e não pelos timestamps do Whisper, que ele mede como ±100 a 300 ms e com pausas embutidas na duração da palavra. Lição registrada: em gravação cheia de retakes, o Whisper junta as repetições numa só e o alinhamento escorrega de 1 a 6 s na segunda metade; por isso cada fronteira é conferida retranscrevendo uma janela isolada. Palavra curta com duração acima de cerca de 1 s marca uma pausa ou um retake inteiro escondido. O limiar de silêncio é calibrado no ruído da própria gravação (piso + 6 dB), porque um -30 dB fixo deixou passar pausas de 8 s com um microfone de lapela ruidoso. Tabela de pausas por modo: no agressivo, de 0,25 a 1 s vira 0,1 s e acima de 1 s vira 0,2 s; no "balanced", 0,3 s e 0,5 a 0,8 s. Retake: 4-gramas com similaridade > 0,7 numa janela de 60 s, mais as 3 a 5 primeiras palavras; mantém o último take, a não ser que esteja incompleto. Todo grupo de retake aparece no plano para o autor trocar o take. Saída: mp4 "pronto para o CapCut". macOS. **Status:** Confirmado (fonte primária) para o método; as medidas de drift são Anedóticas (um caso relatado pelo autor).
- **hassancs91/claude-youtube-editor (HY).** Seis skills: corte (o agente escreve `cuts.json` a partir do transcript da AssemblyAI), visuais em Remotion, limpeza de voz, SFX, thumbnail, upload. O passe de SFX é "function-first" (o som pelo papel: movimento, tensão, ênfase), cai na palavra exata, usa uma biblioteca que cresce a cada vídeo (clipes normalizados a cerca de -20 LUFS) e tem uma etapa de auditoria do autor obrigatória antes da mixagem. Lições registradas: efeito curto percussivo precisa de 3 a 5 dB a mais que o sustentado; efeito embaixo de fala contínua não se ouve com o ducking ligado, então ou vai nas pausas ou sai; textura ruidosa não se conserta com ganho. Transições e zoom ainda estão no roadmap. Depende de APIs pagas (AssemblyAI, ElevenLabs). **Status:** Confirmado (fonte primária) para o processo; as lições de ganho são Anedóticas.
- **YeJe-cpu/SeeCut (SC).** Usa o Gemini, que assiste o vídeo com movimento, para entender o bruto e revisar o próprio corte. Relato do autor: a nota absoluta do juiz era instável e a comparação entre duas versões era confiável, então cada revisão é par a par, rodada duas vezes com a ordem trocada, e uma versão só vence se ganhar nas duas. No máximo 3 versões por vídeo; uma amostra de 25 s leva cerca de uma hora. Saída opcional em draft do JianYing por um motor de terceiros com licença não comercial. Só macOS. Licença do próprio repositório também não comercial. **Status:** Confirmado (fonte primária) para o método; a calibração do juiz é Anedótica (não publicaram os dados).
- **mrbuslov/capcut-ai-editor (SM).** O mais parecido com o fluxo atual do autor: lê a legenda automática que o próprio CapCut gerou, corta pausas acima de 1 s entre legendas e remove repetições mantendo a última, direto no projeto. Exige o CapCut fechado e avisa que edita no lugar, sem backup. **Status:** Confirmado (fonte primária) para o README; não li o código.

### 2.7 Quadro comparativo

| | VV | YA | KF | GW | AE | LC | SM |
| - | - | - | - | - | - | - | - |
| Silêncio | ≥ 0,22 s, -32 dB | > 0,5 s | ≥ 0,6 s, -35 dB | > 0,15 s | 4% amplitude | piso + 6 dB | > 1 s entre legendas |
| Pausa que sobra | ~0,12 s | até 0,5 s | 0,3 s (margens) | ~0,09 s | 0,4 s (margens) | 0,1 a 0,8 s por modo | não diz |
| Retake | começo igual ≥ 0,74 | similaridade ≥ 0,62 + nota | não | agente decide | não | 4-grama > 0,7 em 60 s | repetição |
| Take mantido | último | melhor nota; último no empate | | último completo | | último salvo se incompleto | último |
| pt-BR | não | não (small.en) | mínimo | não (en fixo) | sim (Whisper) | não testado | depende do CapCut |
| Saída | mp4 + SRT | mp4 + EDL texto | mp4 | mp4 | mp4, XML, FCPXML | mp4 | draft CapCut |
| Aprovação do autor | não | opcional | não | não | não | plano mostrado | não |

O capcut-cli (seção 4) também tem `detect-silence` (-30 dB, 0,5 s, folga de 0,1 s) e `detect-retakes` (janela de 60 s, similaridade ≥ 0,8, mínimo de 4 palavras, mantém o take posterior). **Status:** Confirmado (fonte primária), em `src/silence.ts` e `src/retakes.ts`.

### 2.8 Onde falham ou o que não cobrem

- **Retake dito com outras palavras.** Toda detecção é por similaridade de texto; frase reformulada passa. VV assume isso no SKILL.md e põe o agente para ler; GW deixa toda a escolha com o agente. **Status:** Confirmado (fonte primária).
- **O Whisper esconde retake.** LC mediu o Whisper juntando repetições e a deriva de tempo que isso causa; ferramentas que cortam pelo timestamp do Whisper herdam o erro. **Status:** Anedótico / não verificado (um caso relatado).
- **pt-BR.** Nenhuma ferramenta tem lista de hesitações em português que cubra o comum ("né", "tipo", "éé", "então") nem palavras de entrada de retake. Duas fixam inglês no código. **Status:** Confirmado (fonte primária).
- **Gosto.** Ritmo, transição, zoom e SFX ou são regras fixas sem fonte (YA), ou relatos de ajuste (HY), ou ficam de fora (VV, KF, AE, LC). Nenhuma mede o resultado contra um editor humano; a única avaliação com humanos é a de TLB (seção 3.2). **Status:** Confirmado (fonte primária) para a ausência.
- **CapCut.** Só SM e SC entregam projeto editável num editor da ByteDance; as demais entregam mp4 e esperam que o autor importe. **Status:** Confirmado (fonte primária).

## 3. Fundamentação acadêmica e de plataforma

### 3.1 Edição pela transcrição

- **O que é:** BLA liga o transcript à filmagem: o editor apaga o texto e o corte acontece no vídeo. O sistema mostra a "adequação ao corte" de cada ponto, calculada onde o entrevistado está relativamente quieto e parado, e gera para cada corte uma transição visível (jump cut, fade) e uma escondida (interpolação entre quadros parecidos). Também remove "ums" e palavras repetidas num clique e insere pausas com aparência natural para dar ênfase. A avaliação foi de cinco vídeos editados pelos próprios autores, de 50 a 100 s; em cerca de 10% dos cortes eles preferiram a transição visível ou desistiram do corte. Não há estudo com usuários. RUB faz o mesmo para áudio: transcript ligado à fala, "ums" e palavras repetidas em vermelho, respirações e pausas marcadas como símbolos no texto, e frases parecidas agrupadas para escolher o take. LDTA escolhe, para cada fala, o melhor clipe entre vários takes de uma cena de diálogo, segundo idiomas de montagem que o usuário combina, codificados como modelos de Markov ocultos; gera a montagem de uma cena curta em 2 a 3 s. DSC é a versão comercial: Shorten word gaps encurta pausas pela regra "maior que X" ou "entre X e Y", com 200 ms como exemplo de alvo, e o usuário revê um por um ou aplica todos; o Underlord, agente da Descript, tem "cut retakes" entre as ações.
- **Por que importa:** o fluxo "ler o texto, apagar a frase ruim" que o autor faz no CapCut é exatamente o modelo dessa linha de pesquisa desde 2012, e o padrão de mostrar o grupo de takes para o humano escolher já está em RUB.
- **Status:** Confirmado (fonte primária) para BLA e RUB (artigos lidos), LDTA (resumo) e DSC (documentação). A qualidade das transições de BLA não foi medida com espectadores.

### 3.2 Edição com LLM e agentes (2024 a 2026)

- **O que é:** LAVE gera descrições em linguagem do material bruto, e um agente com LLM planeja e executa ações de edição; o usuário pode editar pelo agente ou direto na interface, refinando o que o agente fez (estudo com 8 participantes). EXE interpreta comando em linguagem natural e desenho sobre o quadro para achar o trecho, a região e a operação (estudo observacional com 10). TLK gera candidatos de edição do transcript, escolhe para maximizar compressão, cobertura e qualidade de áudio, e separa na interface a edição de palavras da edição de conteúdo; reduziu carga cognitiva e esforço contra uma abordagem extrativa (N = 12). TLB é o mais relevante: 56 tarefas reais do bruto ao vídeo final (inclusive escolher takes de diálogo e montar entrevista), 16 agentes com Claude Code, Codex e OpenCode, e um teste de qualidade calibrado em 2.582 julgamentos às cegas de 43 editores de vídeo. O melhor agente resolve 26,8% das tarefas; a média, 14%. Das 771 execuções não resolvidas, 562 passaram em todos os outros testes e falharam só no de qualidade. Os agentes cortam a 0,72 vezes o ritmo da edição de referência, percebem o material por quadros parados e transcript, conferem o render atrás de defeito técnico e não de ritmo ou história, e dizem ter acertado em 93% das execuções, inclusive em 95,5% das que falharam num teste. Deixar slate, conversa de equipe ou retake aparece em 1,4% das derrotas dos seis melhores agentes e em 18,5% das do agente que opera a interface gráfica.
- **Por que importa:** a parte mecânica do corte bruto (retake, silêncio, emenda) é onde agentes já vão bem; ritmo e acabamento são onde perdem, e o agente não percebe que perdeu. Isso pede o veredito do autor justamente no ritmo, e não confiar na autoavaliação.
- **Status:** Confirmado (fonte primária) para TLB (preprint, ainda sem revisão por pares; a confiança é a de um preprint). Confirmado pelo resumo para LAVE, EXE e TLK.

### 3.3 Detecção de retake e falso começo

- **O que é:** RUB agrupa as frases do transcript por distância de Levenshtein menor que metade do comprimento da frase mais longa (as frases podem diferir em cerca de metade dos caracteres) e trata cada componente conexo como um grupo de takes; o produtor escolhe. As ferramentas da seção 2 usam a mesma ideia com limiares parecidos (0,6 a 0,85 de similaridade), mais dois sinais: o falso começo é o início de uma frase que se repete logo depois (VV), e uma fronteira de retake costuma vir depois de pausa longa, respiração, clique ou palavra de slate como "de novo" (LC). Ninguém usa sinal visual (olhar para fora, mudança de postura) para detectar take ruim.
- **Por que importa:** a regra "mantém o último take completo" é consenso entre ferramentas, mas é heurística; LC e YA registram a exceção (último take incompleto ou pior).
- **Status:** Confirmado (fonte primária) para os métodos; não encontrei estudo que compare os limiares ou meça acerto em pt-BR. Um fornecedor comercial (TimeBolt) anuncia F1 de 90,6% num benchmark próprio, Anedótico / não verificado.

### 3.4 Quanto de pausa manter entre frases

- **O que é:** na fala real, CV mediu cerca de 6.000 pausas em cinco línguas (sem português) e achou três grupos: breves (< 200 ms), médias (200 a 1.000 ms) e longas (> 1.000 ms), estas só na fala espontânea. RUB usa 250 ms como pausa padrão entre frases ao montar e reinsere a respiração antes da frase seguinte, citando o manual de rádio de Abel e Glass: quem fala respira e pausa antes de cada frase nova, e a pausa dá ênfase e tempo de pensar no que foi dito. MCD achou que palavras ditas depois de uma pausa silenciosa foram mais reconhecidas depois, num teste de memória surpresa. As ferramentas deixam de 0,09 s (GW) a 0,5 s (YA).
- **Por que importa:** a pausa entre frases não é só ar morto: há indício de que ela marca a fronteira e ajuda a guardar o que vem depois. Cortar tudo a 0,09 s junta frases que o espectador precisa separar.
- **Status:** Confirmado (fonte primária) para CV e RUB; MCD confirmado pelo resumo. Não encontrei estudo sobre quanta pausa manter em vídeo curto, nem sobre retenção em função da pausa; todo número das ferramentas é escolha de autor. LC diz que a tabela agressiva reproduz o ritmo de um vídeo de referência (mediana de corte de 1,13 s), Anedótico.

### 3.5 Legenda: compreensão e retenção

- **O que é:** GER resume mais de 100 estudos: legenda na mesma língua melhora compreensão, atenção e memória do vídeo, com benefício maior para quem assiste em segunda língua, quem está aprendendo a ler e pessoas surdas ou com deficiência auditiva. Os números de plataforma (Facebook: +12% de tempo de visualização em anúncios com legenda, em teste interno) e o efeito da legenda sobre o olhar estão em [texto-na-tela.md](texto-na-tela.md), seções 2.4 e 5.2.
- **Status:** Confirmado (fonte primária) para GER pelo resumo; os números de plataforma são dado da própria plataforma sobre anúncio, sem verificação independente.

### 3.6 Cortes, zoom, ritmo e efeitos sonoros

- **Cortes:** LZ variou a taxa de edição (troca de câmera dentro da mesma cena) e achou que, quanto mais edições, maior a excitação fisiológica e a autorrelatada e maior a memória, sem aumento grande de carga cognitiva. LBPK, no modelo de capacidade limitada, prevê que ritmo de produção e conteúdo excitante aumentam atenção e memória até um ponto de sobrecarga, depois do qual a memória cai. **Status:** Confirmado pelo resumo para LZ; LBPK por fonte secundária. Os estudos são de TV com adultos em laboratório; a passagem para Reels é inferência.
- **Zoom (punch-in):** não achei estudo controlado sobre zoom num talking-head. NNG observou, por eyetracking, que vídeo em que só mexem lábios e olhos entedia, e que mudança de expressão, posição ou ângulo de câmera traz a atenção de volta. GLTS é o estudo mais próximo: em clipes de reconstrução 3D com zoom digital mínimo, o zoom-in aumentou a coerência do olhar entre espectadores e o tempo no centro da imagem e reduziu as idas e vindas entre o centro e o entorno; o zoom-out se comportou como a imagem parada, e não como o oposto do zoom-in. As regras de zoom de YA (1,15 a 1,2x, nunca dois seguidos, máximo 1,25x) e de GW (130% em pausas longas ou ênfase; zoom para esconder jump cut) são escolhas de autor. **Status:** GLTS confirmado só por trechos do resumo (não sei a escala usada nem se houve medida de aprendizagem); o resto Anedótico / não verificado.
- **Por que o zoom puxa o olho:** o aparecimento abrupto de um objeto captura a atenção mesmo quando não é relevante para a tarefa (YJ 1984); a captura, porém, não é total: quando a atenção já está focada num lugar, o aparecimento abrupto não necessariamente a arranca de lá (YJ 1990). FS mostrou que um objeto que se expande (looming) e um que se desloca também capturam a atenção, e um que encolhe não; os autores especulam que é porque a expansão sinaliza algo que exige reação. Um punch-in é exatamente isso: uma mudança abrupta em que o rosto cresce. **Status:** Confirmado pelo resumo para YJ e FS. São experimentos de busca visual com estímulos simples; aplicar a vídeo é inferência.
- **Punch-in em tela dividida:** nenhuma fonte estuda zoom no rosto com um painel de diagrama na mesma tela, nem em vídeo curto; procurei em eyetracking de vídeo educacional, nos estudos sobre presença do instrutor, nas bases de atenção e em material de criadores. A evidência indireta aponta numa direção só. (1) O rosto já ganha atenção desproporcional ao tamanho: em WA (N = 36, aulas de matemática com o instrutor em picture-in-picture), o instrutor ocupava cerca de 7% da tela e recebeu 22 a 26% do tempo de olhar; KPS, pelo resumo de KBG, achou 41% do tempo no rosto e troca de olhar entre rosto e slide a cada 3,7 s, sem efeito na lembrança. Num Reel dividido o rosto ocupa metade da tela, bem mais que nesses estudos. (2) WA conclui que no tema difícil o ganho do instrutor sumiu, e atribui isso à atenção dividida entre o conteúdo e o vídeo do instrutor; ZXPY achou que o instrutor no meio da tela puxou mais olhar para si, menos para o conteúdo e mais trocas entre os dois. (3) KBG testou mostrar o rosto só em alguns momentos, para avisar quando olhar os slides: a carga cognitiva subiu em relação a mostrar o rosto sempre, sem diferença em aprendizagem ou abandono, e os autores lembram que alternar a imagem tem um custo de troca parecido com o da contiguidade espacial. (4) O princípio de sinalização de Mayer pede que a pista aponte para o elemento relevante (WA trata os gestos do instrutor como sinalização nesse sentido). Somando: um punch-in no rosto em tela dividida é uma pista que aponta para o rosto. Quando a informação nova da frase está no diagrama, ele compete com o diagrama; quando a frase é a ideia e o diagrama está parado ou repete o que já foi visto, nada nos estudos o contraria. SKR (N = 16, TikTok) achou que formatos de várias telas produzem um modo de atenção "segmentado", com troca rítmica entre as partes e sem sinal de colapso de atenção, mas não separa zoom nem rosto. PH (instrutor e slides, com eyetracking) é o estudo mais parecido com a pergunta, e não consegui ler. **Status:** não abordado diretamente; a conclusão é inferência a partir de WA e KBG (artigos lidos), KPS (secundária, via KBG), ZXPY e SKR (resumo), YJ e FS (resumo). Todos os estudos são de aula longa ou laboratório, com adultos e foco em aprendizagem, não em retenção de Reel.
- **Escala, duração e frequência do punch-in:** não achei fonte primária, nem de plataforma, nem estudo, para escala (o 1,6 a 1,7x do estilo de referência fica bem acima do 1,15 a 1,3x das ferramentas), duração ou quantos punch-ins por vídeo. Instagram, YouTube e TikTok não falam de zoom nas orientações que encontrei. A fonte com dado mais próxima é MSV: num modelo da "sensation value" de 1.200 vídeos curtos, validado em 14.492 vídeos de TikTok, Reels e Shorts, o engajamento (curtidas, comentários e afins) segue um U invertido: estímulo moderado rende mais que pouco ou muito. No ponto ótimo, um vídeo de 60 s teria cerca de 12 tomadas, contra 24 nos vídeos de estímulo alto. Os próprios autores dizem que o resultado é correlacional e que só mediram movimento por troca de tomada, sem zoom nem efeitos sonoros. Um fornecedor (Vizard) recomenda punch-ins esparsos, só no início de frase, sem dado. **Status:** MSV confirmado (fonte primária, preprint sem revisão por pares); o resto Anedótico / não verificado.
- **Som junto do punch-in:** VDB achou que um bipe curto e sem informação espacial, sincronizado com a mudança de um objeto, faz esse objeto saltar aos olhos numa cena confusa e reduz muito o tempo de busca; o efeito não aparece com pista visual no lugar do som e persiste mesmo quando o bipe coincide na maioria das vezes com distratores, então é integração automática de som e imagem, e não alerta geral. É a base mais direta para o clique ou pop no punch-in: o som sincronizado reforça a mudança visual. TT-QT, orientação oficial do TikTok para anúncios, pede que efeitos visuais sejam sincronizados com o som, sem número. Que o som acompanhe o punch-in no estilo de referência é escolha de estilo; não achei quem meça clique contra whoosh contra nada. **Status:** VDB confirmado pelo resumo (laboratório, estímulos simples); TT-QT confirmado (fonte primária, sem dado); a escolha do tipo de som Anedótica / não verificada.
- **Efeitos sonoros:** PLB achou que o início de efeitos sonoros e de efeitos de produção provoca a resposta de orientação (desaceleração cardíaca típica de atenção automática) em ouvintes de rádio; não confirmei o efeito sobre memória. MM é a fonte primária sobre densidade: numa animação narrada de 180 s, sete sons ambientes, cada um tocado uma vez e casado com um evento da explicação (vento, cristais, trovão), não prejudicaram retenção nem transferência; já dois sons mecânicos de 9 s repetidos várias vezes ao longo da animação prejudicaram as duas, e música de fundo prejudicou nos dois experimentos. Os autores atribuem a diferença à coordenação: o som casado um a um com um evento ajuda, o som repetido e arbitrário atrapalha. A narração estava "claramente audível" e nenhum som a mascarava, mas o artigo não dá nível em dB. Isso sustenta o efeito sonoro raro e preso a um evento visual (como o punch-in) e contraria a camada contínua de SFX por cima da fala. Sobre o nível do SFX em relação à voz, não achei fonte primária: procurei na documentação de Instagram, YouTube e TikTok, em recomendações de difusão (EBU, BBC) e em pesquisa de inteligibilidade, que trata de música e fundo, não de efeito curto. As regras de SFX das ferramentas (12 a 20 dB abaixo da voz em YA; nas pausas e nunca por cima de fala contínua em HY) são relato de ajuste. **Status:** MM confirmado (fonte primária; animação educacional, não Reel); PLB por fonte secundária; níveis em dB Anedóticos / não verificados.
- **"Algo muda a cada 3 a 5 s":** aparece em YA como regra e no folclore de edição de vídeo curto; não achei fonte primária. TLB mostra o lado oposto do risco: agentes cortam mais devagar que o editor humano. **Status:** Anedótico / não verificado.
- **Transição entre takes:** BLA é a fonte primária mais próxima: o jump cut é a transição visível mais simples, e a escondida só funciona quando os quadros dos dois lados são parecidos. Para quando cortar e quando transformar, ver [analogia-e-animacao-sincronizada.md](analogia-e-animacao-sincronizada.md), seção 4.2. **Status:** Confirmado (fonte primária).

### 3.7 Loudness para Instagram e YouTube

- **YouTube:** a documentação oficial (YT-VOL) diz que o "stable volume" vem ligado por padrão e equilibra trechos baixos e altos, ajustando o volume continuamente; não dá número em LUFS e não usa o termo normalização. O -14 LUFS que circula vem de terceiros (o guia do Frame.io diz que o YouTube não publica o valor e "tende a" -12 a -14 LUFS). **Status:** Confirmado (fonte primária) que não há número oficial; o -14 é Anedótico / não verificado.
- **Instagram:** não achei número oficial no Help Center nem nos recursos para criadores da Meta. Os guias de terceiros divergem (de -10 a -14 LUFS). **Status:** Confirmado que não encontrei número oficial; os valores são Anedóticos.
- **Recomendação técnica independente:** a AES TD1008 (2021) recomenda, segundo fontes secundárias (Telos Alliance, Radio World), -18 LUFS para fala e -16 para música em streaming e sob demanda, com -17 como meio-termo para conteúdo misto. Não li o documento da AES. **Status:** Anedótico / não verificado (secundária).
- **Na prática:** KF, YA e GW usam -14 LUFS integrado e -1 dBTP para vídeo curto. É um padrão razoável e de baixo risco, porque plataformas tendem a baixar o que está alto demais, mas não é especificação de nenhuma plataforma.

## 4. Formato do projeto CapCut

### 4.1 O que cada biblioteca escreve

| Recurso | PCC | PJY | CLI | VCA | MCP |
| - | - | - | - | - | - |
| Trilhas e segmentos de vídeo e áudio | sim | sim | sim | sim | sim |
| Importar SRT com estilo | sim (`import_srt`, estilo de um texto de referência) | sim | sim (`import-srt`, `caption`, `caption --words`) | sim | não |
| Estilo de texto (fonte, contorno, fundo, sombra) | sim | sim | sim (`add-text`, presets) | sim | básico, clonado de um draft |
| Keyframe de posição e escala (zoom, mover quadro de tela dividida) | sim (position, scale, rotation, alpha, volume e cor) | sim | sim (position, scale, rotation, alpha, volume) | sim | `set_props` estático |
| Keyframe de máscara | não | não | não, de propósito | não verificado | não |
| Transição | sim, com duração | sim | sim | sim | "best-effort" |
| Animação de entrada e saída, efeito, filtro | sim | sim | sim | sim | "best-effort" |
| Efeito sonoro | áudio local; efeito de cena de áudio | igual | áudio local; `add-sfx` com efeitos da biblioteca do CapCut | sim | áudio local |
| Volume e fade de áudio | sim, com keyframe | sim | sim (`volume`, `audio-fade`) | sim | volume |
| Exportar o vídeo pelo CapCut | só a versão chinesa, até a 6 | só JianYing até 6.x | não (`render` é proxy em ffmpeg) | na nuvem (serviço pago) | não |

- **Fonte:** README e código de cada repositório. O CLI declina keyframe de máscara porque nenhum draft criado pelo app com essa codificação foi capturado, e uma codificação inventada salvaria sem erro e não faria nada no app (CHANGELOG do CLI, issue 44). A exportação automática do PCC procura a janela pelo nome chinês do produto e falha no CapCut internacional (PCC issue 17, testado em 9.4); o mantenedor relata que no 9.5 a caixa de exportação não expõe nenhum controle à automação de interface.
- **Consequência para o caso:** o zoom de abertura (scale com keyframe na entrada), o quadro que se move na tela dividida (posição e escala do segmento com keyframe), transições, fades e uma trilha de SFX com arquivos locais são escrevíveis. A borda animada por máscara não é. A exportação final continua manual no CapCut internacional.
- **Status:** Confirmado (fonte primária) para o que as bibliotecas declaram; o funcionamento no CapCut 9.6 não está testado por nenhuma delas.

### 4.2 Versões, criptografia e o CapCut 9.6

- **Criptografia:** o CLI documenta que o JianYing (versão chinesa) passou a criptografar `draft_content.json` a partir da 6.0, e que o CapCut internacional não é criptografado. PJY diz o mesmo para o JianYing novo: o `draft_content.json` "frequentemente não é JSON em texto"; ler um modelo exige um leitor extra, mas gerar draft novo funciona até a 10.8 do JianYing. O CLI acrescenta que, no JianYing 11.4 para macOS, um draft em texto escrito por ferramenta é aberto e convertido para o formato criptografado pelo próprio app. Isso bate com o que se vê na máquina do autor: no CapCut 9.6 para Windows, `draft_content.json` é JSON legível. **Status:** Confirmado (fonte primária) para o que as bibliotecas dizem.
- **crypto_key_store.dat:** nenhuma das bibliotecas, nenhuma issue do PCC e nenhum resultado de busca no código do GitHub menciona esse arquivo. Não consegui verificar o que ele guarda nem se o CapCut 9.6 passa a criptografar algo a partir dele. **Status:** não verificado.
- **Versões testadas:** a matriz do CLI separa evidência de expectativa. Só o CapCut 6.2.8 tem fixture completo testado. O 8.7.0 para Windows tem um fixture criado pelo app (`version` 360000, `new_version` "171.0.0"). Para 9.x há relatos: no 9.2.8 beta para macOS, o app lê `Timelines/<id>/draft_info.json` e trata `draft_content.json` da raiz como espelho legado, então escrever só na raiz não tem efeito; no 9.3.0 para macOS, um draft criado a partir de um modelo capturado do app abriu, foi editado, salvo, fechado e reaberto com a edição mantida. Outras versões 9.x estão como "expected-compatible, unverified". Para o 10.x, há relatos de drafts escritos por ferramenta recusados como corrompidos, e o CLI recusa escrever sem `--force-write`. O guarda de escrita do CLI recusa CapCut acima de 9.x e `version` acima de 360000. **Status:** Confirmado (fonte primária) para a matriz; cada linha 9.x é relato.
- **O caso 9.6 ("version": 360000, "new_version" de "187.0.0" a "189.0.0"):** nenhuma biblioteca tem fixture nem relato com esses valores; o mais alto com fixture é 171.0.0 (8.7.0). O guarda do CLI deixaria escrever (9.x e 360000 estão dentro do limite), mas isso só quer dizer que ninguém viu quebrar. Os modelos que PCC (CapCut 6.7.0, `new_version` 140.0.0) e VCA (CapCut 6.5.0, 138.0.0) embutem são antigos; o CLI relata que todo draft feito a partir do seu modelo 6.5.0 embutido foi recusado pelo CapCut 8.7.0 para Windows como vindo "de um caminho incomum", e que a causa eram os marcadores de versão desatualizados do modelo. **Status:** não verificado para o 9.6; o risco de recusa com modelo antigo é inferência a partir de um relato no 8.7.
- **Pasta `Timelines/`:** a partir do 8.7, o CapCut pode guardar a linha do tempo ativa num documento dentro de `Timelines/` e manter `draft_content.json`, `template-2.tmp` e `draft_meta_info.json` como espelhos. O CLI tem `diagnose` para ver qual é o documento ativo e `sync-timelines` para reconciliar os espelhos. Antes de escrever num projeto do 9.6, é preciso saber se ele tem `Timelines/` e qual arquivo o app lê. **Status:** Confirmado (fonte primária) para o comportamento relatado no 8.7 e 9.2.8.

### 4.3 CapCut fechado e registro do draft

- **Fechar o app:** MCP recusa salvar com o CapCut aberto ou com o arquivo `.locked` presente, porque o autosave do CapCut sobrescreve o que foi escrito por fora. SHI e SM dão a mesma instrução. O CLI recusa escrever num draft da pasta gerenciada enquanto detecta o processo do editor (`refused [editor-open]`), e escreve de forma atômica, com `.bak`, recusando se o arquivo mudou desde a leitura. PCC não fala em fechar o app; só diz que pode ser preciso entrar e sair de um draft ou reiniciar o CapCut para o novo aparecer na lista. **Status:** Confirmado (fonte primária).
- **Registro:** o CLI afirma que a interface do CapCut não varre a pasta de projetos e lista os drafts a partir de um índice, `root_meta_info.json`, na raiz de `com.lveditor.draft`; por isso `init` e `quickstart` registram o draft nesse índice e escrevem o `draft_meta_info.json` da pasta, e `register --apply` repara um draft que não aparece. PCC só copia um `draft_meta_info.json` estático e não toca no índice. A issue 13 do PCC relata que, no CapCut 9.1.0 para macOS, deixar vazio o `draft_materials` do `draft_meta_info.json` faz o app pedir para religar a mídia, mesmo com os caminhos certos no `draft_content.json`; preencher com a mídia da linha do tempo resolve (`register --materials` no CLI). **Status:** Confirmado (fonte primária) para o que cada um faz; a necessidade do índice é afirmação do CLI que não testei, e PCC e CLI divergem sobre ela.
- **O caminho que funcionou no 9.x:** criar um projeto vazio dentro do CapCut, fechar o app, escrever nesse projeto (vídeo, SRT, áudio), sincronizar os espelhos e registrar a mídia, reabrir (SHI, verificado pelo autor no 9.3.0 para macOS). O CLI incorporou isso: desde a 0.23, `init`, `quickstart` e `compile` copiam os marcadores de versão do projeto mais novo criado pelo app, e `compile --into` preenche um projeto vazio criado pelo app mantendo nome e registro; a aceitação no desktop continua pendente segundo o próprio README. **Status:** Confirmado (fonte primária) para a documentação; nenhum relato no Windows 9.x.
- **Teste próprio no CapCut 9.6 para Windows (2026-10-15):** projeto vazio criado no app (`new_version` "189.0.0", com `Timelines/<id>/`), app fechado, o mesmo `draft_content.json` escrito na raiz e em `Timelines/<id>/` por um script próprio, sem biblioteca. O conteúdo foram 22 trechos da faixa principal de outro projeto (materiais e referências copiados, placeholder trocado por caminho absoluto) e keyframes de escala de 1,5 para 1,0 no primeiro trecho, com `time_offset` no tempo do material de origem. Sem tocar em `root_meta_info.json` nem em `draft_materials`. O app abriu o projeto com os 22 trechos e o zoom. **Status:** Confirmado (teste próprio, um caso); falta testar texto, áudio e mídia que não esteja em outro projeto do CapCut.

## 5. Implicações para o desenho

O que segue é proposta para o autor decidir, apoiada nos achados acima.

### 5.1 Quantas skills e como dividir

1. **Corte bruto, uma skill nova.** Junta os brutos, transcreve com timestamps de palavra, monta a tabela de takes, corta silêncios e entrega o vídeo cortado, o SRT da fala mantida e a tabela de takes. É a etapa com mais base (seções 3.1, 3.3) e a que os agentes já fazem bem (3.2). Deve trazer o que falta em todas as ferramentas da comunidade: hesitações e palavras de entrada em pt-BR, limiar de silêncio calibrado no ruído da gravação (LC) e retake por reformulação lido pelo agente, não só por similaridade (VV). Nome no padrão do repositório, por exemplo `cutting-reel-takes`.
2. **Legenda: não precisa de skill própria agora.** O SRT sai do corte bruto, o autor já corrige a legenda e a `reel-motion` já usa o SRT corrigido mais os tempos do Whisper. O estilo da legenda vive melhor num draft-modelo do CapCut (PCC e CLI importam SRT com o estilo de um texto de referência) do que em regras escritas.
3. **Cenas: a skill existente.** `reel-motion` continua igual; ela já entrega arquivos numerados para trilhas próprias do CapCut, e o `timeline.md` dela é a entrada natural da montagem.
4. **Montagem e acabamento, uma skill nova.** Monta o draft do CapCut: segmentos do corte, trilhas das cenas e overlays nos timecodes do `timeline.md`, legenda do SRT com o estilo do modelo, zoom de abertura com keyframe de escala e o whoosh ou impacto sincronizado, trilha de SFX com arquivos locais, volume e fades. Nome como `assembling-capcut-drafts`. As regras de gosto (quantos zooms, quais SFX, qual transição) entram aqui como sugestões que o autor aprova, não como regras fixas, porque nenhuma delas tem fonte primária (3.6).
5. **Orquestrador: depois.** Pelas regras do repositório, uma skill nasce depois de fazer o trabalho à mão algumas vezes. Um orquestrador só faz sentido quando corte e montagem tiverem sido usados em vídeos reais; até lá, cada skill chama a seguinte pelo nome, sem apontar para arquivos da outra (ADR 0002).

### 5.2 Saída: draft do CapCut, mp4 do ffmpeg ou os dois

- **Corte bruto em mp4 primeiro.** É o que LC, VV e KF fazem, não depende do formato do CapCut e já entra no fluxo atual (importar um arquivo só). O custo: o corte vira definitivo, sem folga para estender um corte no CapCut.
- **Draft do CapCut como destino da montagem.** O autor refina e exporta no CapCut; exportar automaticamente não funciona no CapCut internacional (4.1). Um draft com segmentos guarda a folga de cada corte e deixa o autor desfazer um corte no app. O risco é o formato (4.2): cada atualização do CapCut pode quebrar a escrita, e o CLI recomenda guardar o instalador da versão validada e fazer backup da pasta de drafts antes de abrir o app depois de uma atualização.
- **Proxy em mp4 para revisão.** Um render rápido em ffmpeg (o `render` do CLI faz isso) deixa o autor ver o corte no celular antes de abrir o CapCut.
- **Os dois, em fases:** mp4 do corte bruto agora; draft do CapCut quando o teste da seção 5.4 passar no 9.6 para Windows.

### 5.3 Pontos de aprovação

1. **Tabela de takes, antes de renderizar.** Cada grupo de retake com os takes, o escolhido e o motivo, mais os trechos duvidosos. Está em RUB, LC, YA e VV. Na dúvida, mantém (VV).
2. **SRT corrigido pelo autor.** Já é prática; o SRT é a fonte do texto da legenda e das cenas.
3. **Plano de cenas e stills.** Já existe na `reel-motion`.
4. **Plano de acabamento e SFX, antes de mixar.** Lista com tempo, efeito e motivo, como a auditoria obrigatória de HY.
5. **Veredito de ritmo no CapCut.** TLB mostra que o agente não julga o próprio ritmo e quase sempre diz que acertou; esse veredito fica com o autor, assistindo.

### 5.4 O que testar primeiro

1. **Linha de base do corte bruto.** Rodar VV (e o `detect-retakes` do CLI no SRT) em dois ou três brutos reais em pt-BR e comparar com o corte que o autor fez à mão no CapCut. Anotar: retake que passou, frase boa cortada, fim de palavra comido, tamanho das pausas que sobraram. É o caminho que o repositório pede para uma skill sem caso próprio (rodar a ferramenta existente em entrada realista e registrar onde falha).
2. **Pausa de referência.** Medir as pausas entre frases nos Reels já publicados do autor, cortados à mão. Isso dá o alvo para a pausa que sobra, no lugar de escolher entre 0,09 e 0,5 s sem base (3.4).
3. **Escrita no CapCut 9.6 para Windows, com risco mínimo.** Num projeto vazio criado no app e com o CapCut fechado: ver se há `Timelines/`, rodar `capcut diagnose` e `capcut version`, escrever um segmento de vídeo e um SRT com `compile --into`, reabrir, salvar, fechar e reabrir para ver se a edição ficou. Depois, um keyframe de escala e um áudio local. Só então montar um vídeo inteiro. Se o CLI recusar ou o app ignorar, a montagem fica em mp4 e o draft espera.
4. **crypto_key_store.dat.** Ver em quais projetos ele aparece, se surge depois de alguma ação no app (login, recurso pago, nuvem) e se esses projetos continuam com `draft_content.json` legível.

### 5.5 Riscos

- **Formato do CapCut:** não documentado, muda a cada versão, sem teste no 9.6; atualização automática do app pode migrar drafts (4.2). Mitigação: backup da pasta de drafts, versão anotada a cada uso, escrita só com o app fechado.
- **Whisper e retakes:** o Whisper pode juntar retakes e deslocar os tempos (LC). Mitigação: conferir as fronteiras retranscrevendo a janela, e a tabela de takes aprovada pelo autor.
- **pt-BR:** nenhuma ferramenta cobre hesitações em português; duas fixam inglês no código.
- **Licenças:** PCC não tem licença (por padrão, todos os direitos reservados), SC e o motor de draft do JianYing que ele usa são não comerciais. Usar como referência de formato, não copiar código para este repositório público.
- **Gosto em regra fixa:** as regras de ritmo, zoom e SFX da comunidade não têm fonte primária (3.6). Escrevê-las como lei na skill repetiria o erro; o desenho mais seguro é sugerir e o autor aprovar.
- **Agente que se dá por satisfeito:** TLB, 93% de autoavaliação positiva. O veredito final não pode ser do agente.
