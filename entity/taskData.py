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
class TaskChain:
    # 签到天数
    check_in: int = 0
    #排名
    Leaderboard: int = 0
    #领水次数
    Faucet: int = 0
    #交互
    Swap: int = 0
    #流动性
    Liquidity: int = 0
    #桥
    Bridge: int = 0
    #总分
    PointsCount: int = 0

@dataclass_json
@dataclass
class TaskDeek:
    #积分
    Points: str = 0
    #排名
    top: str = 0

@dataclass_json
@dataclass
class TaskPortal:
    XP: int = 0

@dataclass_json
@dataclass
class TaskDiamante:
    #积分
    Points: str = 0


@dataclass_json
@dataclass
class TaskPassport:

    Score: float = 0

@dataclass_json
@dataclass
class TaskHighlayer:
    #总分
    Total: str = 0

@dataclass_json
@dataclass
class TaskArch:
    #总分
    Level: str = 0
    Total: str = 0

@dataclass_json
@dataclass
class TaskHumanity:
    #总分
    Rewards_Balance: str = 0
    #排名
    Ranking: str = 0
    #签到得分
    Rewards: str = 0
    #前天得分
    Rewards_Yesterday: str = 0
    #钱包
    wallet: str = 0


@dataclass_json
@dataclass
class TaskTheoriq:
    #总分
    Your_xp: str = 0
    #排名
    Your_rank: str = 0
    #任务完成情况
    Completed_Quests: str = 0
