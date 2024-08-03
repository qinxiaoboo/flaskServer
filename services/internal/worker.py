import asyncio
import random
from datetime import datetime
from pathlib import Path
from flaskServer.config.config import WORK_PATH,RANDOM_ORDER, SKIP_FIRST_ACCOUNTS, WAIT_BETWEEN_ACCOUNTS, THREADS_NUM
import aiofiles
from loguru import logger


async def process_batch(bid: int, batch, async_func, sleep):
    await asyncio.sleep(WAIT_BETWEEN_ACCOUNTS[0] / THREADS_NUM * bid)
    failed = []
    for idx, d in enumerate(batch):
        if sleep and idx != 0:
            await asyncio.sleep(random.uniform(WAIT_BETWEEN_ACCOUNTS[0], WAIT_BETWEEN_ACCOUNTS[1]))
        try:
            await async_func(d)
        except Exception as e:
            failed.append(d)
            await log_long_exc(d.name, 'Process account error', e)
        print()
    return failed

async def log_long_exc(idx, msg, exc, warning=False, to_file=True):
    e_msg = str(exc)
    if e_msg == '':
        e_msg = ' '
    e_msg_lines = e_msg.splitlines()
    if warning:
        logger.warning(f'{idx}) {msg}: {e_msg_lines[0]}')
    else:
        logger.error(f'{idx}) {msg}: {e_msg_lines[0]}')
    if len(e_msg_lines) > 1 and to_file:
        async with aiofiles.open(Path(WORK_PATH) / Path(r'flaskServer\logs\errors.txt'), 'a', encoding='utf-8') as file:
            await file.write(f'{str(datetime.now())} | {idx}) {msg}: {e_msg}\n\n')
            await file.flush()

def get_batches(skip: int = None, threads: int = THREADS_NUM,data = []):
    _data = data
    if skip is not None:
        _data = _data[skip:]
    if RANDOM_ORDER:
        random.shuffle(_data)
    _batches = [[] for _ in range(threads)]
    for _idx, d in enumerate(_data):
        _batches[_idx % threads].append(d)
    return _batches

async def process(batches, async_func, sleep=True):
    tasks = []
    for idx, b in enumerate(batches):
        tasks.append(asyncio.create_task(process_batch(idx, b, async_func, sleep)))
    return await asyncio.gather(*tasks)

def worker(datas,func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(process(get_batches(SKIP_FIRST_ACCOUNTS, data=datas), func))
    return results

