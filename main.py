#!/usr/bin/env python3
# author: lu4nx <www.shellcodes.org>

import re
import os
import sys
import json
from sqlite3 import DatabaseError, OperationalError

from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QPixmap, QDesktopServices, QColor, QFont
from PyQt5.QtWidgets import (
    QMenu,
    QDialog,
    QMainWindow,
    QApplication,
    QMessageBox,
    QListWidgetItem,
    QFileDialog,
)

from core.ydk import YDK
from core.word_study import WordStudy
from core.fl_card_list import ForbiddenLimitedCardList
from core.card_database import CardDatabase

from ui import Ui_MainWindow, Ui_settings, Ui_about, Ui_count, Ui_word_study


__VERSION__ = "0.5"
__OFFICIAL_WEBSITE__ = "https://github.com/1u4nx/yugioh_card_query"


class UserSetting(object):
    def __init__(self):
        self.user_config_file = f"{os.getenv('HOME')}/.ygo_card_query.conf"
        self.card_pictures_path = None
        self.card_database_path = None
        self.limit_card_path = None
        self.setting_flag = False

    def load(self):
        """加载用户配置信息"""
        if not os.path.exists(self.user_config_file):
            return

        # 不允许连接到其他文件，防止任意文件读取
        if os.path.islink(self.user_config_file):
            return

        with open(self.user_config_file, "r") as f:
            config_content = json.load(f)
            self.card_pictures_path = config_content["card_pictures_path"]
            self.card_database_path = config_content["card_database_path"]
            self.limit_card_path = config_content["limit_card_path"]

        self.setting_flag = True

    def write(self, card_pictures_path, card_database_path, limit_card_path):
        with open(self.user_config_file, "w") as f:
            f.write(json.dumps({
                "card_pictures_path": card_pictures_path,
                "card_database_path": card_database_path,
                "limit_card_path": limit_card_path
            }))

    def get_card_database_path(self):
        return self.card_database_path

    def get_card_pictures_path(self):
        return self.card_pictures_path

    def get_limit_card_path(self):
        return self.limit_card_path

    def is_setting(self):
        return self.setting_flag


CONF = UserSetting()
CONF.load()


class InputHistory(object):
    """单链表的历史记录保存"""

    def __init__(self):
        self.inputs = []

    def add(self, item):
        self.inputs.append(item)

    def back(self):
        try:
            return self.inputs.pop()
        except IndexError:
            return None


class CardItem(QListWidgetItem):
    def __init__(self, name, card_number):
        super(CardItem, self).__init__(name)
        self.card_number = card_number

    def get_card_name(self):
        # 替换掉名字前的“[怪]”、“[限1]”等标签
        return re.sub(r"\[.{1,3}\]", "", self.text())

    def get_number(self):
        return self.card_number


class CountUI(Ui_count):
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self.dialog)
        self.db = CardDatabase(CONF.get_card_database_path())

    def count_card(self):
        all_type = self.db.count_all_type()
        types_count = {
            "怪兽卡": {},
            "魔法卡": {},
            "陷阱卡": {}
        }

        for name, total in all_type:
            if name.startswith("怪兽"):
                if name == "怪兽":
                    name = "普通"
                name = name.replace("怪兽 ", "")
                types_count["怪兽卡"].setdefault(name, 0)
                types_count["怪兽卡"][name] += total
            elif name.startswith("魔法"):
                if name == "魔法":
                    name = "普通"
                name = name.replace("魔法 ", "")
                types_count["魔法卡"].setdefault(name, 0)
                types_count["魔法卡"][name] += total
            elif name.startswith("陷阱"):
                if name == "陷阱":
                    name = "普通"
                name = name.replace("陷阱 ", "")
                types_count["陷阱卡"].setdefault(name, 0)
                types_count["陷阱卡"][name] += total

        return types_count

    def pretty_types_count(self):
        count_result = self.count_card()
        card_total = 0

        ret = ""
        for type_name in count_result:
            ret += f"{type_name}：\n"
            for sub_type_name in count_result[type_name]:
                sub_type_total = count_result[type_name][sub_type_name]
                ret += f"        {sub_type_name}：{sub_type_total}\n"
                card_total += sub_type_total

        return f"总卡数：{card_total}\n\n{ret}"

    def show(self):
        self.count_info_text.setText(self.pretty_types_count())
        self.dialog.show()
        self.dialog.exec()


