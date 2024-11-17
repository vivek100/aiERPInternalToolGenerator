from langchain_community.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.chains import LLMChain
from src.prompts.code_generation_prompts import code_generation_prompt
from src.utils.memory_utils import create_memory
from src.config.settings import settings
from enum import Enum
import logging

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

def create_code_generation_chain(model_provider: ModelProvider = ModelProvider.OPENAI):
    """Create the code generation chain."""
    try:
        llm = get_llm(model_provider)
        logger.debug(f"Created LLM using provider: {model_provider}")

        code_gen_chain = LLMChain(
            llm=llm,
            prompt=code_generation_prompt,
            output_key="code_structure",
            verbose=True,
            memory=create_memory(
                input_key="phase",
                output_key="code_structure"
            )
        )

        return code_gen_chain
        
    except Exception as e:
        logger.error(f"Error creating code generation chain: {str(e)}")
        raise 