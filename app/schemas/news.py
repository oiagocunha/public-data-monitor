from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str = Field(
        description="Estado atual da API. Retorna 'ok' quando a aplicacao esta saudavel.",
        examples=["ok"],
    )


class CollectNewsResponse(BaseModel):
    inserted: int = Field(
        description="Quantidade de noticias novas inseridas no banco nesta execucao.",
        examples=[12],
        ge=0,
    )


class NewsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Identificador unico da noticia no banco.")
    title: str = Field(description="Titulo principal da noticia.")
    summary: str = Field(description="Resumo curto do conteudo da noticia.")
    url: str = Field(description="URL canonica da noticia na fonte original.")
    source: str = Field(description="Nome da fonte de origem da noticia.", examples=["g1"])
    published_at: datetime | None = Field(
        description=(
            "Data e hora de publicacao informada pela fonte original, quando extraida do HTML. "
            "Pode ser nulo quando a origem nao expoe o dado de forma estruturada ou consistente "
            "no markup — nesse caso o registro e mantido com titulo e URL validos."
        ),
    )


class NewsPage(BaseModel):
    items: list[NewsRead] = Field(description="Lista de noticias da pagina atual.")
    limit: int = Field(description="Quantidade maxima de itens solicitada.")
    offset: int = Field(description="Quantidade de itens pulados antes desta pagina.")
    total: int = Field(description="Total de noticias cadastradas no banco.")
    has_next: bool = Field(description="Indica se existe uma proxima pagina para consulta.")
