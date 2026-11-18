import os

from fastapi import FastAPI, Path, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from src.domain.service import BadRequest, CitizenService, NotFound, ProviderUnavailable
from src.infra.answer_provider import FakeAnswerProvider
from src.infra.repository import InMemoryPointRepository


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    point_id: str = Field(min_length=1, max_length=50)
    question: str = Field(min_length=1, max_length=300)


def error_response(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def create_app(service: CitizenService | None = None) -> FastAPI:
    if service is None:
        if os.getenv("AI_PROVIDER", "fake") != "fake":
            raise ValueError("Somente AI_PROVIDER=fake está implementado no slice.")
        service = CitizenService(InMemoryPointRepository(), FakeAnswerProvider())
    app = FastAPI(title="EcoPontos Cidadãos API", version="1.0.0")

    @app.exception_handler(RequestValidationError)
    async def validation_error(_request: Request, _error: RequestValidationError):
        return error_response("VALIDATION_ERROR", "Entrada inválida ou fora dos limites.", 422)

    @app.exception_handler(NotFound)
    async def not_found(_request: Request, error: NotFound):
        return error_response("NOT_FOUND", str(error), 404)

    @app.exception_handler(BadRequest)
    async def bad_request(_request: Request, error: BadRequest):
        return error_response("BAD_REQUEST", str(error), 400)

    @app.exception_handler(ProviderUnavailable)
    async def unavailable(_request: Request, error: ProviderUnavailable):
        return error_response("AI_UNAVAILABLE", str(error), 503)

    @app.get("/points")
    def list_points(limit: int = Query(10, ge=1, le=100),
                    offset: int = Query(0, ge=0, le=10000),
                    material: str | None = Query(None, pattern="^(papel|plastico|vidro|metal)$")):
        return service.list_points(limit, offset, material)

    @app.get("/points/{id}")
    def get_point(id: str = Path(min_length=1, max_length=50)):
        return service.get_point(id)

    @app.post("/ask")
    def ask(body: AskRequest):
        return service.ask(body.point_id, body.question)

    return app


app = create_app()
