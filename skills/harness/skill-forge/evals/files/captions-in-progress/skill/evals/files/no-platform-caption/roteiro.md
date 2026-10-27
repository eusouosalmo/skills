cuuida, modo em loop funciona bem em desenvolvimento com specs SDD?

Macho, funciona bem... mas não é o loop em si que resolve o problema. É o que vem antes dele e o que vem depois.

Pra contextualizar... de domingo pra segunda, eu tava cansado mas queria fechar um escopo que eu tava codando. Já tinha usado a skill de grill nesse problema, que basicamente é pedir para a inteligência artificial me entrevistar com perguntas criadas a partir de vários ângulos do contexto do problema. Depois rodei as skills que transformam nosso contexto em especificações e então faltava só codar.

Aí pensei: e se o Claude codasse sozinho enquanto eu dormia? Foi aí que rodei um loop estilo Ralph, mas com duas travas. Primeiro: ele não podia commitar nada — bloqueei git de escrita, para que eu pudesse revisar de maneira mais fácil.

A segunda trava, cada etapa só virava concluída se passasse nos testes que eu mandei ele criar e o teste precisava falhar primeiro, antes do código existir — só depois ele codava até o teste passar. E o porquê disso é que se o teste já passa antes de tu escrever qualquer código, ele não presta pois não está testando nada — é um teste furado, que vai passar sempre, independente do que tu escreva. Isso daí é o TDD clássico. E ainda tem um segundo Claude, com o contexto limpo, revisando o diff atrás dele antes do próximo ciclo pegar a próxima etapa.

Na prática, o checklist morava na própria etapa — já vinha com os critérios escritos, e só virava concluída quando os testes batiam com eles.

Foi assim que funcionou aqui. Se tu já tá testando algo parecido, me manda como ficou o teu.
