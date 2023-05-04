# author: lu4nx <www.shellcodes.org>

"""结构定义参考 ygopro 代码：script/constant.lua"""

import sqlite3


def get_monster_race(race_code):
    return {
        0x1ffffff: "全种族",
        0x1: "战士",
        0x2: "魔法师",
        0x4: "天使",
        0x8: "恶魔",
        0x10: "不死",
        0x20: "机械",
        0x40: "水",
        0x80: "炎",
        0x100: "岩石",
        0x200: "鸟兽",
        0x400: "植物",
        0x800: "昆虫",
        0x1000: "雷",
        0x2000: "龙",
        0x4000: "兽",
        0x8000: "兽战士",
        0x10000: "恐龙",
        0x20000: "鱼",
        0x40000: "海龙",
        0x80000: "爬虫类",
        0x100000: "念动力",
        0x200000: "幻神兽",
        0x400000: "创造神",
        0x800000: "幻龙",
        0x1000000: "电子界",
    }.get(race_code, None)


def get_card_type(type_code):
    """判断卡片类型"""
    card_type_codes_map = {
        0x1: {
            "name": "怪兽",
            "sub_type": {
                0x4000000: "连接",
                0x2000000: "特殊召唤",
                0x1000000: "灵摆",
                0x800000: "超量",
                0x400000: "卡通",
                0x2000: "同调",
                0x1000: "调整",
                0x4000: "衍生物",
                0x800: "二重",
                0x200: "灵魂",
                0x80: "仪式",
                0x40: "融合",
                0x20: "效果",
                0x10: "通常",
            }
        },
        0x2: {
            "name": "魔法",
            "sub_type": {
                0x80000: "场地",
                0x40000: "装备",
                0x20000: "永久",
                0x10000: "速攻",
                0x80: "仪式",
            }
        },
        0x4: {
            "name": "陷阱",
            "sub_type": {
                0x100000: "反击",
                0x20000: "永久",
            }
        }
    }

    type_attributes = []
    type_choose = None

    for code in card_type_codes_map:
        if main_type := (type_code & code):
            name = card_type_codes_map.get(main_type)["name"]
            type_attributes.append(name)
            type_choose = card_type_codes_map[code]["sub_type"]
            break

    assert type_choose is not None

    for code in type_choose:
        if (type_code & code) == code:
            type_attributes.append(type_choose[code])

    return "/".join(type_attributes)


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
    elif card_type.find("魔法") > -1:
        return "魔"
    elif card_type.find("陷阱") > -1:
        return "陷"

    raise TypeError("Card type error")


class Card(object):
    def __init__(self, **argv):
        self.number = argv.get("number")
        self.name = argv.get("name")
        self.type = argv.get("card_type")
        self.race = argv.get("race")
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

    def get_short_type(self):
        return get_card_short_type(self.type)

    def get_attribute(self):
        card_attribute = get_card_attribute(self.attribute)
        if card_attribute is None:
            return "?"
        return card_attribute

    def get_race(self):
        if self.is_monster():
            race = get_monster_race(self.race)
            if race is None:
                return "?"
            return race

    def get_defense(self):
        # 没有防御力的，数据库保存的值为 -2
        if self.defense == -2:
            return "?"
        # 连接怪兽没有防御力
        elif self.is_link_monster():
            return "?"
        return self.defense

    def get_attack(self):
        # 没有攻击力的，数据库保存的值为 -2
        if self.attack == -2:
            return "?"
        return self.attack

    def get_level(self):
        # 连接怪兽没有等级，而数据库中的等级值是连接数
        if self.is_link_monster():
            return None
        elif self.is_pendulum_monster():
            # 灵摆怪兽的 level 字段中，只有低两位保存的等级
            return self.level & 0xff

        return self.level

    def get_link_number(self):
        """返回连接怪兽的连接数"""
        if self.is_link_monster():
            return self.level
        return None

    def get_xyz_rank(self):
        """返回超量怪兽的阶级"""
        if self.is_xyz_monster():
            if self.is_pendulum_monster():
                return self.level & 0xff
            else:
                return self.level

        return None

    def get_desc(self):
        return self.desc

    def is_monster(self):
        return self.get_type().startswith("怪兽")

    def is_link_monster(self):
        return self.is_monster() and self.get_type().find("连接") > -1

    def is_ritual_monster(self):
        return self.is_monster() and self.get_type().find("仪式") > -1

    def is_pendulum_monster(self):
        return self.is_monster() and self.get_type().find("灵摆") > -1

    def is_xyz_monster(self):
        return self.is_monster() and self.get_type().find("超量") > -1

    def is_synchro_monster(self):
        return self.is_monster() and self.get_type().find("同调") > -1

    def is_spell(self):
        return self.get_type().startswith("魔法")

    def is_trap(self):
        return self.get_type().startswith("陷阱")


