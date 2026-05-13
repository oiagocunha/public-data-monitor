from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_delete_news_api_key
from app.db.session import SessionLocal
from app.schemas.news import CollectNewsResponse, HealthResponse, NewsPage, NewsRead
from app.services import (
    collect_news,
    count_news,
    delete_news_by_id,
    get_news_by_id,
    list_news,
)

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


@router.get(
    "/news/{news_id}",
    response_model=NewsRead,
    summary="Obter noticia por id",
    description="Retorna uma unica noticia pelo identificador numerico persistido no banco.",
    response_description="Dados completos da noticia.",
)
async def get_news_by_id_route(
    news_id: int = Path(
        ...,
        ge=1,
        description="Identificador da noticia no banco de dados.",
        examples=[1],
    ),
    session: AsyncSession = Depends(get_session),
) -> NewsRead:
    item = await get_news_by_id(session=session, news_id=news_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noticia nao encontrada.",
        )
    return NewsRead.model_validate(item)


@router.delete(
    "/news/{news_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover noticia por id",
    description=(
        "Remove uma noticia pelo id. Exige header X-API-Key igual a NEWS_DELETE_API_KEY "
        "no servidor; se a variavel nao estiver definida, o endpoint responde 403."
    ),
    dependencies=[Depends(require_delete_news_api_key)],
)
async def delete_news_route(
    news_id: int = Path(
        ...,
        ge=1,
        description="Identificador da noticia a remover.",
        examples=[1],
    ),
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await delete_news_by_id(session=session, news_id=news_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noticia nao encontrada.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
