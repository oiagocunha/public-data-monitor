# Public Data Monitor

Backend para coleta e consulta de notícias públicas com FastAPI, PostgreSQL e processamento assíncrono.

## Objetivo

Construir um MVP de coleta e consulta de notícias para demonstrar competências de backend.

## Tecnologias utilizadas

- Python
- asyncio
- FastAPI
- SQL assíncrono
- Docker
- Organização em camadas

## Requisitos

Antes de rodar o projeto, você precisa de:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Configuração

1. Clone o repositório:

```bash
git clone <url-do-seu-repositorio>
cd public-data-monitor
```

2. (Opcional) copie o arquivo de ambiente de exemplo:

```bash
cp .env.example .env
# No Windows (PowerShell): Copy-Item .env.example .env
```

> O projeto funciona sem arquivo `.env` ao subir via Docker Compose, pois as variáveis
> necessárias já estão definidas no `docker-compose.yml` (incluindo a conexão com o banco).

## Uso

1. Suba os containers sem travar o terminal:

```bash
docker compose up -d --build
```

2. Acesse:

- API: `http://localhost:8001`
- Swagger (OpenAPI): `http://localhost:8001/docs`

3. Dispare a coleta inicial de notícias:

```bash
curl -X POST http://localhost:8001/news
```

4. Consulte as notícias coletadas:

```bash
curl "http://localhost:8001/news?limit=20&offset=0"
```

## Demonstração (Documentação)

### 1) Tela inicial da documentação

Visão geral dos endpoints disponíveis e organização da API.

![Tela inicial do Swagger](./docs/images/swagger-home.png)

### 2) Coleta de notícias (`POST /news`)

Execução da coleta com retorno da quantidade de itens inseridos.

![Endpoint POST /news](./docs/images/swagger-post-news.png)

### 3) Listagem de notícias (`GET /news`)

Consulta paginada com `limit` e `offset`, retornando `items`, `total` e `has_next`.

Parameters:  
![Endpoint GET /news](./docs/images/swagger-get-news_parameters.png)

Responses:  
![Endpoint GET /news](./docs/images/swagger-get-news_responses.png)

### 4) Schemas da API

Visualização dos contratos de resposta da aplicação (`HealthResponse`, `CollectNewsResponse`, `NewsRead` e `NewsPage`).

![Schemas da API](./docs/images/swagger-schemas.png)

## Endpoints

- `GET /health` - health check da aplicação
- `POST /news` - executa a coleta e persiste notícias novas
- `GET /news?limit=20&offset=0` - lista notícias com paginação
- `GET /docs` - documentação interativa da API

Exemplo de resposta paginada:

```json
{
  "items": [],
  "limit": 20,
  "offset": 0,
  "total": 120,
  "has_next": true
}
```

## Convenção RESTful adotada

Para manter consistência com RESTful naming convention:

- usar substantivos no plural para recursos (`/news`);
- usar o método HTTP para representar a ação (`POST /news` cria/coleta, `GET /news` consulta);
- evitar verbos na URL (por isso `POST /collect` foi substituído por `POST /news`).

## Estrutura

```text
app/
  api/        # rotas FastAPI
  core/       # configurações
  db/         # engine e sessão
  models/     # modelos SQLAlchemy
  schemas/    # schemas de resposta
  scrapers/   # scrapers por fonte
  services.py # regras de coleta e consulta
```

## Decisões técnicas

- **asyncio + httpx**: scraping é I/O bound, então concorrência async melhora throughput.
- **FastAPI**: integração natural com ecossistema async e tipagem clara.
- **Deduplicação por URL**: evita reprocessamento e registros repetidos no banco.
- **Scraper isolado por fonte**: facilita manutenção quando o HTML de uma fonte muda.
- **Retry e logging básicos**: melhora resiliência e debugging sem aumentar complexidade.

## Licença

Este projeto está licenciado sob a [MIT License](./LICENSE).
