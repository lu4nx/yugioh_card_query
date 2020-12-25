class YDK(object):
    """.ydk 文件解析"""

    def __init__(self, ydk_file_path):
        self.ydk_file_path = ydk_file_path
        self.main_deck = []
        self.extra_deck = []
        self.side_deck = []
        self.load()

    def load(self):
        stat = None

        with open(self.ydk_file_path) as f:
            for line in f:
                if line.startswith("#main"):
                    stat = "main"
                    continue
                elif line.startswith("#extra"):
                    stat = "extra"
                    continue
                elif line.startswith("!side"):
                    stat = "side"
                    continue

                if stat == "main":
                    self.main_deck.append(line.strip())
                    continue
                elif stat == "extra":
                    self.extra_deck.append(line.strip())
                    continue
                elif stat == "side":
                    self.side_deck.append(line.strip())
                    continue

                continue

