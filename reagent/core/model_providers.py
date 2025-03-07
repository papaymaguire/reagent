from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Type

from ..types.configs import ModelConfig
from .messages import Completion, CompletionChunk, Message
from .tools import Tool

_provider_registry: Dict[str, Type["ModelProvider"]] = {}


def provider_factory(provider_name: str, **kwargs) -> "ModelProvider":
    """
    Factory method to create a model provider instance.

    Args:
        provider_name (str): Name of the provider to create.
        **kwargs: Configuration parameters for the provider.

    Returns:
        ModelProvider: An instance of the requested provider.

    Raises:
        ValueError: If the provider name is not registered.
    """
    provider_cls = _provider_registry.get(provider_name)
    if provider_cls is None:
        registered_providers = ", ".join(_provider_registry.keys())
        raise ValueError(
            f"Unknown provider '{provider_name}'. "
            f"Available providers are: {registered_providers}"
        )
    return provider_cls(**kwargs)


class ModelProvider(ABC):
    """
    Abstract base class defining the interface for AI model providers.

    This class serves as a template for implementing different model providers
    like OpenAI, Anthropic, etc. It defines the required methods that all
    model providers must implement.
    """

    def __init_subclass__(cls, **kwargs):
        """Register provider classes when they are defined."""
        super().__init_subclass__(**kwargs)
        _provider_registry[cls.__name__.lower()] = cls

    @abstractmethod
    async def complete(
        self,
        *,
        model_config: ModelConfig,
        messages: List[Message],
        tools: List[Tool],
    ) -> Completion:
        """
        Performs an asynchronous completion request to the model.

        Args:
            model_config (ModelConfig): The model configuration to be used for the completion.
            messages (List[Message]): The input message to send to the model.
            tools (List[Tool]): The tools available to the model.

        Returns:
            Completion: The model's response.
        """
        pass

    @abstractmethod
    async def stream(
        self,
        *,
        model_config: ModelConfig,
        messages: List[Message],
        tools: List[Tool],
    ) -> AsyncGenerator[CompletionChunk, None]:
        """
        Performs an asynchronous streaming completion request to the model.

        Args:
            model_config (ModelConfig): The model configuration to be used for the completion.
            messages (List[Message]): The input message to send to the model.
            tools (List[Tool]): The tools available to the model.

        Returns:
            AsyncGenerator[CompletionChunk, None]: An async generator that yields response chunks.
        """
        pass
