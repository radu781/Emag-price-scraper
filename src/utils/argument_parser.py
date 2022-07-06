from enum import Enum, auto
from typing import Any
from flask.wrappers import Request
from dataclasses import dataclass, field


class Method(Enum):
    Get = auto()
    Post = auto()


class ArgType(Enum):
    Mandatory = auto()
    Optional = auto()
    Similar = auto()


@dataclass(frozen=True, eq=True)
class Argument:
    key: str
    type: ArgType
    default_value: Any


class ArgsNotFoundException(Exception):
    def __init__(self, args: list[str]) -> None:
        super().__init__(args)


@dataclass(frozen=True, eq=True)
class ArgumentParser:
    url: Request
    args: set[Argument]
    method: Method = field(default=Method.Get)

    def get_values(self) -> dict[str, str]:
        out: dict[str, str] = {}
        not_found: list[str] = []

        match self.method:
            case Method.Post:
                for arg in self.args:
                    if arg.type == ArgType.Mandatory and not arg.key in self.url.form:
                        not_found.append(arg.key)
                    elif arg.type == ArgType.Similar:
                        for item in self.url.form:
                            if item.find(arg.key) != -1:
                                out[arg.key] = item.split(arg.key)[1]
                    else:
                        out[arg.key] = self.url.form.get(arg.key, arg.default_value, type=str) 
            case Method.Get:
                for arg in self.args:
                    if arg.type == ArgType.Mandatory and not arg.key in self.url.args:
                        not_found.append(arg.key)
                    else:
                        out[arg.key] = self.url.args.get(arg.key, arg.default_value, type=str) 
        if not_found != []:
            raise ArgsNotFoundException(not_found)

        return out
