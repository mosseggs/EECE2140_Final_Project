# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 14:05:36 2025

@author: juani
"""
class TruthTable:
    """makes a truthtable"""

    def __init__(self) -> None:
        self.variables : list[str] = []
        self.table : list[dict[str, int]] = []

    def parse(self, phrase : str) -> None:
        """Parses the string for the phrases."""
        # TODO: Needs work
        for char in phrase.split(" "):
            if char.lower() not in ["and", "or", "xor", "not", "nand", "nor", "xnor"]:
                self.variables.append(char)

    def get_variable_count(self) -> None:
        """Gets the amount of variables for manual insertion into the truth table"""
        while True:
            count = int(input("Enter number of variables (1 - 4): "))
            while count > 0:
                print(count)
                count2 : int = count
                if count >= 26:
                    count2 = 26
                self.add_variables(count2, int(count/26))
                count -= 26
            break
        print(f"{self.variables}")

    def add_variables(self, count: int, start: int) -> None:
        """Helper method to add variables over 26"""
        for letter in range(count):
            if start > 0:
                self.variables.append(chr(start+65))
            self.variables.append(chr(letter + 65))

    def generate_table(self)-> None:
        """Generates a table"""
        total_rows = 2 ** len(self.variables)

        for i in range(total_rows):
            row = {}
            print(f"Entry {i + 1}:")
            for var in self.variables:
                row[var] = 0
            for j in range(len(self.variables)):
                k = len(self.variables) - j - 1
                print(f"{i}:{j}:{int(i/(2**j))}")
                if int(i / (2**j)) % 2 == 0:
                    row[list(self.variables)[k]] = 0
                else:
                    row[list(self.variables)[k]] = 1
            # TODO: make this get filled in automatically.
            while True:
                y_value = input("Enter output Y (0 or 1): ")
                if y_value in ['0', '1']:
                    row['Y'] = int(y_value)
                    break
                else:
                    print("Invalid input. Enter 0 or 1.")
            print()
            self.table.append(row)

    def display_table(self)-> None:
        """Prints the table"""
        print("\nTruth Table:")
        print("-" * (len(self.variables) * 4 + 6))
        header = " ".join(self.variables) + " | Y"
        print(header)
        print("-" * (len(self.variables) * 4 + 6))
        for row in self.table:
            values = " ".join(str(row[var]) for var in self.variables)
            print(f"{values} | {row['Y']}")
        print("-" * (len(self.variables) * 4 + 6))
table = TruthTable()
table.parse("A AND B")
table.generate_table()
table.display_table()
