"""
加载限制卡数据

官方规定的限制卡有三种：

1. 禁止卡：不允许加入牌组

2. 限制卡：只能够放一张在牌组

3. 准限制卡：最多能放两张在牌组
"""

import re


class LimitCard(object):
    """限制卡数据库"""

    def __init__(self, card_data_path):
        self.card_data_path = card_data_path
        # 数据结构：{限表名: {卡号: 次数}}
        self.limit_cards = {}
        self.limit_name_list = []
        self.init_card_data()

    def init_card_data(self):
        current_list = None
        with open(self.card_data_path, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                if line.startswith("!"):
                    list_name = line.strip()[1:]
                    current_list = list_name
                    self.limit_name_list.append(list_name)
                    self.limit_cards.setdefault(list_name, {})
                    continue
                if not self.is_card_number(line):
                    continue
                if current_list is not None:
                    number, limit, _ = line.split(maxsplit=2)
                    self.limit_cards[current_list][int(number)] = int(limit)

    def is_card_number(self, data):
        """卡片码最短 5 位，判断行数据前 5 个字符是否位数字

        :returns: True 或 False
        """
        return re.match(r"^\d{5,}", data) is not None

    def get_limit_number(self, card_number):
        # NOTE: 按文件格式规律，第一个是 OCG 的限卡表，默认只查 OCG 的
        # 暂时没考虑 TCG
        new_list = self.limit_name_list[0]
        return self.limit_cards[new_list].get(card_number, None)
