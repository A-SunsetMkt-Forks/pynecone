"""Utilities for working with registries."""

import httpx

from reflex.config import environment
from reflex.utils import console, net


def latency(registry: str) -> int:
    """Get the latency of a registry.

    Args:
        registry (str): The URL of the registry.

    Returns:
        int: The latency of the registry in microseconds.
    """
    try:
        return net.get(registry).elapsed.microseconds
    except httpx.HTTPError:
        console.info(f"Failed to connect to {registry}.")
        return 10_000_000


def average_latency(registry: str, attempts: int = 3) -> int:
    """Get the average latency of a registry.

    Args:
        registry: The URL of the registry.
        attempts: The number of attempts to make. Defaults to 10.

    Returns:
        The average latency of the registry in microseconds.
    """
    return sum(latency(registry) for _ in range(attempts)) // attempts


def _get_best_registry() -> str:
    """Get the best registry based on latency.

    Returns:
        The best registry.
    """
    registries = [
        "https://registry.npmjs.org",
        "https://r.cnpmjs.org",
    ]

    return min(registries, key=average_latency)


def get_npm_registry() -> str:
    """Get npm registry. If environment variable is set, use it first.

    Returns:
        The npm registry.
    """
    return environment.NPM_CONFIG_REGISTRY.get() or _get_best_registry()
