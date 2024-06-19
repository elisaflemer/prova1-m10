# prova1-m10

Esta atividade se refere à prova substitutiva do módulo 10 de Engenharia da Computação. Ela é composta por um sistema em Docker Compose contendo um backend em FastAPI, com uma API de reviews de filmes armazenada em SQLite, e um gateway em nginx para redirecionamento através do localhost na porta 80, quando a rota inicia com o prefixo "/reviews".

A API em si tem maturidade de Richardson de nível 2. Ela inclui rotas para ver todos as resenhas, ver uma resenha por ID, adicionar uma resenha, deletar uma resenha e atualizar uma resena. Além disso, ela loga os eventos do sistema a partir do nível INFO, em arquivos na pasta logs, na raiz do projeto, gerando um novo arquivo com timestamp diariamente à meia-noite. Essa pasta é mapeada como volume no Docker Compose.

Também foi implementado um cache para as rotas de cache utilizando o Redis.

## Rotas

- /reviews: retorna todas as resenha (GET com cache -- chave 'reviews')
- /reviews/{id}: retorna uma resenha através de seu ID (GET com cache -- chave 'review-{id}')
- /reviews: adiciona uma resenha via JSON (POST)
- /reviews/{id}: atualiza uma resenha via JSON (PUT)
- /reviews/{id}: deleta uma resenha (DELETE)

## Como executar

Todo o desenvolvimento foi feito em Docker Compose. Logo, não é necessário iniciar ambientes virtuais. Em vez disso, certifique-se, primeiro, de ter o Docker baixado em seu sistema e de estar com o daemon ativado. Então, execute, na pasta raiz do projeto:

```bash
docker compose up
```

A partir daí, as rotas estarão acessíveis a partir da URL `http://localhost/reviews`.

Para acessar os logs, confira a pasta `logs`. Os arquivos estarão separados por timestamp de 1 em um 1 minuto. Para alterar o nível das mensagens do log, baste modificar o argumento na linha 18 do arquivo `app/logging_config.py`.

```python
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
```

## Vídeo

