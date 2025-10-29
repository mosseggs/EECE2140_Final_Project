# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 14:05:36 2025

@author: juani
"""
class TruthTable:
    """makes a truthtable"""

    def __init__(self) -> None:
        self._variables : list[str] = []
        self._table : list[dict[str, int]] = []
        self._answers : list[str] = []

    @property
    def variables(self) -> list[str]:
        return self._variables

    @property
    def answers(self) -> list[str]:
        return self._answers

    def parse(self, phrase : str) -> None:
        """Parses the string for the phrases."""
        # TODO: Needs work
        while(phrase.find("(") != -1):
            print(phrase)
            phrase = self.subPhrases(phrase)

        print(phrase)
        for char in phrase.split(" "):
            if char.lower() not in ["and", "or", "xor", "not", "nand", "nor", "xnor", ""]:
                self._variables.append(char)

    def subPhrases(self, phrase: str) -> str:
        """Parses the string for any sub-phrases using parenthesis"""
        start : int = 0
        subPhrase : str = ""
        for i in range(len(phrase)):
            if phrase[i] == "(":
                start += 1
            elif phrase[i] == ")" and start != 1:
                start -= 1
            elif phrase[i] == ")" and start == 1:
                sub_table : TruthTable = TruthTable()
                sub_table.parse(phrase[phrase.find("(") + 1: i])
                if(sub_table.variables != []):
                    print("---" + phrase)
                    print(self.variables)
                    print(sub_table.variables)
                    self._variables += sub_table.variables
                    print(self.variables)
                    print("---")
                subPhrase = phrase[:phrase.find("(")] + phrase[i + 1:]
                break
        return subPhrase





    def add_variables(self, count: int, start: int) -> None:
        """Helper method to add variables over 26"""
        for letter in range(count):
            if start > 0:
                self._variables.append(chr(start+65))
            self._variables.append(chr(letter + 65))

    def generate_table(self)-> None:
        """Generates a table"""
        total_rows = 2 ** len(self._variables)

        for i in range(total_rows):
            row = {}
            print(f"Entry {i + 1}:")
            for var in self._variables:
                row[var] = 0
            for j in range(len(self._variables)):
                k = len(self._variables) - j - 1
                print(f"{i}:{j}:{int(i/(2**j))}")
                if int(i / (2**j)) % 2 == 0:
                    row[list(self._variables)[k]] = 0
                else:
                    row[list(self._variables)[k]] = 1
            # TODO: make this get filled in automatically.
            while True:
                y_value = input("Enter output Y (0 or 1): ")
                if y_value in ['0', '1']:
                    row['Y'] = int(y_value)
                    break
                else:
                    print("Invalid input. Enter 0 or 1.")
            print()
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
table.parse("((AC AND B) AND C)")
table.generate_table()
table.display_table()
