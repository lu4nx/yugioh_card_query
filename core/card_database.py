# Author: lx@shellcodes.org

import sqlite3


def get_card_type(type_code):
    """判断卡片类型"""
    card_type = None
    if (type_code & 0x1) == 0x1:
        if (type_code & 0x4000000) == 0x4000000:
            card_type = "怪兽 连接"
        elif (type_code & 0x40) == 0x40:
            card_type = "怪兽 融合"
        elif (type_code & 0x20) == 0x20:
            card_type = "怪兽 效果"
        else:
            card_type = "怪兽"
    elif (type_code & 0x2) == 0x2:
        if (type_code & 0x10000) == 0x10000:
            card_type = "魔法 速攻"
        elif (type_code & 0x20000) == 0x20000:
            card_type = "魔法 永久"
        elif (type_code & 0x40000) == 0x40000:
            card_type = "魔法 装备"
        elif (type_code & 0x80000) == 0x80000:
            card_type = "魔法 场地"
        else:
            card_type = "魔法"
    elif (type_code & 0x4) == 0x4:
        if (type_code & 0x20000) == 0x20000:
            card_type = "陷阱 永久"
        else:
            card_type = "陷阱"

    return card_type


def get_card_attribute(attribute_code):
    return {
        0x01: "地",
        0x02: "水",
        0x04: "炎",
        0x08: "风",
        0x10: "光",
        0x20: "暗",
        0x40: "神"
    }.get(attribute_code, None)


def get_card_short_type(type_code):
    """获得卡片类型短名"""
    card_type = get_card_type(type_code)

    if card_type.find("怪兽") > -1:
        return "怪"
    elif card_type.find("魔") > -1:
        return "魔"
    elif card_type.find("陷阱") > -1:
        return "陷"
    return "?"


class Card(object):
    def __init__(self, **argv):
        self.number = argv.get("number")
        self.name = argv.get("name")
        self.type = argv.get("card_type")
        self.attribute = argv.get("attribute")
        self.attack = argv.get("attack")
        self.defense = argv.get("defense")
        self.level = argv.get("level")
        self.desc = argv.get("desc")

    def get_number(self):
        return self.number

    def get_name(self):
        return self.name

    def get_type(self):
        card_type = get_card_type(self.type)
        assert card_type is not None
        return card_type

    def get_attribute(self):
        card_attribute = get_card_attribute(self.attribute)
        assert card_attribute is not None
        return card_attribute

    def get_defense(self):
        # 防御力无限，或没有防御力的，数据库保存的值为 -2
        if self.defense == -2:
            return "?"
        # 连接怪兽没有防御力
        elif self.is_link_monster():
            return "?"
        return self.defense

    def get_attack(self):
        # 攻击力无限的，或没有攻击力的，数据库保存的值为 -2
        if self.attack == -2:
            return "?"
        return self.attack

    def get_level(self):
        # 连接怪兽没有等级，而数据库中的等级值是连接数
        if self.is_link_monster():
            return None
        return self.level

    def get_link_number(self):
        """返回连接怪兽的连接数"""
        if self.is_link_monster():
            return self.level
        return None

    def get_desc(self):
        return self.desc

    def is_monster(self):
        return self.get_type().startswith("怪兽")

    def is_link_monster(self):
        return self.is_monster() and self.get_type().startswith("连接")

    def is_spell(self):
        return self.get_type().startswith("魔法")

    def is_trap(self):
        return self.get_type().startswith("陷阱")


class CardDatabase(object):
    def __init__(self, card_db_path, card_pictures_path):
        self.card_db_path = card_db_path
        self.card_pictures_path = card_pictures_path
        self.connect = sqlite3.connect(self.card_db_path)
        self.conn = self.connect.cursor()

    def get_card_info(self, card_number):
        cursor = self.conn.execute(("select texts.id, texts.name, texts.desc,"
                                    "datas.type, datas.attribute, datas.level,"
                                    "datas.atk, datas.def from texts, datas "
                                    "where texts.id=? "
                                    "and texts.id = datas.id"),
                                   (card_number,))
        item = cursor.fetchone()
        card = Card(
            number=item[0],
            name=item[1],
            desc=item[2],
            card_type=item[3],
            attribute=item[4],
            level=item[5],
            attack=item[6],
            defense=item[7]
            )

        monster_info = self.monster_info_desc(card)
        return f"""{card.get_name()}（{card.get_number()}）

类型：{card.get_type()}
{monster_info}
{card.get_desc()}
"""

    def monster_info_desc(self, card_obj):
        if card_obj.is_monster() and card_obj.is_link_monster():
            return f"""
LINK：{card_obj.get_link_number()}，属性：{card_obj.get_attribute()}

攻击：{card_obj.get_attack()}
"""
        elif card_obj.is_monster():
            return f"""
等级：{card_obj.get_level()}，属性：{card_obj.get_attribute()}

攻击：{card_obj.get_attack()}，防御：{card_obj.get_defense()}
"""
        return ""

    def match_query(self, search_keyword, field):
        assert field in ("卡名", "卡码", "描述",)

        if field == "卡名":
            cursor = self.conn.execute(
                ("select texts.id, texts.name, datas.type from "
                 "texts, datas where name like ? and texts.id=datas.id"),
                (f"%{search_keyword}%",))
        elif field == "卡码":
            cursor = self.conn.execute(
                ("select texts.id, texts.name, datas.type from "
                 "texts, datas where texts.id=? and texts.id=datas.id"),
                (search_keyword,))
        elif field == "描述":
            cursor = self.conn.execute(
                ("select texts.id, texts.name, datas.type from "
                 "texts, datas where texts.desc like ? and texts.id=datas.id"),
                (f"%{search_keyword}%",))

        return list(cursor)

    def __del__(self):
        self.conn.close()
