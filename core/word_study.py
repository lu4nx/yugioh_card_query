class WordStudy(object):
    def __init__(self):
        self.words = [
            ("この", "这个"),
            ("カード", "卡片"),
            ("自分", "自己"),
            ("相手", "对手"),
            ("手札", "手牌"),
            ("モンスター", "怪兽"),
            ("リバース", "反转"),
            ("効果", "效果"),
            ("発動できる", "可以发动。指的是选发效果。"),
            ("発動する", "发动。指的是必发效果。"),
            ("メインフェイズ", "主要阶段"),
            ("各", "每。例如：各カード（每张卡）"),
            ("罠", "陷阱")
        ]
        self.cur = -1

    def get_next_word(self):
        if self.cur + 1 >= len(self.words):
            self.cur = 0
            return self.words[self.cur]

        self.cur += 1
        return self.words[self.cur]

    def get_pre_word(self):
        if self.cur - 1 <= 0:
            self.cur = 0
            return self.words[self.cur]

        self.cur -= 1
        return self.words[self.cur]