class WordStudyUI(Ui_word_study):
    def __init__(self, parent=None):
        self.dialog = QDialog(parent=parent)
        self.setupUi(self.dialog)
        self.word_study = WordStudy()
        self.next_button.clicked.connect(self.next_word)
        self.pre_button.clicked.connect(self.pre_word)

    def show(self):
        self.next_word()
        self.dialog.show()
        self.dialog.exec()

    def pre_word(self):
        word = self.word_study.get_pre_word()
        if word:
            self.japanese_text_edit.setPlainText(word[0])
            self.chinese_text_edit.setPlainText(word[1])

    def next_word(self):
        word = self.word_study.get_next_word()
        if word:
            self.japanese_text_edit.setPlainText(word[0])
            self.chinese_text_edit.setPlainText(word[1])


class SettingUI(Ui_settings):
    def __init__(self, parent=None):
        self.dialog = QDialog(parent=parent)
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 子窗口没关闭的情况下无法操作主窗口
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setupUi(self.dialog)
        self.save_setting_button.clicked.connect(self.save_setting)
        self.card_pictures_path_edit.setText(CONF.get_card_pictures_path())
        self.card_database_path_edit.setText(CONF.get_card_database_path())
        self.limit_card_file_path_edit.setText(CONF.get_limit_card_path())
        self.select_pic_dir_button.clicked.connect(self.select_pictures_dir)
        self.select_database_file_button.clicked.connect(
            self.select_database_file)
        self.select_limit_card_file_button.clicked.connect(
            self.select_limit_card_file)

    def show(self):
        self.dialog.show()
        self.dialog.exec()

    def select_pictures_dir(self):
        choose_pic_dir = QFileDialog.getExistingDirectory(self.dialog,
                                                          "选择图片目录",
                                                          "/")
        self.card_pictures_path_edit.setText(choose_pic_dir)

    def select_database_file(self):
        choose_file, _ = QFileDialog.getOpenFileName(self.dialog,
                                                     "选择数据库文件",
                                                     "/",
                                                     "(*.cdb);;All Files (*)")
        self.card_database_path_edit.setText(choose_file)

    def select_limit_card_file(self):
        choose_file, _ = QFileDialog.getOpenFileName(self.dialog,
                                                     "选择禁卡数据",
                                                     "/",
                                                     "(*.conf);;All Files (*)")
        self.limit_card_file_path_edit.setText(choose_file)

    def save_setting(self):
        card_pictures_path = self.card_pictures_path_edit.text()
        card_database_path = self.card_database_path_edit.text()
        limit_card_path = self.limit_card_file_path_edit.text()
        CONF.write(card_pictures_path, card_database_path, limit_card_path)
        QMessageBox.information(self.dialog, "提示", "保存成功，重启程序后生效",
                                QMessageBox.Ok)


class AboutUI(Ui_about):
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self.dialog)

    def show(self):
        self.dialog.show()
        self.dialog.exec()