class CardDatabase(object):
    """完整的卡片数据库"""

    def __init__(self, card_db_path,):
        self.card_db_path = card_db_path
        self.connect = sqlite3.connect(self.card_db_path)
        self.conn = self.connect.cursor()

    def count_all_type(self):
        sql = "select type, count(1) from datas group by type"
        cursor = self.conn.execute(sql)
        return [(get_card_type(i[0]), i[1],)
                for i in list(cursor)]

    def query_for_password(self, card_password):
        cursor = self.conn.execute((
            "select texts.id, texts.name, texts.desc,"
            "datas.type, datas.attribute, datas.level,"
            "datas.atk, datas.def, datas.race from texts, datas "
            "where texts.id=? "
            "and texts.id = datas.id"), (card_password,))

        if (item := cursor.fetchone()) is None:
            return

        return Card(number=item[0],
                    name=item[1],
                    desc=item[2],
                    card_type=item[3],
                    attribute=item[4],
                    level=item[5],
                    attack=item[6],
                    defense=item[7],
                    race=item[8])

    def get_card_info(self, card_number):
        card = self.query_for_password(card_number)
        monster_info = self.monster_info_desc(card)
        return f"""{card.get_name()}（{card.get_number()}）

【{card.get_type()}】
{monster_info}
{card.get_desc()}
"""

    def monster_info_desc(self, card_obj):
        if not card_obj.is_monster():
            return ""

        level_field = "等级"
        level_field_value = card_obj.get_level()

        # LINK 怪兽和超量怪兽是没有等级的
        if card_obj.is_link_monster():
            level_field = "LINK"
            level_field_value = card_obj.get_link_number()
        elif card_obj.is_xyz_monster():
            level_field = "阶级"
            level_field_value = card_obj.get_xyz_rank()

        return f"""
{level_field}：{level_field_value}，{card_obj.get_race()}族，属性：{card_obj.get_attribute()}

攻击：{card_obj.get_attack()}，防御：{card_obj.get_defense()}
"""

    def add_query_where_sql(self, **options):
        where_spell = []
        where_monster = []
        where_monster_value = []
        where_trap = []
        where_monster_expr = "(type & 0x1) "
        where_spell_expr = "(type & 0x2) "
        where_trap_expr = "(type & 0x4) "
        sql = []

        # 怪兽选项
        options.get("monster_normal") and where_monster.append("(type & 0x10)")
        options.get("monster_effect") and where_monster.append("(type & 0x20)")
        options.get("monster_tuner") and where_monster.append("(type & 0x1000)")
        options.get("monster_token") and where_monster.append("(type & 0x4000)")
        options.get("monster_dual") and where_monster.append("(type & 0x800)")
        options.get("monster_toon") and where_monster.append("(type & 0x400000)")
        options.get("monster_spirit") and where_monster.append("(type & 0x200)")
        options.get("monster_spsummon") and where_monster.append("(type & 0x2000000)")
        options.get("monster_fusion") and where_monster.append("(type & 0x40)")
        options.get("monster_xyz") and where_monster.append("(type & 0x800000)")
        options.get("monster_synchro") and where_monster.append("(type & 0x2000)")
        options.get("monster_pendulum") and where_monster.append("(type & 0x1000000)")
        options.get("monster_link") and where_monster.append("(type & 0x4000000)")
        options.get("monster_ritual") and where_monster.append("(type & 0x80)")
        options.get("attack") and where_monster_value.append(f"atk={int(options.get('attack'))}")
        options.get("defense") and where_monster_value.append(f"def={int(options.get('defense'))}")
        options.get("level") and where_monster_value.append(f"level={int(options.get('level'))}")
        options.get("link_num") and where_monster_value.append(f"level={int(options.get('link_num'))} and (type & 0x4000000)")

        if options.get("pendulum_scales"):
            # level 字段的高 2 位是保存的灵摆刻度，因此先将等级左移 24 位，再与 level 字段的高 2 位做位运算
            # 灵摆最大刻度是 13
            scale = hex(int(options.get("pendulum_scales")) << 24)
            where_monster_value.append(f"((level & 0xf000000)={scale}) and (type & 0x1000000)")

        options.get("xyz_rank") and where_monster_value.append(f"level={int(options.get('xyz_rank'))} and (type & 0x800000)")

        # 魔法卡选项
        options.get("spell_normal") and where_spell.append("type=0x2")
        options.get("spell_continuous") and where_spell.append("(type & 0x20000)")
        options.get("spell_quickplay") and where_spell.append("(type & 0x10000)")
        options.get("spell_field") and where_spell.append("(type & 0x80000)")
        options.get("spell_equip") and where_spell.append("(type & 0x40000)")
        options.get("spell_ritual") and where_spell.append("(type & 0x80)")

        # 陷阱卡选项
        options.get("trap_normal") and where_trap.append("type=0x4")
        options.get("trap_continuous") and where_trap.append("(type & 0x20000)")
        options.get("trap_counter") and where_trap.append("(type & 0x100000)")

        monster_sub_sql = " or ".join(where_monster)
        monster_value_sub_sql = " and ".join(where_monster_value)
        spell_sub_sql = " or ".join(where_spell)
        trap_sub_sql = " or ".join(where_trap)

        if options.get("monster"):
            if monster_sub_sql:
                where_monster_expr = f"({where_monster_expr} and ({monster_sub_sql}))"
            if monster_value_sub_sql:
                where_monster_expr = f"({where_monster_expr} and ({monster_value_sub_sql}))"

            sql.append(where_monster_expr)

        if options.get("spell"):
            if spell_sub_sql:
                where_spell_expr = f"({where_spell_expr} and ({spell_sub_sql}))"

            sql.append(where_spell_expr)

        if options.get("trap"):
            if trap_sub_sql:
                where_trap_expr = f"({where_trap_expr} and ({trap_sub_sql}))"

            sql.append(where_trap_expr)

        return " or ".join(sql)

    def search(self, search_keyword, field, **options):
        assert field in ("卡名/卡密", "描述文本",)

        wheres = self.add_query_where_sql(**options)

        if field == "卡名/卡密":
            sql = ("select texts.id, texts.name, datas.type, datas.race, datas.attribute,"
                   "datas.atk, datas.def, datas.level, texts.desc from texts, datas "
                   "where texts.id=datas.id and (name like ? or texts.id=?)")
            query_value = (f"%{search_keyword}%", search_keyword)
        elif field == "描述文本":
            sql = ("select texts.id, texts.name, datas.type, datas.race, datas.attribute,"
                   "datas.atk, datas.def, datas.level, texts.desc from texts, datas "
                   "where texts.id=datas.id and texts.desc like ?")
            query_value = (f"%{search_keyword}%",)

        if wheres:
            sql = f"{sql} and ({wheres})"

        print(f"execute SQL: {sql}")
        for _ in self.conn.execute(sql, query_value):
            yield Card(number=_[0],
                       name=_[1],
                       card_type=_[2],
                       race=_[3],
                       attribute=_[4],
                       attack=_[5],
                       defense=_[6],
                       level=_[7],
                       desc=_[8])

    def __del__(self):
        self.conn.close()
