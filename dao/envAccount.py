from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class EnvAccountInfo:
    id:int=0
    group:str=""
    env:str=""
    tw:str=""
    discord:str=""
    outlook:str=""
    ip:str=""
    status:str=""
    label:str=""
