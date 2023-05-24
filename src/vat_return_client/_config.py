"""
Service configuration set with parameters in .env file.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class Config:
    client_id: str
    scope: str


def read_env_file(file_path: str = None) -> Dict:
    """Loads .env file and returns config datamodel."""
    if not file_path:
        file_path = Path(__file__).parent.parent.parent / ".env"

    with open(file_path, 'r') as f:
        lines = f.readlines()
    env_vars = {}

    for line in lines:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            env_vars[key.lower()] = value

    return env_vars


config = Config(**read_env_file())
