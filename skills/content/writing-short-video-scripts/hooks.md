# Hooks

Seven patterns for the first 3 seconds of an educational technical video, each tied to the mechanism behind it. The examples all start from the same lukewarm claim, "testar o código é importante", and show form only; their facts are made up. Name a pattern by its pt-BR name in the script.

| Pattern | Why it holds | Example |
|---|---|---|
| The viewer's situation with an unexpected consequence (situação do espectador) | people attend to what is about them, and the situation itself filters who watches; a broken expectation pulls them to find out why | "Se tu só testa o código clicando na tela, tu testa o caminho que já sabe que funciona." |
| A bet (aposta) | asking for a guess raises curiosity about the answer | "Quantos bugs um teste de dez linhas pegou no meu último projeto? Eu chutei zero." |
| A common belief contradicted by a concrete detail (crença contrariada) | broken expectation plus something specific to picture | "O teste que mais me salvou não testava regra de negócio nenhuma. Ele só abria a tela de login." |
| The author's scene at the turning point, outcome open (cena do autor) | an unfinished sequence the viewer wants to see end | "Sexta, cinco da tarde, eu subi uma correção de uma linha. Às seis, ninguém conseguia pagar no site." |
| The unsaid question (pergunta não dita) | a scene or an absurd prediction makes the viewer form the question alone, and a question of their own pulls harder than one they are handed; no line asks it | "Se cada teste que eu escrevo pega um bug, meu projeto com dois mil testes não devia ter bug nenhum." |
| Exclusion (exclusão) | the proof comes before the question: the obvious causes are denied one by one, or the case where the thing does not happen is shown, so the viewer is left with no explanation | "Mesmo teste, mesmo código, mesma máquina. Eu rodei duas vezes e na segunda ele falhou." |
| Half-truth (meia-verdade) | the line is true in one metric only; the viewer accepts it, and the video proves it and then shows the metric where it is false, so the trap is the lesson | "O melhor teste que tu pode escrever é o que roda em um milissegundo." |

Calling the viewer by role ("Se tu é desenvolvedor...") is not a pattern: none of the strongest reference reels opens that way. The situation does the filtering.

## Terms in the hook

Every technical term in the hook comes full and with one meaning ("testes automatizados", not "testes"; "arquitetura de software", not "arquitetura"; "desenvolvedor", not "dev"), because in the first second there is no context to tell a short or ambiguous word apart. The niche stays implicit in the situation, never as a vocative. A role word enters only when it is part of the situation ("desenvolvedores experientes juraram que..."), never to call the viewer.

## The five questions

A hook passes when it answers all five:

1. **Who?** The viewer or the author is in the sentence, not only a process, an area or "eles".
2. **What concrete thing?** A number, a scene, a tool, a moment.
3. **What question stays open?** After the line, the viewer wants to know something. A line that already states the conclusion leaves nothing open.
4. **What does it contradict?** Something the viewer believed before.
5. **Is it true?** A contradiction keeps the qualifier that makes it true ("teste demais atrasa o projeto *quando testa a mesma camada duas vezes*"), and the video delivers what the hook promises. A half-truth passes only when the video shows the metric where it is false. A hook the video does not pay off is empty clickbait.

The lukewarm claim "testar o código é importante" fails the first four: no one is in it, nothing is concrete, it states its own conclusion, and every viewer already agrees.

## Which pattern

When the format asks for a hook pattern ([formats.md](formats.md)), the main hook uses it. Otherwise pick the strongest for these notes. Write two alternatives besides the main one, each from a pattern different from the main hook's and from each other's, and name each hook's pattern in parentheses.

## Visual hook

What the screen does in the first 3 seconds takes one of five forms. Pick the one the format points to; text that repeats the spoken hook is not a form, because the screen would close the question the voice leaves open, and most of the strongest reference reels have no big text in the hook.

| Form | What the screen does | Fits |
|---|---|---|
| Result shown first (resultado mostrado antes) | the finished thing (a diagram, a green pipeline, the trip in miniature) appears and then comes apart | process as a ladder |
| Image built on the word (imagem que se monta na palavra) | what is heard appears at that instant, drawn or typed: the symptom typed as code or `EXPLAIN` output, the scene drawn as it is said | paradox in layers, symptom, cure and dose, common doubt (the typed question) |
| Still comparison (comparação parada) | one ready image with a difference for the eye to find; nothing moves | experiment that reproduces everyday life, absurd comparison |
| Source or subject over the face (fonte ou assunto sobre o rosto) | the source's cover or an image of the subject over the recording | study with fine print, tool swap |
| Face and setting only (só rosto e cenário) | the setting says who the video is for (a kitchen, a call, a notebook) | routine that becomes a list, analogy formats that open on a scene the author plays |

## After the hook

Two moves for the sentence right after the hook, each only when its trigger holds; without the trigger they become a tic.

- **Anticipated objection.** When the hook sounds exaggerated (an absurd claim, a half-truth, a consequence that intimidates), the next sentence says the viewer's doubt, denies it and promises the proof: "Parece exagero, mas eu vou te mostrar a conta." The viewer who was about to dismiss the hook stays to see the proof.
- **Antagonist with a price.** Who charges for what the video gives away, with the price, makes the delivery worth more: "Tem curso cobrando quinhentos reais pra ensinar isso." Only when the antagonist and the price exist and were checked in a primary source; otherwise leave it out.
