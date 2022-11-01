from abc import ABC, abstractmethod


class Converter(ABC):
    """Abstract class for converting a file to a different file format."""

    def __init__(self, source_file, target_file):
        self.source_file = source_file
        self.target_file = target_file

    def read_source(self):
        """Read the source file."""
        source_file = open(self.source_file, "r+")
        return source_file.readlines()

    def write_target(self, lines):
        """Write the target file."""
        file = open(self.target_file, "w", encoding="utf8")
        for line in lines:
            print(line, file=file)

    def convert_file(self):
        """Convert the source file to a target file."""
        source_lines = self.read_source()
        lines = self.convert(source_lines)
        self.write_target(lines)

    @abstractmethod
    def convert(self, source_lines):
        """Convert the source file content to pseudo code."""
        pass


def get_converter():
    """Get the converter which set in the settings."""
    from config import settings

    converter = settings.get("pseudo.converter")
    match converter:
        case "sre":
            from brick.cmd.pseudo.converter.sre import SREConverter

            return SREConverter
        case "laqa":
            from brick.cmd.pseudo.converter.laqa import LAQAConverter

            return LAQAConverter
        case _:
            raise NotImplementedError(
                f"Converter {converter} is not implemented."
            )
