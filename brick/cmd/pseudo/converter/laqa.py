from brick.cmd.pseudo import Converter


class LAQAConverter(Converter):
    def remove_line_breaks(self, source_lines):
        """Remove line breaks from the source file."""
        for line in source_lines:
            line_index = source_lines.index(line)
            if line and line[-1] == "\n":
                source_lines[line_index] = line[:-1]
        return source_lines

    def remove_blank_lines(self, source_lines):
        """Remove blank lines from the source file."""
        for line in source_lines:
            line_index = source_lines.index(line)
            if line == "" or line == "\n":
                del source_lines[line_index]
        return source_lines

    def remove_comments(self, source_lines):
        """Remove comments from the source file."""
        for line in source_lines:
            line_index = source_lines.index(line)
            if "#" in line:
                del source_lines[line_index]
        return source_lines

    def replace_keywords(
        self, source_lines, keywords, char_check=True, remove_end_char=False
    ):
        """Replace keywords in the source file."""
        useful_lines = []
        for count in range(len(source_lines)):
            for i in range(len(keywords)):
                # Check if the keyword is in the line
                found = source_lines[count].find(keywords[i][0])
                if found != -1:
                    working_line = source_lines[count]
                    if (
                        found > 0
                        and len(source_lines[count])
                        > found + len(keywords[i][0])
                        and char_check
                    ):
                        if count == 14:
                            pass
                        previous_char = working_line[found - 1]
                        next_char = working_line[found + len(keywords[i][0])]
                        if previous_char in [
                            "(",
                            " ",
                            '"',
                            ".",
                        ] and next_char in ["(", " ", '"', "."]:
                            first_bit = working_line[:found]
                            second_bit = working_line[
                                found + len(keywords[i][0]) :
                            ]
                            replaced_line = (
                                first_bit + keywords[i][1] + second_bit
                            )
                            source_lines[count] = replaced_line
                    else:
                        first_bit = working_line[:found]
                        second_bit = working_line[
                            found + len(keywords[i][0]) :
                        ]
                        replaced_line = first_bit + keywords[i][1] + second_bit
                        if remove_end_char:
                            replaced_line = self.remove_end_bit(
                                replaced_line, keywords[i][2]
                            )
                        source_lines[count] = replaced_line

        return source_lines

    def trace_indentations(self, source_lines):
        """Trace indentations in the source file to find where structures start and end."""
        search_for = [
            ["if", "ENDIF", [], [], False],
            ["def", "ENDFUNCTION", [], [], True],
            ["class", "ENDCLASS", [], [], True],
            ["while", "ENDWHILE", [], [], False],
            ["for", "ENDFOR", [], [], False],
        ]
        for count in range(len(source_lines)):
            for i in range(len(search_for)):
                current_keyword = search_for[i][0]
                # Check if the keyword is in the line
                found = source_lines[count].find(current_keyword)

                if found != -1:
                    # Define how many characters it is indented
                    distance = found
                    line_finished = False
                    for j in range(count + 1, len(source_lines)):
                        flag = False

                        for k in range(distance + 1):
                            if distance == 0:
                                pass

                            try:
                                if source_lines[j][k] != " ":
                                    if (
                                        source_lines[j][
                                            distance : distance + 4
                                        ]
                                        == "else"
                                    ):
                                        flag = False
                                    elif (
                                        source_lines[j][
                                            distance : distance + 1
                                        ]
                                        == "#"
                                    ):
                                        flag = False
                                    elif (
                                        source_lines[j][
                                            distance : distance + 3
                                        ]
                                        == "~~~"
                                    ):
                                        flag = False
                                    else:
                                        flag = True
                            except:
                                pass

                        if flag:
                            if not line_finished:
                                search_for[i][2].append(j)
                                search_for[i][3].append(distance)
                                line_finished = True
                            break

        return search_for

    def rebuild_list(self, source_lines, search_for, to_remove=None):
        """Rebuild the source lines list, searching for search_for keywords, and removing to_remove lines."""
        if to_remove is None:
            to_remove = []

        refreshed_lines = []
        for i in range(len(source_lines)):
            for count in range(len(search_for)):
                if i in search_for[count][2]:
                    for j in range(len(search_for[count][2])):
                        if search_for[count][2][j] == i:
                            parter_line = j
                            indended = ""
                            for k in range(search_for[count][3][parter_line]):
                                indended += " "
                            refreshed_lines.append(
                                indended + search_for[count][1]
                            )
                            if search_for[count][4]:
                                refreshed_lines.append("")
            if i not in to_remove:
                refreshed_lines.append(source_lines[i])

        return refreshed_lines

    def remove_keyword_lines(self, source_lines, keywords):
        """Remove lines containing keywords from the source file."""
        to_remove = []
        for count in range(len(source_lines)):
            for i in range(len(keywords)):
                # Check if the keyword is in the line
                found = source_lines[count].find(keywords[i])
                if found != -1:
                    to_remove.append(count)
        return to_remove

    def convert_str_to_list(self, source_lines):
        """Convert the source file to a list."""
        source_lines = source_lines.splitlines()
        return source_lines

    def convert_list_to_str(self, source_lines):
        """Convert the source file to a string."""
        source_lines = "\n".join(source_lines)
        return source_lines

    def remove_end_bit(self, line, to_remove):
        """Remove characters at the end of a line."""
        for i in range(len(to_remove)):
            if line[-1] == to_remove[i]:
                line = line[:-1]
        return line

    def convert(self, source_lines):
        source_lines = self.read_source()
        source_lines = self.remove_line_breaks(source_lines)
        source_lines = self.remove_line_breaks(source_lines)
        source_lines = self.remove_comments(source_lines)

        keywords = [["elif", "~~~"]]

        for i in range(0, 6):
            source_lines = self.replace_keywords(source_lines, keywords)

        search_for = self.trace_indentations(source_lines)

        source_lines = self.rebuild_list(source_lines, search_for)
        source_lines = self.remove_comments(source_lines)

        for x in range(0, 10):
            source_lines = self.replace_keywords(
                source_lines,
                [
                    ["def", "FUNCTION"],
                    ["print", "OUTPUT"],
                    ["self.", " "],
                    ["return", "RETURN"],
                    ["else:", "ELSE:"],
                    ["==", "|"],
                    ["if", "IF"],
                    ["or", "OR"],
                    ["and", "AND"],
                    ["and", "AND"],
                    ["class", "CLASS"],
                ],
            )
        for x in range(0, 5):
            source_lines = self.replace_keywords(
                source_lines,
                [
                    ["self.", " "],
                ],
                False,
            )
        for x in range(0, 10):
            source_lines = self.replace_keywords(
                source_lines, [["=", "<-"], ["~~~", "ELSEIF"]]
            )
        for x in range(0, 10):
            source_lines = self.replace_keywords(
                source_lines,
                [
                    ["|", "="],
                ],
            )

        source_lines = self.replace_keywords(
            source_lines, [["OUTPUT(", "OUTPUT ", ")"]], False, True
        )
        source_lines = self.replace_keywords(source_lines, [["<- ?", "= ?"]])
        source_lines = self.replace_keywords(source_lines, [["<- ?", "= ?"]])

        source_lines = self.remove_blank_lines(source_lines)

        return source_lines
