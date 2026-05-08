# Public Data Monitor

Projeto backend focado em coleta assíncrona de dados públicos com persistência em PostgreSQL e API em FastAPI.

## Objetivo

Construir um MVP de coleta e recuperação de notícias públicas para demonstrar competências de backend:
Python, asyncio, FastAPI, SQL async, Docker e organização de código.

## Stack

- Python 3.11
- FastAPI
- SQLAlchemy Async + asyncpg
- PostgreSQL
- httpx + BeautifulSoup4
- Docker Compose

## Como rodar

```bash
docker compose up --build
```

API disponível em `http://localhost:8001`.

## Endpoints

- `GET /health`
- `POST /collect` (dispara coleta da fonte G1 Tecnologia)
- `GET /news?limit=20&offset=0`

Exemplo de resposta de paginação:

```json
{
  "items": [],
  "limit": 20,
  "offset": 0,
  "total": 120,
  "has_next": true
}
```

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
