import json
from logging import Filter

__author__ = 'nengfang.han'


class KafkaFilter(Filter):
    def filter(self, record):
        return super().filter(record)


class MineLogFilter(Filter):
    def filter(self, record):
        return super().filter(record)
