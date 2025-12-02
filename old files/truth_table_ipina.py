# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 14:05:36 2025

@author: juani and gabrielL
"""
class TruthTable:
    """makes a truthtable"""

    def __init__(self) -> None:
        self._variables : list[str] = []
        self._table : list[dict[str, int]] = []
        self._answers : list[bool] = []
        self._answers2 : list[bool] = []

    @property
    def variables(self) -> list[str]:
        return self._variables

    @property
    def answers(self) -> list[bool]:
        return self._answers

    def parse(self, phrase : str) -> None:
        """Parses the string for the phrases."""
        # TODO: Needs work
        while(phrase.find("(") != -1):
            phrase = self.sub_phrases(phrase)
        for char in range(len(phrase.split(" "))):
            splitted : list[str] = phrase.split(" ")
            offset : int = 1
            if (splitted[char].lower() not in ["and", "or", "xor", "not", "nand", "nor", "xnor", ""]
                and splitted[char] not in self.variables):
                self._variables.append(splitted[char])
                if self.answers == []:
                    self._answers = [False, True]
                else:
                    self._answers2 = [False, True]
                if splitted[char - 1].lower() == "not":
                    if self._answers2 == []:
                        self._answers = self.reverse(self._answers)
                    else:
                        self._answers2 = self.reverse(self._answers2)
                    offset = 2
                if (splitted[char - offset].lower() in ["and", "or", "xor", "nand", "nor", "xnor"]):
                    self._answers = self.get_answers(self._answers, splitted[char - offset], self._answers2)
                    self._answers2 = []

    def sub_phrases(self, phrase: str) -> str:
        """Parses the string for any sub-phrases using parenthesis"""
        start : int = 0
        sub_phrase : str = ""
        for i in range(len(phrase)):
            if phrase[i] == "(":
                start += 1
            elif phrase[i] == ")" and start != 1:
                start -= 1
            elif phrase[i] == ")" and start == 1:
                sub_table : TruthTable = TruthTable()
                sub_table.parse(phrase[phrase.find("(") + 1: i])
                if(sub_table.variables != []):
                    self._variables += sub_table.variables
                sub_phrase = phrase[:phrase.find("(")] + phrase[i + 1:]
                split : list[str] = sub_phrase.split(" ")
                if phrase[phrase.find("(") - 3:phrase.find("(")].lower() == "not":
                        sub_table._answers = sub_table.reverse(sub_table._answers)
                if self._answers == []:
                    self._answers = sub_table.answers
                else:
                    check : list[str] = ["and", "or", "xor", "nand", "nor", "xnor"]
                    common : list[str] = list(filter(lambda x: x in [s.lower() for s in split], check))
                    if common != []:
                        item : str = common[0]
                        lowersplit = [s.lower() for s in split]
                        self._answers = self.get_answers(self._answers, split[lowersplit.index(item)],sub_table.answers)

                break
        return sub_phrase

    def reverse(self, ans: list[bool]) -> list[bool]:
        """implements the not operator"""
        new_ans : list[bool] = []
        for i in ans:
            new_ans.append(not i)
        return new_ans

    def get_answers(self, ans1: list[bool], operator: str, ans2 : list[bool]) -> list[bool]:
        """Implements every operator that requires 2 inputs"""
        new_ans : list[bool] = []
        for i in ans1:
            for j in ans2:
                match(operator.lower()):
                    case "and" | "&&" | "&":
                        new_ans.append(i and j)
                    case "or" | "||" | "|":
                        new_ans.append(i or j)
                    case "xor" | "^" | "⊻":
                        new_ans.append(i != j)
                    case "nand":
                        new_ans.append(not (i and j))
                    case "nor":
                        new_ans.append(not (i or j))
                    case "xnor":
                        new_ans.append(i == j)
        return new_ans

    def get_variable_count(self) -> None:
        """Gets the amount of variables for manual insertion into the truth table"""
        count = -1
        while count <= 0:
            count = int(input("Enter number of variables: "))
        for i in range(int(count/26) + 1):
            if(count - 26 > 0):
                self.add_variables(26, i)
            else:
                self.add_variables(count, i)
            count -= 26
        print(f"{self.variables}")

    def add_variables(self, count: int, start: int) -> None:
        """Helper method to add variables over 26"""
        for letter in range(count):
            start2 : int = start
            string : str = ""
            while start2 > 0:
                start3 : int = start2 % 26
                if (start2 == 26):
                    start3 = 26
                string += chr(start2 % 26 + 64)
                start2 -= 26
            self._variables.append(string + chr(letter + 65))

    def generate_table(self)-> None:
        """Generates a table"""
        total_rows = 2 ** len(self._variables)

        for i in range(total_rows):
            row = {}
            for var in self._variables:
                row[var] = 0
            for j in range(len(self._variables)):
                k = len(self._variables) - j - 1
                if int(i / (2**j)) % 2 == 0:
                    row[list(self._variables)[k]] = 0
                else:
                    row[list(self._variables)[k]] = 1
            # TODO: make this get filled in automatically.
            if self.answers == [] and self.variables != []:
                print(f"Entry {i + 1}:")
                while True:
                    y_value = input("Enter output Y (0 or 1): ")
                    if y_value in ['0', '1']:
                        row['Y'] = int(y_value)
                        break
                    else:
                        print("Invalid input. Enter 0 or 1.")
                print()
            else:
                if self.answers[i]:
                    row['Y'] = 1
                else:
                    row['Y'] = 0
            self._table.append(row)

    def display_table(self)-> None:
        """Prints the table"""
        print("\nTruth Table:")
        print("-" * (len(self._variables) * 4 + 6))
        header = " ".join(self._variables) + " | Y"
        print(header)
        print("-" * (len(self._variables) * 4 + 6))
        for row in self._table:
            values : str = ""
            for var in self._variables:
                values += str(row[var]) + " " * len(var)
            print(f"{values}| {row['Y']}")
        print("-" * (len(self._variables) * 4 + 6))
table = TruthTable()
table.parse("(A AND B) AND NOT(D)")
# table.get_answers([False, True], "AND", [False, False, False, True])
# table.reverse([False, True])
# table.get_variable_count()
table.generate_table()
table.display_table()
