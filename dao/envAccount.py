from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class EnvAccountInfo:
    id:int=0
    group:str=""
    env:str=""
    tw:str=""
    tw_status:int=0
    tw_error:str=""
    discord:str=""
    discord_status:int=0
    discord_error:str=""
    outlook:str=""
    outlook_status:int=0
    outlook_error:str=""
    ip:str=""
    status:str=""
    label:str=""
