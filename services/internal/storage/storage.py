import os
import json
import asyncio

class Storage:

    def __init__(self, filename: str):
        self.filename = filename
        self.data = {}
        self.lock = asyncio.Lock()

    def init(self):
        if not os.path.exists(self.filename):
            self.data = {}
            return
        with open(self.filename, 'r', encoding='utf-8') as file:
            if len(file.read().strip()) == 0:
                self.data = {}
                return
        with open(self.filename, 'r', encoding='utf-8') as file:
            converted_data = json.load(file)
        self.data = converted_data

    def get_final_value(self, key: str):
        value = self.data.get(key)
        if value is None:
            return None
        return deepcopy(value)

    def set_final_value(self, key: str, value):
        self.data[key] = deepcopy(value)

    def remove(self, key: str):
        if key in self.data:
            self.data.pop(key)

    async def get_value(self, key: str):
        async with self.lock:
            return self.get_final_value(key)

    async def set_value(self, key: str, value):
        async with self.lock:
            self.set_final_value(key, value)

    async def async_save(self):
        async with self.lock:
            self.save()

    def save(self):
        self._save(self.data)

    def _save(self, converted_data):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(converted_data, file)
