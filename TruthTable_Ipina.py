# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 14:05:36 2025

@author: juani
"""
class TruthTable:
    def __init__(self):
        self.variables = []
        self.table = []

    def get_variable_count(self):
        while True:
            try:
                count = int(input("Enter number of variables (1 - 4): "))
                if 1 <= count <= 4:
                    self.variables = ['A', 'B', 'C', 'D'][:count]
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Enter a number between 1 and 4.")

    def generate_table(self):
        total_rows = 2 ** len(self.variables)

        for i in range(total_rows):
            row = {}
            print(f"Entry {i + 1}:")
            for var in self.variables:
                while True:
                    value = input(f"Enter value for {var} (0 or 1): ")
                    if value in ['0', '1']:
                        row[var] = int(value)
                        break
                    else:
                        print("Invalid input. Enter 0 or 1.")
            while True:
                y_value = input("Enter output Y (0 or 1): ")
                if y_value in ['0', '1']:
                    row['Y'] = int(y_value)
                    break
                else:
                    print("Invalid input. Enter 0 or 1.")
            print()
            self.table.append(row)

    def display_table(self):
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
table.get_variable_count()
table.generate_table()
table.display_table()