class MainUI(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent=parent)
        self.setupUi(self)
        # 禁止改变窗口大小
        self.setFixedSize(self.width(), self.height())
        # 菜单选项响应注册
        self.setting_action.triggered.connect(lambda: SettingUI().show())
        self.word_study_action.triggered.connect(lambda: WordStudyUI().show())
        self.card_count_action.triggered.connect(lambda: CountUI().show())
        self.about_action.triggered.connect(lambda: AboutUI().show())
        self.official_website_action.triggered.connect(
            self.open_official_website
        )
        self.search_button.clicked.connect(self.do_search)
        self.load_ydk_action.triggered.connect(self.load_ydk)
        # 响应回车事件
        self.search_button.setShortcut(QtCore.Qt.Key_Return)
        self.set_card_picture_show()
        self.search_result_widget.itemSelectionChanged.connect(self.show_card)
        # 注册卡图的右键菜单
        self.card_picture.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.card_picture.customContextMenuRequested.connect(
            self.show_picture_menu
        )
        # 注册搜索结果的右键菜单
        self.search_result_widget.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu
        )
        self.search_result_widget.customContextMenuRequested.connect(
            self.show_search_result_menu
        )
        # 搜索历史
        self.history = InputHistory()
        self.history_button.clicked.connect(self.back_history)

        self.monster_checkBox.clicked.connect(lambda: self.active_opts("monster"))
        self.spell_checkBox.clicked.connect(lambda: self.active_opts("spell"))
        self.trap_checkBox.clicked.connect(lambda: self.active_opts("trap"))

        if not CONF.is_setting():
            self.please_setting()
            return

        try:
            self.card_database = CardDatabase(CONF.get_card_database_path())
        except OperationalError:
            QMessageBox.information(self, "提示",
                                    "数据库加载失败，请检查配置的路径是否失效", QMessageBox.Ok)
            return

        try:
            self.limit_card = ForbiddenLimitedCardList(CONF.get_limit_card_path())
        except ValueError:
            QMessageBox.information(self, "提示",
                                    "禁卡数据加载失败，请检查", QMessageBox.Ok)
            return

    def active_opts(self, opt_type):
        assert(opt_type in ("monster", "spell", "trap"))

        group_targets = {"monster": self.monster_checkBox,
                         "spell": self.spell_checkBox,
                         "trap": self.trap_checkBox}

        if opt_type == "monster":
            opts = (self.monster_normal_checkBox, self.monster_effect_checkBox,
                    self.monster_tuner_checkBox, self.monster_token_checkBox,
                    self.monster_dual_checkBox, self.monster_toon_checkBox,
                    self.monster_spirit_checkBox, self.monster_spsummon_checkBox,
                    self.monster_fusion_checkBox, self.monster_xyz_checkBox,
                    self.monster_synchro_checkBox, self.monster_pendulum_checkBox,
                    self.monster_link_checkBox, self.monster_ritual_checkBox,
                    self.attack_edit, self.defense_edit, self.level_edit,
                    self.link_num_edit, self.pendulum_scales_edit,
                    self.xyz_rank_edit)
        elif opt_type == "spell":
            opts = (self.spell_normal_checkBox, self.spell_continuous_checkBox,
                    self.spell_quickplay_checkBox, self.spell_field_checkBox,
                    self.spell_equip_checkBox, self.spell_ritual_checkBox)
        elif opt_type == "trap":
            opts = (self.trap_normal_checkBox, self.trap_continuous_checkBox,
                    self.trap_counter_checkBox)

        for opt in opts:
            if group_targets[opt_type].isChecked():
                opt.setEnabled(True)
            else:
                opt.setEnabled(False)

        return

    def open_official_website(self):
        QDesktopServices.openUrl(QtCore.QUrl(__OFFICIAL_WEBSITE__))

    def load_ydk(self):
        ydk_file, _ = QFileDialog.getOpenFileName(self,
                                                     "选择文件",
                                                     "/",
                                                     "(*.ydk);;All Files (*)")
        if not ydk_file:
            return

        ydk_obj = YDK(ydk_file)
        self.search_result_widget.clear()

        for deck_type, deck in ((f"\t主卡组（{len(ydk_obj.main_deck)}）", ydk_obj.main_deck),
                                (f"\t额外卡组（{len(ydk_obj.extra_deck)}）", ydk_obj.extra_deck),
                                (f"\t副卡组（{len(ydk_obj.side_deck)}）", ydk_obj.side_deck)):
            font = QFont()
            font.setPointSize(12)
            item4deck = QListWidgetItem()
            item4deck.setText(deck_type)
            item4deck.setForeground(QColor("blue"))
            item4deck.setFont(font)
            self.search_result_widget.addItem(item4deck)
            # self.search_result_widget.addItem(deck_type)

            for card_password in deck:
                card = self.card_database.query_password(card_password)

                if card is None:
                    self.search_result_widget.addItem(f"???{card_password}")
                    continue

                limit_count = self.limit_card.get_limit_number(card.get_number())
                item = self.format_list_item(card, limit_count)
                self.search_result_widget.addItem(item)

    def back_history(self):
        # 先要弹出一次当前的搜索关键字，才能取到上一次的搜索关键字，因此调用两次 back 方法
        self.history.back()
        search_keyword = self.history.back()

        if not search_keyword:
            return
        self.search_keyword_edit.lineEdit().setText(search_keyword)
        self.do_search()

    def show_picture_menu(self):
        menu = QMenu(self)
        copy_pic = menu.addAction("复制卡图")
        save_pic = menu.addAction("卡图另存为...")
        copy_pic.triggered.connect(self.copy_card_pic2clipboard)
        save_pic.triggered.connect(self.save_picture)
        menu.exec(QCursor.pos())

    def show_search_result_menu(self):
        def open_url(url):
            # 可以不用 URL 转码，浏览器会自动转
            QDesktopServices.openUrl(QtCore.QUrl(url))

        menu = QMenu(self)
        search_taobao = menu.addAction("淘宝搜卡")
        search_ourocg = menu.addAction("ourocg.cn 查卡")
        select = self.search_result_widget.selectedItems()

        if not select:
            return

        item = select[0]
        search_taobao.triggered.connect(lambda: open_url(f"https://s.taobao.com/search?q={item.get_card_name()}"))
        search_ourocg.triggered.connect(lambda: open_url(f"https://www.ourocg.cn/search/{item.get_number()}"))
        menu.exec(QCursor.pos())

    def save_picture(self):
        choose_file, _ = QFileDialog.getSaveFileName(self, "另存为",
                                                     "*.png", "(*.png)")
        self.card_picture.pixmap().save(choose_file, "png")

    def copy_card_pic2clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.card_picture.pixmap())

    def please_setting(self):
        QMessageBox.information(self, "提示", "请先配置数据：工具 > 设置", QMessageBox.Ok)

    def set_card_picture_show(self, path=None):
        app_base_dir = os.path.dirname(os.path.realpath(__file__))
        defalut_pic = f"{app_base_dir}/images/card_default_picture.png"

        if (path is None) or (not os.path.exists(path)) or (os.path.islink(path)):
            card_pic_file = QPixmap(defalut_pic)
        else:
            card_pic_file = QPixmap(path)

        # 调整图片大小，缩放到和 label 一样大
        self.card_picture.setPixmap(card_pic_file.scaled(
            self.card_picture.width(), self.card_picture.height())
        )

    def do_search(self):
        if not CONF.is_setting():
            self.please_setting()
            return

        self.search_result_widget.clear()
        search_type = self.search_type.currentText()
        search_keyword = self.search_keyword_edit.lineEdit().text()
        self.history.add(search_keyword)

        if search_keyword == "":
            QMessageBox.information(self, "提示", "请输入关键字", QMessageBox.Ok)
            return

        # 下拉列表保存搜索记录
        if self.search_keyword_edit.findText(search_keyword) == -1:
            self.search_keyword_edit.addItem(search_keyword)

        try:
            attack = self.attack_edit.text() and int(self.attack_edit.text())
            defense = self.defense_edit.text() and int(self.defense_edit.text())
            level = self.level_edit.text() and int(self.level_edit.text())
            link_num = self.link_num_edit.text() and int(self.link_num_edit.text())
            pendulum_scales = self.pendulum_scales_edit.text() and int(self.pendulum_scales_edit.text())
            xyz_rank = self.xyz_rank_edit.text() and int(self.xyz_rank_edit.text())
        except ValueError:
            QMessageBox.information(self, "警告", "ATT、DEF、等级、LINK 值、刻度、阶级必须是数字", QMessageBox.Ok)
            return

        try:
            search_result = self.card_database.match_query(search_keyword,
                                                           search_type,
                                                           monster=self.monster_checkBox.isChecked(),
                                                           spell=self.spell_checkBox.isChecked(),
                                                           trap=self.trap_checkBox.isChecked(),
                                                           monster_normal=self.monster_normal_checkBox.isChecked(),
                                                           monster_effect=self.monster_effect_checkBox.isChecked(),
                                                           monster_tuner=self.monster_tuner_checkBox.isChecked(),
                                                           monster_token=self.monster_token_checkBox.isChecked(),
                                                           monster_dual=self.monster_dual_checkBox.isChecked(),
                                                           monster_toon=self.monster_toon_checkBox.isChecked(),
                                                           monster_spirit=self.monster_spirit_checkBox.isChecked(),
                                                           monster_spsummon=self.monster_spsummon_checkBox.isChecked(),
                                                           monster_fusion=self.monster_fusion_checkBox.isChecked(),
                                                           monster_xyz=self.monster_xyz_checkBox.isChecked(),
                                                           monster_synchro=self.monster_synchro_checkBox.isChecked(),
                                                           monster_pendulum=self.monster_pendulum_checkBox.isChecked(),
                                                           monster_link=self.monster_link_checkBox.isChecked(),
                                                           monster_ritual=self.monster_ritual_checkBox.isChecked(),
                                                           spell_normal=self.spell_normal_checkBox.isChecked(),
                                                           spell_continuous=self.spell_continuous_checkBox.isChecked(),
                                                           spell_quickplay=self.spell_quickplay_checkBox.isChecked(),
                                                           spell_field=self.spell_field_checkBox.isChecked(),
                                                           spell_equip=self.spell_equip_checkBox.isChecked(),
                                                           spell_ritual=self.spell_ritual_checkBox.isChecked(),
                                                           trap_normal=self.trap_normal_checkBox.isChecked(),
                                                           trap_continuous=self.trap_continuous_checkBox.isChecked(),
                                                           trap_counter=self.trap_counter_checkBox.isChecked(),
                                                           attack=attack,
                                                           defense=defense,
                                                           level=level,
                                                           link_num=link_num,
                                                           pendulum_scales=pendulum_scales,
                                                           xyz_rank=xyz_rank)
        except DatabaseError:
            QMessageBox.information(self, "警告", "数据库文件格式有误，请重新设置",
                                    QMessageBox.Ok)
            return

        if not search_result:
            QMessageBox.information(self, "提示", "查询结果为空", QMessageBox.Ok)
            return

        result_total = 0
        for i in search_result:
            result_total += 1
            limit_count = self.limit_card.get_limit_number(i.get_number())
            item = self.format_list_item(i, limit_count)
            self.search_result_widget.addItem(item)

        self.total_label.setText(f"共检索到 {result_total} 条记录")

    def format_list_item(self, card, limit_count):
        if limit_count is None:
            item = CardItem(f"[{card.get_short_type()}]{card.get_name()}",
                            card_number=(card.get_number()))
        elif limit_count == 0:
            item = CardItem(f"[{card.get_short_type()}][禁]{card.get_name()}",
                            card_number=(card.get_number()))
            item.setForeground(QColor("red"))
        else:
            item = CardItem(
                f"[{card.get_short_type()}][限{limit_count}]{card.get_name()}",
                card_number=(card.get_number()))
            item.setForeground(QColor("red"))

        return item

    def show_card(self):
        items = self.search_result_widget.selectedItems()
        # 列表没支持多选，因此这里循环实际暂时无意义，和取第一个元素是一样的
        for item in items:
            if item is None:
                continue

            if not isinstance(item, CardItem):
                continue

            card_number = item.get_number()
            picture_path = f"{CONF.get_card_pictures_path()}/{card_number}.jpg"
            self.set_card_picture_show(picture_path)
            card_info = self.card_database.get_card_info(card_number)
            self.card_info.setText(card_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = MainUI()
    main_ui.show()
    main_ui.setWindowTitle(f"{main_ui.windowTitle()} v{__VERSION__}")
    sys.exit(app.exec_())
