# Visão geral do projeto

Documento com os **pontos principais** do *Public Data Monitor* no código e na arquitetura. Para rodar e prints, use o [README](../README.md).

## O que é

API em **FastAPI** que **coleta** notícias públicas de uma fonte configurada (hoje: **G1 Tecnologia**), **persiste** em **PostgreSQL** com deduplicação por URL e **expõe** consulta paginada, **detalhe por id** e **exclusão administrativa opcional**, com documentação OpenAPI em `/docs`. Há **[demo no Render](https://public-data-monitor.onrender.com/docs)** para experimentar sem subir o repositório localmente.

## Objetivo técnico

Demonstrar um MVP de backend com **I/O assíncrono** (HTTP + banco), **SQLAlchemy async**, **camadas separadas** (rotas → serviços → scraper/modelo) e **deploy local** via Docker Compose.

## Stack

| Camada | Tecnologia |
|--------|------------|
| API | FastAPI, Pydantic (schemas de resposta) |
| Banco | PostgreSQL 16, SQLAlchemy 2 async, asyncpg |
| Coleta | httpx, BeautifulSoup4 |
| Runtime | Python 3.11+, Uvicorn (via Docker) |
| Infra | Docker Compose (API + Postgres) |

## Estrutura de pastas (resumo)

```text
app/
  main.py          # FastAPI, lifespan: cria tabelas ao subir
  api/routes.py    # Endpoints HTTP
  api/deps.py      # Dependências (ex.: API key para DELETE)
  services.py      # Coleta, consulta por id, exclusão, contagem e listagem
  scrapers/g1.py   # Extração HTML da fonte G1
  models/news.py   # Entidade SQLAlchemy `News`
  schemas/news.py  # Contratos de resposta (Swagger)
  db/              # Engine, sessão async, Base
  core/config.py   # Configuração (DATABASE_URL, NEWS_DELETE_API_KEY opcional)
```

## Fluxo principal

1. **Subida da API** (`lifespan` em `main.py`): garante que as tabelas existam (`create_all` no metadata do SQLAlchemy).
2. **Coleta** (`POST /news`): chama `collect_news` → scraper `scrape_g1_tech` → `INSERT` com `ON CONFLICT DO NOTHING` na coluna **URL** → retorna quantos registros **novos** foram inseridos.
3. **Listagem** (`GET /news`): `list_news` ordena por `created_at` decrescente, aplica `limit`/`offset`; `count_news` alimenta `total` e `has_next` na resposta paginada.
4. **Detalhe** (`GET /news/{id}`): `get_news_by_id` retorna um registro ou 404.
5. **Exclusão** (`DELETE /news/{id}`): só ativa se `NEWS_DELETE_API_KEY` estiver definida; exige header `X-API-Key` idêntico; responde 204 ou 404.

## API (contrato resumido)

| Método | Caminho | Função |
|--------|---------|--------|
| `GET` | `/health` | Health check (`status: ok`) |
| `POST` | `/news` | Dispara coleta e persistência |
| `GET` | `/news` | Lista notícias (query: `limit`, `offset`) |
| `GET` | `/news/{id}` | Detalhe de uma notícia |
| `DELETE` | `/news/{id}` | Remove notícia (opcional; ver `NEWS_DELETE_API_KEY` + `X-API-Key`) |
| — | `/docs` | Swagger UI (gerado pelo FastAPI) |

Convenção adotada: recurso em plural **`/news`**; ações via **método HTTP** (`POST` coleta, `GET` lista/detalha, `DELETE` remove quando habilitado).

## Modelo de dados (`News`)

Campos relevantes: `title`, `summary`, `url` (**único**, base da deduplicação), `source`, `published_at`, `created_at`.

## Decisões de implementação (rápido)

- **Async end-to-end** na coleta HTTP e no acesso ao banco.
- **Deduplicação** alinhada ao índice único em `url` + `on_conflict_do_nothing` no insert em lote.
- **Scraper isolado** (`scrapers/g1.py`) para trocar ou acrescentar fontes sem misturar com rotas.
- **Retry** no client HTTP do G1 (resiliência a falhas transitórias).
- **Schemas Pydantic** com descrições para documentação clara no Swagger.

## Infraestrutura

- `docker-compose.yml`: serviços `db` (Postgres) e `api` (build do `Dockerfile`), porta da API mapeada para **8001** no host.
- Variável `DATABASE_URL` pode vir de `.env` (Compose lê `.env` por padrão) ou de valores definidos no compose; detalhes no README.

## Testes

Pasta `tests/`: testes de rota (com mocks) e utilitários do scraper, conforme arquivos presentes no repositório.

---

Este arquivo é **só visão de projeto**; instruções de uso, licença e demonstração visual continuam no [README](../README.md).
