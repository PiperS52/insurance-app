from typing import Any, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from structlog import get_logger
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Policy

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

    result = await session.get(Policy, id)
    if result is None:
        return JSONResponse(status_code=404, content="Policy not found")

    return result

@app.get("/policies", response_model=list[Policy])
async def get_policies(
    session: AsyncSession = Depends(get_session)
) -> List[Policy]:
    """get a list of movies"""
    logger.debug("get_movies")

    result = await session.execute(select(Policy))
    policies = result.scalars().all()
    return [Policy(
        title=policy.title,
        date=policy.date,
        type=policy.type,
        name=policy.name,
        wording=policy.wording,
        price=policy.price,
        id=policy.id
    ) for policy in policies]
