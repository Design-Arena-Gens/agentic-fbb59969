import asyncio
from datetime import datetime
from backend.database import SessionLocal
from backend.models import Experiment, AgentConfig, ExperimentStatus, FrameworkType
from backend.config import settings


def run_agent(experiment_id: int):
    """Run agent experiment in background"""
    db = SessionLocal()
    try:
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            return

        # Update status to running
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.utcnow()
        db.commit()

        # Get agent config
        agent = db.query(AgentConfig).filter(AgentConfig.id == experiment.agent_id).first()
        if not agent:
            experiment.status = ExperimentStatus.FAILED
            experiment.error = "Agent not found"
            experiment.completed_at = datetime.utcnow()
            db.commit()
            return

        # Execute agent based on framework
        try:
            if agent.framework == FrameworkType.CREWAI:
                result = run_crewai_agent(agent.config, experiment.input_data)
            elif agent.framework == FrameworkType.LANGCHAIN:
                result = run_langchain_agent(agent.config, experiment.input_data)
            elif agent.framework == FrameworkType.OPENAI:
                result = run_openai_agent(agent.config, experiment.input_data)
            else:
                raise ValueError(f"Unsupported framework: {agent.framework}")

            experiment.status = ExperimentStatus.COMPLETED
            experiment.result = result
            experiment.completed_at = datetime.utcnow()

        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.error = str(e)
            experiment.completed_at = datetime.utcnow()

        db.commit()

    except Exception as e:
        print(f"Error running agent: {e}")
    finally:
        db.close()


def run_crewai_agent(config: dict, input_data: dict) -> dict:
    """Run CrewAI agent"""
    try:
        from crewai import Agent, Task, Crew

        agent = Agent(
            role=config.get("role", "Assistant"),
            goal=config.get("goal", "Help the user"),
            backstory=config.get("backstory", "Helpful assistant"),
            verbose=config.get("verbose", False),
        )

        task_description = input_data.get("task", "Complete the assigned task")
        task = Task(
            description=task_description,
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
        )

        result = crew.kickoff()

        return {
            "framework": "crewai",
            "output": str(result),
            "config": config,
        }
    except Exception as e:
        return {
            "framework": "crewai",
            "error": str(e),
            "message": "CrewAI execution failed. Make sure API keys are configured.",
        }


def run_langchain_agent(config: dict, input_data: dict) -> dict:
    """Run Langchain agent"""
    try:
        from langchain.llms import OpenAI
        from langchain.agents import initialize_agent, AgentType

        llm = OpenAI(
            model=config.get("llm", "gpt-3.5-turbo-instruct"),
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 2000),
            openai_api_key=settings.OPENAI_API_KEY,
        )

        agent = initialize_agent(
            tools=[],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=config.get("verbose", False),
        )

        prompt = input_data.get("prompt", "Hello!")
        result = agent.run(prompt)

        return {
            "framework": "langchain",
            "output": result,
            "config": config,
        }
    except Exception as e:
        return {
            "framework": "langchain",
            "error": str(e),
            "message": "Langchain execution failed. Make sure API keys are configured.",
        }


def run_openai_agent(config: dict, input_data: dict) -> dict:
    """Run OpenAI agent"""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        messages = [
            {"role": "system", "content": config.get("system_message", "You are a helpful assistant")},
            {"role": "user", "content": input_data.get("prompt", "Hello!")},
        ]

        response = client.chat.completions.create(
            model=config.get("model", "gpt-3.5-turbo"),
            messages=messages,
            temperature=config.get("temperature", 0.7),
            max_tokens=config.get("max_tokens", 1500),
        )

        return {
            "framework": "openai",
            "output": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "config": config,
        }
    except Exception as e:
        return {
            "framework": "openai",
            "error": str(e),
            "message": "OpenAI execution failed. Make sure API keys are configured.",
        }
