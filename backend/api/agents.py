from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import User, AgentConfig
from backend.schemas import AgentConfigCreate, AgentConfigUpdate, AgentConfigResponse
from backend.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[AgentConfigResponse])
async def list_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agents = db.query(AgentConfig).filter(AgentConfig.user_id == current_user.id).all()
    return agents


@router.get("/{agent_id}", response_model=AgentConfigResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(AgentConfig).filter(
        AgentConfig.id == agent_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    return agent


@router.post("/", response_model=AgentConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = AgentConfig(
        name=agent_data.name,
        framework=agent_data.framework,
        config=agent_data.config,
        user_id=current_user.id
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


@router.put("/{agent_id}", response_model=AgentConfigResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(AgentConfig).filter(
        AgentConfig.id == agent_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    update_data = agent_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    db.commit()
    db.refresh(agent)

    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    agent = db.query(AgentConfig).filter(
        AgentConfig.id == agent_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    db.delete(agent)
    db.commit()

    return None
