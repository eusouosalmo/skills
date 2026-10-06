## Tool calls
- Skill: {"skill": "writing-as-eusouosalmo", "args": "legenda de Instagram para o vídeo cujo roteiro está em roteiro.md"}
- Bash: {"command": "ls -la /tmp/claude-1000/caption-run.VT5x; cat /tmp/claude-1000/caption-run.VT5x/roteiro.md", "description": "Lista a pasta e mostra o rot
- Read: {"file_path": "/home/salmo/.claude/skills/writing-as-eusouosalmo/examples.md"}
- Read: {"file_path": "/home/salmo/.claude/skills/writing-as-eusouosalmo/checklist.md"}
- Write: {"file_path": "/tmp/claude-1000/caption-run.VT5x/legenda.md", "content": "Modo em loop funciona bem em desenvolvimento com specs SDD? Funciona, mas nã
- Write: {"file_path": "/tmp/claude-1000/-tmp-claude-1000-caption-run-VT5x/15945fcc-059f-4814-a6d8-6fba15a39b05/scratchpad/legenda.md", "content": "Modo em loo
- Bash: {"command": "python3 /home/salmo/.claude/skills/writing-as-eusouosalmo/scripts/check-voice.py /tmp/claude-1000/-tmp-claude-1000-caption-run-VT5x/15945

## Final answer

Escrevi a legenda no registro falado (com "tu"), usando só o que está no roteiro. O verificador de voz não encontrou nenhum problema e o texto passou pelo checklist.

---

Modo em loop funciona bem em desenvolvimento com specs SDD? Funciona, mas não é o loop em si que resolve o problema. É o que vem antes dele e o que vem depois.

Antes, usei a skill de grill, que é pedir para a inteligência artificial me entrevistar com perguntas criadas a partir de vários ângulos do problema. Depois rodei as skills que transformam esse contexto em especificações.

Aí deixei o Claude codando sozinho enquanto eu dormia, num loop estilo Ralph com duas travas:
- sem commit: bloqueei git de escrita, para revisar de maneira mais fácil
- teste primeiro: cada etapa só virava concluída se passasse nos testes que eu mandei ele criar, e cada um precisava falhar antes do código existir. Se já passa sem código nenhum, é um teste furado, porque não verifica nada. Esse é o TDD clássico.

E entre um ciclo e outro, um segundo Claude, com o contexto limpo, revisava o diff antes da próxima etapa começar.

Se tu já tá testando algo parecido, me manda como ficou o teu.

---

O que mudei em relação ao roteiro:
- **"De domingo pra segunda" saiu.** Assim a legenda não fica presa a uma data.
- **Encurtei a explicação do teste furado.** No roteiro ela é mais longa.
- **Sem hashtags.** O roteiro não tinha nenhuma, então não inventei. Se você usa um conjunto fixo, é só colar no fim.

A pasta do projeto não tinha permissão de escrita, então o arquivo ficou só na área temporária: `/tmp/claude-1000/-tmp-claude-1000-caption-run-VT5x/15945fcc-059f-4814-a6d8-6fba15a39b05/scratchpad/legenda.md`. Se quiser, copio para a pasta do projeto.
