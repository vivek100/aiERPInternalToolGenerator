from langchain_community.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain, SequentialChain
from src.prompts.requirements_prompts import (
    functional_requirements_prompt,
    technical_requirements_prompt
)
from src.utils.memory_utils import create_memory
from src.config.settings import settings
from enum import Enum
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

def get_llm(provider: ModelProvider, streaming: bool = False):
    """Create LLM based on provider choice."""
    if provider == ModelProvider.OPENAI:
        return ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4-0125-preview",
            api_key=settings.openai_api_key,
            streaming=streaming
        )
    elif provider == ModelProvider.ANTHROPIC:
        return ChatAnthropic(
            temperature=0.7,
            model="claude-3-sonnet-20240229",
            anthropic_api_key=settings.anthropic_api_key,
            streaming=streaming
        )
    else:
        raise ValueError(f"Unsupported model provider: {provider}")

def create_requirements_chain(model_provider: ModelProvider = ModelProvider.OPENAI):
    """Create the requirements generation chain."""
    try:
        # Create LLMs
        functional_llm = get_llm(model_provider)
        technical_llm = get_llm(model_provider)
        
        logger.debug(f"Created LLMs using provider: {model_provider}")

        # Create memory
        functional_memory = create_memory(
            input_key="user_input",
            output_key="functional_requirements"
        )

        technical_memory = create_memory(
            input_key="functional_requirements",
            output_key="technical_requirements"
        )

        # Create chains
        functional_chain = LLMChain(
            llm=functional_llm,
            prompt=functional_requirements_prompt,
            output_key="functional_requirements",
            memory=functional_memory
        )

        technical_chain = LLMChain(
            llm=technical_llm,
            prompt=technical_requirements_prompt,
            output_key="technical_requirements",
            memory=technical_memory
        )

        # Combine chains
        requirements_chain = SequentialChain(
            chains=[functional_chain, technical_chain],
            input_variables=["user_input"],
            output_variables=["functional_requirements", "technical_requirements"],
            verbose=True
        )

        return requirements_chain

    except Exception as e:
        logger.error(f"Error creating requirements chain: {str(e)}")
        raise 