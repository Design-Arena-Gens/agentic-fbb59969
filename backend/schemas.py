from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from backend.models import FrameworkType, ExperimentStatus


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    preferences: Optional[Dict[str, Any]] = {}
    created_at: datetime

    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Agent Schemas
class AgentConfigBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    framework: FrameworkType
    config: Dict[str, Any]

    @validator("framework")
    def validate_framework(cls, v):
        if v not in [FrameworkType.CREWAI, FrameworkType.LANGCHAIN, FrameworkType.OPENAI]:
            raise ValueError("Invalid framework type")
        return v


class AgentConfigCreate(AgentConfigBase):
    pass


class AgentConfigUpdate(BaseModel):
    name: Optional[str] = None
    framework: Optional[FrameworkType] = None
    config: Optional[Dict[str, Any]] = None


class AgentConfigResponse(AgentConfigBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Experiment Schemas
class ExperimentCreate(BaseModel):
    agent_id: int
    input_data: Optional[Dict[str, Any]] = {}


class ExperimentResponse(BaseModel):
    id: int
    agent_id: int
    status: ExperimentStatus
    input_data: Optional[Dict[str, Any]] = {}
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExperimentStatus(BaseModel):
    status: str
