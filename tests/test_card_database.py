from unittest import TestCase
from core.card_database import CardBase


class TestCardBase(TestCase):
    def setUp(self) -> None:
        self.base = CardBase()

    def test_normal_monster(self):
        self.assertEqual(self.base.get_card_type(0x11),
                         "怪兽")

    def test_link_monster(self):
        self.assertEqual(self.base.get_card_type(0x4000021),
                         "怪兽 连接 效果")

    def test_fusion_monster(self):
        self.assertEqual(self.base.get_card_type(0x41),
                         "怪兽 融合")

    def test_is_pendulum_monster(self):
        self.assertEqual(self.base.get_card_type(0x1000021),
                         "怪兽 灵摆 效果")

    def test_is_ritual_monster(self):
        self.assertEqual(self.base.get_card_type(0x81),
                         "怪兽 仪式")

    def test_is_xyz_monster(self):
        self.assertEqual(self.base.get_card_type(0x800021),
                         "怪兽 超量 效果")

    def test_is_synchro_monster(self):
        self.assertEqual(self.base.get_card_type(0x2021),
                         "怪兽 同调 效果")

    def test_effect_monster(self):
        self.assertEqual(self.base.get_card_type(0x2000021),
                         "怪兽 效果")

    def test_normal_spell(self):
        self.assertEqual(self.base.get_card_type(0x2),
                         "魔法")

    def test_equip_spell(self):
        self.assertEqual(self.base.get_card_type(0x40002),
                         "魔法 装备")

    def test_quick_play_spell(self):
        self.assertEqual(self.base.get_card_type(0x10002),
                         "魔法 速攻")

    def test_ritual_spell(self):
        self.assertEqual(self.base.get_card_type(0x82),
                         "魔法 仪式")

    def test_continuous_spell(self):
        self.assertEqual(self.base.get_card_type(0x20002),
                         "魔法 永久")

    def test_field_spell(self):
        self.assertEqual(self.base.get_card_type(0x80002),
                         "魔法 场地")

    def test_normal_trap(self):
        self.assertEqual(self.base.get_card_type(0x4),
                         "陷阱")

    def test_continuous_trap(self):
        self.assertEqual(self.base.get_card_type(0x20004),
                         "陷阱 永久")

    def test_counter_trap(self):
        self.assertEqual(self.base.get_card_type(0x100004),
                         "陷阱 反击")

    def test_get_attribute(self):
        self.assertEqual(self.base.get_card_attribute(0x1), "地")
        self.assertEqual(self.base.get_card_attribute(0x2), "水")
        self.assertEqual(self.base.get_card_attribute(0x4), "炎")
        self.assertEqual(self.base.get_card_attribute(0x8), "风")
        self.assertEqual(self.base.get_card_attribute(0x10), "光")
        self.assertEqual(self.base.get_card_attribute(0x20), "暗")
        self.assertEqual(self.base.get_card_attribute(0x40), "神")

    def test_short_name(self):
        self.assertEqual(self.base.get_card_short_type(0x4000021), "怪")
        self.assertEqual(self.base.get_card_short_type(0x40002), "魔")
        self.assertEqual(self.base.get_card_short_type(0x20004), "陷")

    def test_monster_race(self):
        self.assertIsNone(self.base.get_monster_race(0))
        self.assertEqual(self.base.get_monster_race(0x2000), "龙")
        self.assertEqual(self.base.get_monster_race(0x2), "魔法师")
