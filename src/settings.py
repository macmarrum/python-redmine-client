# Copyright (C) 2026  macmarrum (at) outlook (dot) ie
# SPDX-License-Identifier: Apache-2.0
import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

me = Path(__file__)
CONFIG_PATH = me.parent / 'redmine.toml'


class Env(Enum):
    prod = 'prod'
    staging = 'staging'
    local = 'local'


@dataclass
class Settings:
    base_url: str
    api_key: str

    @classmethod
    def from_toml(cls, path: Path, env: Env):
        with open(path, 'rb') as f:
            return cls(**tomllib.load(f)[env.name])

    @classmethod
    def of(cls, env: Env):
        return cls.from_toml(CONFIG_PATH, env)
