from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from backend.database import get_db
from backend.models import User, AgentConfig, Experiment, ExperimentStatus as ExperimentStatusEnum
from backend.schemas import ExperimentCreate, ExperimentResponse, ExperimentStatus
from backend.security import get_current_user
from backend.agent_engine import run_agent

router = APIRouter()


@router.get("/", response_model=List[ExperimentResponse])
async def list_experiments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiments = db.query(Experiment).join(AgentConfig).filter(
        AgentConfig.user_id == current_user.id
    ).all()
    return experiments


@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = db.query(Experiment).join(AgentConfig).filter(
        Experiment.id == experiment_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )

    return experiment


@router.post("/", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    experiment_data: ExperimentCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify agent ownership
    agent = db.query(AgentConfig).filter(
        AgentConfig.id == experiment_data.agent_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    # Create experiment
    experiment = Experiment(
        agent_id=experiment_data.agent_id,
        input_data=experiment_data.input_data,
        status=ExperimentStatusEnum.PENDING
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    # Run agent in background
    background_tasks.add_task(run_agent, experiment.id)

    return experiment


@router.get("/{experiment_id}/status", response_model=ExperimentStatus)
async def get_experiment_status(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = db.query(Experiment).join(AgentConfig).filter(
        Experiment.id == experiment_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )

    return {"status": experiment.status.value}


@router.get("/{experiment_id}/results", response_model=ExperimentResponse)
async def get_experiment_results(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiment = db.query(Experiment).join(AgentConfig).filter(
        Experiment.id == experiment_id,
        AgentConfig.user_id == current_user.id
    ).first()

    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )

    if experiment.status not in [ExperimentStatusEnum.COMPLETED, ExperimentStatusEnum.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Experiment is not completed yet"
        )

    return experiment
