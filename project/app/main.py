from typing import Any
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from structlog import get_logger
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Policy
from common.errors.policy_not_found_error import PolicyNotFoundError

app = FastAPI()
logger = get_logger(__name__)


@app.get("/health", summary="App health check", status_code=200)
async def health_check() -> Any:
    """health check route"""
    logger.debug("health_check")
    return {"status": "healthy"}


@app.get(
    "/policies/{policy_id}",
    summary="Gets a policy by id",
    status_code=200,
    responses={404: {"description": "Policy not found"}},
    response_model=Policy,
)
async def get_policy_by_id(
    policy_id: int, session: AsyncSession = Depends(get_session)
) -> Policy:
    """get a policy by id"""
    logger.debug("get_policy_by_id")

    id = policy_id
    try:
        result = await session.execute(select(Policy, id))
    except PolicyNotFoundError:
        return JSONResponse(status_code=404, content="Policy not found")

    return result
