from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TG:
    url:str = "https://web.telegram.org/k/"
    name:str = ""
    userName:str = ""
    phone:str = ""

@dataclass_json
@dataclass
class SaHaRa:
    rank:str = ""
    points:str=""
    setTwitter:bool=False