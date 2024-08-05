from flaskServer.services.dto.galxeAccount import getAccountByEnv
from flaskServer.services.internal.galxe.account import GalxeAccount, wait_a_bit
from flaskServer.services.dto.space_points import updateSpacePoints
from flaskServer.services.internal.worker import worker
from flaskServer.initData.galxe_points import init
from flaskServer.config.config import GALXE_CAMPAIGN_IDS
from loguru import logger


async def process_env(env):
    account = getAccountByEnv(env)
    async with  GalxeAccount(account.idx, account, account.evm_private_key) as galxe_account:
        logger.info(f'{account.idx}) Galxe signing in')
        await galxe_account.login()
        logger.info(f'{account.idx}) Galxe signed in')
        await wait_a_bit()

        # for campaign_id in GALXE_CAMPAIGN_IDS:
        #     await galxe_account.complete_campaign(campaign_id)
        #     await galxe_account.claim_campaign(campaign_id)
        #
        # await wait_a_bit()

        logger.info(f'{account.idx}) Checking spaces stats')
        await galxe_account.spaces_stats()
        for key, value in account.spaces_points.items():
            updateSpacePoints(account.idx, key, value[0], value[1], value[2])

def todo():
    from flaskServer.mode.env import Env
    from flaskServer.config.connect import app
    with app.app_context():
        envs = Env.query.all()
        result = worker(envs,process_env)
        logger.info(f"Galxe 采集任务执行完成")
        p = init()
        logger.info(f"Galxe 任务详情已生成文件：{p.absolute()}")

if __name__ == '__main__':
    todo()