from typing import Type

from pydantic import (
    BaseModel,
    Field,
    create_model,
)

from popug_sdk.conf import settings


class PaginationMetaSchema(BaseModel):
    page: int
    page_size: int
    count: int


class ResponseMetaSchema(BaseModel):
    app: str = settings.project


def get_list_response_schema(
    schema: Type[BaseModel],
    meta_schema: Type[BaseModel] = ResponseMetaSchema,
    suffix: str = "",
) -> Type[BaseModel]:
    name = schema.__name__.removesuffix("Schema")
    paginated_meta_schema = create_model(
        f"Pagination{meta_schema.__name__}",
        __base__=meta_schema,
        pagination=(PaginationMetaSchema, ...),
    )

    return create_model(
        f"{name}{suffix}ListResponseSchema",
        meta=(
            paginated_meta_schema,
            Field(default_factory=paginated_meta_schema),
        ),
        result=(list[schema], Field(default_factory=list)),  # type: ignore
    )


def get_response_schema(
    schema: Type[BaseModel],
    response_meta: Type[BaseModel] = ResponseMetaSchema,
    suffix: str = "",
) -> Type[BaseModel]:
    name = schema.__name__.removesuffix("Schema")

    return create_model(
        f"{name}{suffix}ResponseSchema",
        meta=(response_meta, Field(default_factory=response_meta)),
        result=(schema, ...),
    )
