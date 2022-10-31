import re


class Converter:
    CONVERSIONS = {
        "basic": {
            "for": "FOR",
            "=": "TO",
            "if": "IF",
            "==": "EQUALS",
            "while": "WHILE",
            "until": "UNTIL",
            "import": "IMPORT",
            "class": "DEFINE CLASS",
            "def": "DEFINE FUNCTION",
            "else:": "ELSE:",
            "elif": "ELSEIF",
            "except:": "EXCEPT:",
            "try:": "TRY:",
            "pass": "PASS",
            "in": "IN",
        },
        "prefix": {"=": "SET ", "#F": "CALL "},
        "advanced": {"print": "OUTPUT", "return": "RETURN", "input": "INPUT"},
    }

    def __init__(self, source_file, target_file):
        self.source_file = source_file
        self.target_file = target_file

    def read_source(self):
        source_file = open(self.source_file, "r+")
        return source_file.readlines()

    def convert(self):
        source_lines = self.read_source()
        for line in source_lines:
            line_index = source_lines.index(line)
            line = str(line)
            line = re.split(r"(\s+)", line)
            for key, value in self.CONVERSIONS["prefix"].items():
                if key in line:
                    if not str(line[0]) == "":
                        line[0] = value + line[0]
                    else:
                        line[2] = value + line[2]
            for key, value in self.CONVERSIONS["basic"].items():
                for word in line:
                    if key == str(word):
                        line[line.index(word)] = value
            for key, value in self.CONVERSIONS["advanced"].items():
                for word in line:
                    line[line.index(word)] = word.replace(key, value)
            for key, value in self.CONVERSIONS["prefix"].items():
                for word in line:
                    if word == key:
                        del line[line.index(word)]
            source_lines[line_index] = "".join(line)
        return source_lines

    def write_target(self, lines):
        file = open(self.target_file, "w", encoding="utf8")
        for line in lines:
            print(line, file=file)
