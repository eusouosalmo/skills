# Roteiro: o índice GIN serve o operador, não a coluna JSONB

Plataforma: Instagram Reels | Duração alvo: 60 a 90 s | Objetivo: informar

## Script

| Bloco | Fala | Visual |
|---|---|---|
| Gancho (sintoma) | Tu criou um índice GIN na coluna JSONB do Postgres, e a consulta continua varrendo a tabela inteira. | Forma: imagem que se monta na palavra (o sintoma digitado). Desde o primeiro frame, código na tela: `CREATE INDEX ON pagamentos USING gin (metadados);` e embaixo `WHERE metadados->>'status' = 'recusado'`, com o `EXPLAIN` mostrando `Seq Scan on pagamentos` em destaque. |
| Contexto (nome do remédio) | O remédio tem nome: operador indexável. | Texto na tela: "operador indexável". |
| Entrega (caso do começo ao fim) | Numa tabela de pagamentos, cada gateway devolve a resposta num formato diferente, então JSONB faz sentido. Aí o suporte pede a lista dos recusados. Tu escreve metadados, setinha dupla, status, igual a recusado, e o EXPLAIN mostra Seq Scan. Isso porque a setinha só extrai um texto, e o GIN não sabe comparar texto com igual. Ele guarda as chaves e valores de dentro do JSON e só responde a operadores como o contém. Troca o filtro pra metadados contém status recusado, e o índice entra. Ou cria um B-tree daquela expressão exata. | Dois JSONs de gateways diferentes lado a lado na mesma coluna `metadados`. Depois a consulta com `->>` e o `Seq Scan`. Lista do que o GIN (`jsonb_ops`) aceita: `@>`, `?`, `?\|`, `?&`, `@?`, `@@`. Troca para `WHERE metadados @> '{"status": "recusado"}'` e o `EXPLAIN` com `Bitmap Index Scan`. Alternativa: `CREATE INDEX ON pagamentos ((metadados->>'status'));` |
| Entrega (teste com caso novo) | Caso novo: pagamentos acima de cem reais. O GIN ajuda? Não, porque maior que não é operador do GIN. Aqui vai um B-tree no valor convertido pra número, escrito igualzinho no WHERE. | `WHERE (metadados->>'valor')::numeric > 100` com um "?" na tela, pausa curta. Depois `CREATE INDEX ON pagamentos (((metadados->>'valor')::numeric));` com a expressão destacada nas duas linhas, mostrando que é a mesma. |
| Conexão (princípio) | Então o índice não serve a coluna, ele serve o operador. | Texto na tela: "O índice serve o operador, não a coluna." Tabela curta: `@>`, `?` vão no GIN; `->>` com `=`, `>`, `<` vão no B-tree de expressão. |
| Conexão (quando não vale) | Só que, quando o campo aparece em quase toda consulta, ele vira coluna normal, porque o Postgres não guarda estatística dos campos de dentro do JSON. | `ALTER TABLE pagamentos ADD COLUMN status text;` Texto na tela: "campo em toda consulta = coluna". |
| CTA | Qual operador tu mais usa no teu JSONB? | Texto na tela: "`->>`, `@>` ou `?`?" |

Ganchos alternativos:
- Me disseram que a setinha do JSONB não usa o índice GIN, e eu aceitei sem saber por quê. (crença comum contrariada; vem das anotações; a tela mostra o `->>` e o `Seq Scan` no primeiro segundo)
- Se tu é desenvolvedor e guarda JSON numa coluna JSONB do Postgres, aquele índice GIN pode não estar fazendo nada nas tuas consultas. (chamando o público pelo papel, com condição)

A checar antes de gravar:
- O índice GIN com a classe padrão `jsonb_ops` atende `@>`, `?`, `?|`, `?&`, `@?` e `@@`; `jsonb_path_ops` só atende `@>`, `@?` e `@@` (não atende `?`). Conferir em https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING e https://www.postgresql.org/docs/current/gin-builtin-opclasses.html
- `->` e `->>` não são operadores de nenhuma classe GIN, então `metadados->>'status' = 'recusado'` não usa o índice GIN da coluna. Conferir nas mesmas páginas.
- Com a tabela pequena, o planner escolhe Seq Scan mesmo com o índice certo. Para a demonstração na tela, usar uma tabela com volume (ex.: `generate_series` com centenas de milhares de linhas) e conferir que o `EXPLAIN` mostra `Bitmap Index Scan` depois da troca para `@>`.
- O índice de expressão só é usado quando o WHERE repete a expressão do índice, inclusive o cast `::numeric`. Conferir em https://www.postgresql.org/docs/current/indexes-expressional.html
- O Postgres não coleta estatística por campo de dentro de um valor JSONB, e a seletividade de `@>` é estimada por um valor fixo. Conferir em https://www.postgresql.org/docs/current/planner-stats.html e no código de `contsel` / `matchingsel`; se a afirmação não se sustentar para a versão alvo, trocar o motivo da última fala por outro concreto (ex.: B-tree comum e constraint `NOT NULL` só funcionam em coluna).
- "Operador indexável" como nome: a documentação fala em operadores que a classe de operador do índice suporta (https://www.postgresql.org/docs/current/indexes-opclass.html). Conferir se o termo soa natural para o público.

Crédito para a legenda: documentação oficial do PostgreSQL, seção 8.14.4 (jsonb Indexing).

