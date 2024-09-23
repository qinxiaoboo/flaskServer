from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TaskData:
    # 完成任务个数
    count: int = 0

    # 积分记录
    credits: int = 0

    #
    OnssCoin_Num: int = 0

    CheckIn_DaysCount: int = 0

    #
    level_1: int = 0

    level_2: int = 0

    level_3: int = 0

    level_4: int = 0

    level_5: int = 0


@dataclass_json
@dataclass
class oneneselabs:
    # 示例
    a=0