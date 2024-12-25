import time
import uuid


class FakeRedis:
    def __init__(self):
        self.data = {}
        self.expired_keys = set()  # 存储过期的键，避免频繁检查
        self.last_cleanup_time = time.time()  # 上次清理的时间
        self.cleanup_interval = 10  # 每10秒清理一次过期键

    # 清理过期键
    def _clean_expired(self):
        current_time = time.time()
        # 如果距离上次清理已经过去了一定的时间，进行一次清理
        if current_time - self.last_cleanup_time > self.cleanup_interval:
            expired_keys = {key for key, value in self.data.items()
                            if value.get('expire_at') and value['expire_at'] < current_time}
            for key in expired_keys:
                del self.data[key]
            self.expired_keys.clear()  # 清空过期键缓存
            self.last_cleanup_time = current_time  # 更新上次清理时间

    def set(self, key, value, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        self.data[key] = {'value': value, 'expire_at': expire_at}
        self._clean_expired()  # 设置时清理过期键
        return "OK"

    def get(self, key):
        self._clean_expired()  # 获取时清理过期键
        if key in self.data:
            item = self.data[key]
            if item['expire_at'] and item['expire_at'] < time.time():
                del self.data[key]
                return None
            return item['value']
        return None

    def del_key(self, key):
        self._clean_expired()  # 删除时清理过期键
        if key in self.data:
            del self.data[key]
            return 1
        return 0

    def exists(self, key):
        self._clean_expired()  # 检查时清理过期键
        return 1 if key in self.data else 0

    def ttl(self, key):
        self._clean_expired()  # TTL时清理过期键
        if key in self.data:
            item = self.data[key]
            if item['expire_at']:
                remaining_time = item['expire_at'] - time.time()
                return max(remaining_time, 0)
        return -1

    def flushdb(self):
        self.data.clear()
        self.expired_keys.clear()
        return "OK"

    # 其他操作（哈希、列表、集合等）同理，增加过期时间检查
    # 示例：列表操作
    def lpush(self, key, value, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        if key not in self.data:
            self.data[key] = {'list': []}
        self.data[key]['list'].insert(0, {'value': value, 'expire_at': expire_at})
        self._clean_expired()  # 每次修改列表时清理过期键
        return len(self.data[key]['list'])

    def rpush(self, key, value, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        if key not in self.data:
            self.data[key] = {'list': []}
        self.data[key]['list'].append({'value': value, 'expire_at': expire_at})
        self._clean_expired()  # 每次修改列表时清理过期键
        return len(self.data[key]['list'])

    def llen(self, key):
        self._clean_expired()  # 获取列表长度时清理过期键
        if key in self.data:
            return len(self.data[key].get('list', []))
        return 0

    # 扩展哈希、集合等操作，遵循同样的原则
    # 哈希操作
    def hset(self, key, field, value, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        if key not in self.data:
            self.data[key] = {}
        self.data[key][field] = {'value': value, 'expire_at': expire_at}
        self._clean_expired()  # 每次修改哈希时清理过期键
        return 1

    def hget(self, key, field):
        self._clean_expired()  # 获取哈希字段时清理过期键
        if key in self.data and field in self.data[key]:
            item = self.data[key][field]
            if item['expire_at'] and item['expire_at'] < time.time():
                del self.data[key][field]
                return None
            return item['value']
        return None

    def hdel(self, key, field):
        self._clean_expired()  # 删除哈希字段时清理过期键
        if key in self.data and field in self.data[key]:
            del self.data[key][field]
            return 1
        return 0

    def hgetall(self, key):
        self._clean_expired()  # 获取哈希所有字段时清理过期键
        if key in self.data:
            return {field: item['value'] for field, item in self.data[key].items()
                    if item['expire_at'] is None or item['expire_at'] > time.time()}
        return {}

    # Set 操作
    def sadd(self, key, value, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        if key not in self.data:
            self.data[key] = {'set': set()}
        self.data[key]['set'].add({'value': value, 'expire_at': expire_at})
        self._clean_expired()  # 修改集合时清理过期键
        return len(self.data[key]['set'])

    def smembers(self, key):
        self._clean_expired()  # 获取集合时清理过期键
        if key in self.data:
            return [item['value'] for item in self.data[key].get('set', [])
                    if item['expire_at'] is None or item['expire_at'] > time.time()]
        return []

    def srem(self, key, value):
        self._clean_expired()  # 删除集合成员时清理过期键
        if key in self.data:
            for item in self.data[key]['set']:
                if item['value'] == value and (item['expire_at'] is None or item['expire_at'] > time.time()):
                    self.data[key]['set'].remove(item)
                    return 1
        return 0

    # ZSet 操作
    def zadd(self, key, score, member, ex=None):
        expire_at = None
        if ex:
            expire_at = time.time() + ex
        if key not in self.data:
            self.data[key] = {'zset': {}}
        self.data[key]['zset'][member] = {'score': score, 'expire_at': expire_at}
        self._clean_expired()  # 修改 ZSet 时清理过期键
        return 1

    def zrange(self, key, start, end):
        self._clean_expired()  # 获取 ZSet 范围时清理过期键
        if key in self.data:
            sorted_members = sorted(self.data[key]['zset'].items(), key=lambda x: x[1]['score'])
            return [member for member, item in sorted_members[start:end + 1]
                    if item['expire_at'] is None or item['expire_at'] > time.time()]
        return []

    def zrem(self, key, member):
        self._clean_expired()  # 删除 ZSet 成员时清理过期键
        if key in self.data and member in self.data[key]['zset']:
            del self.data[key]['zset'][member]
            return 1
        return 0

    # --------------- Redis 锁 ---------------
    def lock(self, lock_name, acquire_timeout=30, lock_timeout=30):
        """
        尝试获取锁，如果成功则返回锁的标识（一般是唯一的值），否则返回 None。

        :param lock_name: 锁的名字
        :param acquire_timeout: 尝试获取锁的最大时间（秒）
        :param lock_timeout: 锁的有效时间（秒），即加锁后多少秒自动释放
        :return: 锁的标识（UUID）或 None（如果获取锁失败）
        """
        lock_value = str(uuid.uuid4())  # 使用唯一值作为锁的标识
        lock_acquired = False
        lock_key = f"lock:{lock_name}"

        start_time = time.time()
        while time.time() - start_time < acquire_timeout:
            # 查看锁是否存在
            if not self.get(lock_key):
                if self.set(lock_key, lock_value, ex=lock_timeout) == "OK":
                    lock_acquired = True
                    break
            time.sleep(0.1)  # 每隔0.1秒尝试一次

        if lock_acquired:
            return lock_value  # 返回锁的标识（UUID）
        return None  # 获取锁失败

    def unlock(self, lock_name, lock_value):
        """
        释放锁，仅当锁的标识和当前持有者一致时才能释放。

        :param lock_name: 锁的名字
        :param lock_value: 锁的标识
        :return: 成功释放锁返回 True，失败返回 False
        """
        lock_key = f"lock:{lock_name}"
        current_lock_value = self.get(lock_key)

        # 检查是否是当前持有锁的用户
        if current_lock_value == lock_value:
            self.del_key(lock_key)  # 删除锁
            return True
        return False  # 如果锁标识不匹配，不能释放锁


redis = FakeRedis()

class RedisLock:
    def __init__(self, lock_name, acquire_timeout=30, lock_timeout=30):
        self.redis = redis
        self.lock_name = lock_name
        self.acquire_timeout = acquire_timeout
        self.lock_timeout = lock_timeout
        self.lock_value = None

    def __enter__(self):
        """
        在进入with语句块时自动尝试获取锁
        """
        self.lock_value = self.redis.lock(self.lock_name, self.acquire_timeout, self.lock_timeout)
        if self.lock_value is None:
            raise TimeoutError(f"Failed to acquire lock {self.lock_name}")
        return self.lock_value

    def __exit__(self, exc_type, exc_value, traceback):
        """
        在退出with语句块时自动释放锁
        """
        if self.lock_value:
            self.redis.unlock(self.lock_name, self.lock_value)


