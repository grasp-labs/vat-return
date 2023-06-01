"""
Service configuration set with parameters in .env and .pem files.

Filenames:
    .env
    virksomhetssertifikat.pem
    private.pem
"""
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

BASE_PATH = path = Path(__file__).parent.parent.parent


@dataclass
class Config:
    username: str
    password: str
    api_key: str
    client_id: str
    scope_test: str
    private_key: str = None
    virksomhetssertifikat: str = None


def read_pem_keys(file_path: str = None, private: bool = True):
    """

    :param file_path:
    :param private:
    :return:
    """
    if not file_path:
        file_path = BASE_PATH / "private.pem" if private else BASE_PATH / "virksomhetssertifikat.pem"
    with open(file_path, "r") as file:
        cert = file.read()

    if private:
        return cert

    pattern = r'-----BEGIN CERTIFICATE-----\n(.+)\n-----END CERTIFICATE-----'
    matches = re.search(pattern, cert, re.DOTALL)
    if matches:
        cert = matches.group(1)
    return cert


def read_env_file(file_path: str = None) -> Dict:
    """Loads .env file and returns config datamodel."""
    if not file_path:
        file_path = BASE_PATH / ".env"

    with open(file_path, 'r') as f:
        lines = f.readlines()
    env_vars = {}

    for line in lines:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            env_vars[key.lower()] = value
    env_vars["private_key"] = read_pem_keys(private=True)
    env_vars["virksomhetssertifikat"] = read_pem_keys(private=False)
    return env_vars


config = Config(**read_env_file())
