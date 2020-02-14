from unittest import TestCase
from core.card_database import (
    get_card_type,
    get_card_attribute,
    get_card_short_type
)


class TestCardType(TestCase):
    def test_normal_monster(self):
        """测试普通怪兽"""
        self.assertEqual(get_card_type(0x11),
                         "怪兽")

    def test_link_monster(self):
        """测试连接怪兽"""
        self.assertEqual(get_card_type(0x4000021),
                         "怪兽 连接")

    def test_fusion_monster(self):
        """测试融合怪兽"""
        self.assertEqual(get_card_type(0x41),
                         "怪兽 融合")

    def test_is_pendulum_monster(self):
        """测试灵摆怪兽"""
        self.assertEqual(get_card_type(0x1000021),
                         "怪兽 灵摆")

    def test_effect_monster(self):
        """测试效果怪兽"""
        self.assertEqual(get_card_type(0x2000021),
                         "怪兽 效果")

    def test_normal_spell(self):
        """测试普通魔法卡"""
        self.assertEqual(get_card_type(0x2),
                         "魔法")

    def test_equip_spell(self):
        """测试装备魔法卡"""
        self.assertEqual(get_card_type(0x40002),
                         "魔法 装备")

    def test_quick_play_spell(self):
        """测试速攻魔法卡"""
        self.assertEqual(get_card_type(0x10002),
                         "魔法 速攻")

    def test_continuous_spell(self):
        """测试永久魔法卡"""
        self.assertEqual(get_card_type(0x20002),
                         "魔法 永久")

    def test_field_spell(self):
        """测试场地魔法卡"""
        self.assertEqual(get_card_type(0x80002),
                         "魔法 场地")

    def test_normal_trap(self):
        """测试普通陷阱卡"""
        self.assertEqual(get_card_type(0x4),
                         "陷阱")

    def test_continuous_trap(self):
        """测试永久陷阱卡"""
        self.assertEqual(get_card_type(0x20004),
                         "陷阱 永久")


class TestCardAttribute(TestCase):
    """测试卡片属性"""

    def test_get_attribute(self):
        self.assertEqual(get_card_attribute(0x1), "地")
        self.assertEqual(get_card_attribute(0x2), "水")
        self.assertEqual(get_card_attribute(0x4), "炎")
        self.assertEqual(get_card_attribute(0x8), "风")
        self.assertEqual(get_card_attribute(0x10), "光")
        self.assertEqual(get_card_attribute(0x20), "暗")
        self.assertEqual(get_card_attribute(0x40), "神")


class TestCardTypeShortName(TestCase):
    """测试卡片类型短名"""

    def test_short_name(self):
        self.assertEqual(get_card_short_type(0x4000021), "怪")
        self.assertEqual(get_card_short_type(0x40002), "魔")
        self.assertEqual(get_card_short_type(0x20004), "陷")