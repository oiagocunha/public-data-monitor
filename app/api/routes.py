from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal
from app.schemas.news import CollectNewsResponse, HealthResponse, NewsPage, NewsRead
from app.services import collect_news, count_news, list_news

router = APIRouter(tags=["News"])


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get(
    "/health",
    summary="Verificar saude da API",
    description="Endpoint simples para monitoramento e readiness check da aplicacao.",
    response_model=HealthResponse,
    response_description="Status atual da API.",
)
async def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/news",
    summary="Executar coleta de noticias",
    description=(
        "Inicia a coleta na fonte configurada (G1 Tecnologia), "
        "deduplica por URL e persiste apenas noticias novas."
    ),
    response_model=CollectNewsResponse,
    response_description="Resultado da coleta com quantidade de itens inseridos.",
)
async def collect_news_route(session: AsyncSession = Depends(get_session)) -> CollectNewsResponse:
    inserted = await collect_news(session)
    return CollectNewsResponse(inserted=inserted)


@router.get(
    "/news",
    response_model=NewsPage,
    summary="Listar noticias coletadas",
    description=(
        "Retorna noticias paginadas ordenadas da mais recente para a mais antiga, "
        "com metadados de navegacao."
    ),
    response_description="Pagina de noticias com itens e metadados de paginacao.",
)
async def get_news(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Numero maximo de noticias por pagina (entre 1 e 200).",
        examples=[20],
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Quantidade de registros ignorados antes de retornar a pagina atual.",
        examples=[0, 20, 40],
    ),
    session: AsyncSession = Depends(get_session),
) -> NewsPage:
    news = await list_news(session=session, limit=limit, offset=offset)
    total = await count_news(session=session)
    return NewsPage(
        items=[NewsRead.model_validate(item) for item in news],
        limit=limit,
        offset=offset,
        total=total,
        has_next=(offset + limit) < total,
    )
