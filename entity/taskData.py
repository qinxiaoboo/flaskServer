from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TaskData:
    # 完成任务个数
    count:int=0