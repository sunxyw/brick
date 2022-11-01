import re

from brick.cmd.pseudo import Converter


class SREConverter(Converter):
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
        "advanced": {"print": "Print", "return": "RETURN", "input": "INPUT"},
    }

    def convert(self, source_lines):
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
