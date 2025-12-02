# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 14:05:36 2025

@author: juani and gabrielL
"""

import math
from typing import Any, List

# import SymPy
try:
    import sympy
    from sympy.logic.boolalg import simplify_logic
    sympy_available = True
except Exception:
    sympy_available = False



# convert integer to list of bits (binary)
def bits_of(i: int, width: int) -> List[int]:
    return [(i >> (width - 1 - b)) & 1 for b in range(width)]



# Convert SymPy expression into readable word-based form
def sympy_obj_to_words(expr: Any, variables: List[str]) -> str:
    if expr is True:
        return "1"
    if expr is False:
        return "0"

    s = str(expr)
    s = s.replace("&", " AND ")
    s = s.replace("|", " OR ")
    s = s.replace("~", " NOT ")
    s = s.replace("True", "1").replace("False", "0")

    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip()



# Detect XOR and XNOR patterns after simplification
def detect_xor_xnor(expr_str: str, variables: List[str]) -> str:
    s = expr_str.replace(" ", "")


    if len(variables) == 2:
        A, B = variables

        # XOR pattern
        xor1 = f"({A}ANDNOT{B})OR({B}ANDNOT{A})"
        xor2 = f"({B}ANDNOT{A})OR({A}ANDNOT{B})"

        # XNOR pattern
        xnor1 = f"({A}AND{B})OR(NOT{A}ANDNOT{B})"
        xnor2 = f"(NOT{A}ANDNOT{B})OR({A}AND{B})"

        if s == xor1 or s == xor2:
            return f"{A} XOR {B}"
        if s == xnor1 or s == xnor2:
            return f"{A} XNOR {B}"

    return expr_str



class TruthTableExtended:

    def __init__(self, variables: List[str], outputs: List[int]):

        self.variables = variables
        self.outputs = outputs


    def print_truth_table(self) -> str:
        s = "Truth Table:\n"
        s += "-------\n"
        s += " ".join(self.variables) + " | Y\n"
        s += "-------\n"

        n = len(self.variables)
        rows = 2 ** n

        for i in range(rows):
            bits_i = bits_of(i, n)
            s += " ".join(str(x) for x in bits_i) + " | " + str(self.outputs[i]) + "\n"

        s += "-------\n\n"
        return s


    @staticmethod
    def detect_variables(expr: str) -> List[str]:
        found = []
        for c in expr.replace("(","").replace(")","").split():
            if c not in ["and", "or", "not", "^", "=="]:  # Supports up to 5 variables, can be removed later if need be
                if c not in found:
                    found.append(c)
        found.sort()
        return found


    @staticmethod
    def from_expression(expr_raw: str) -> 'TruthTableExtended':

         # Normalize expression for Python eval
        norm = expr_raw
        norm = norm.replace(" AND ", " and ")
        norm = norm.replace(" OR ", " or ")
        norm = norm.replace(" NOT ", " not ")
        norm = norm.replace("XOR", "^")
        norm = norm.replace("XNOR", "==")
        norm = norm.replace("&", " and ")
        norm = norm.replace("|", " or ")
        norm = norm.replace("~", " not ")

        variables = TruthTableExtended.detect_variables(norm)
        n = len(variables)
        rows = 2 ** n

        outputs = []

        # Evaluate expression for each truth table row
        for i in range(rows):
            bits_i = bits_of(i, n)

            # Assign variable True/False
            env = {variables[idx]: (bits_i[idx] == 1) for idx in range(n)}

            # Evaluate expression
            try:
                val = eval(norm, {}, env)
            except Exception:
                val = False
            outputs.append(1 if val else 0)

        return TruthTableExtended(variables, outputs)


    @staticmethod
    def from_manual(n: int, outs: List[int]) -> 'TruthTableExtended':
        variables = [chr(ord('A') + i) for i in range(n)]
        return TruthTableExtended(variables, outs)



    def min_expression(self) -> str:
        true_terms = [i for i, v in enumerate(self.outputs) if v == 1]

        # Special cases
        if not true_terms:
            return "0"
        if len(true_terms) == len(self.outputs):
            return "1"

        if sympy_available:
            try:
                syms = [sympy.Symbol(v) for v in self.variables]
                expr = sympy.logic.boolalg.SOPform(syms, true_terms)
                simp = simplify_logic(expr, force=True, form="dnf")
                word = sympy_obj_to_words(simp, self.variables)
            except:
                return self._fallback(true_terms)
        else:
            return self._fallback(true_terms)

        # Additional XOR/XNOR detection
        return detect_xor_xnor(word, self.variables)



    def _fallback(self, terms : List[int]) -> str:
        n = len(self.variables)
        parts = []

        for i in terms:
            bits_i = bits_of(i, n)
            literals = []
            for idx, b in enumerate(bits_i):
                if b == 1:
                    literals.append(self.variables[idx])
                else:
                    literals.append("NOT " + self.variables[idx])
            parts.append("(" + " AND ".join(literals) + ")")

        return " OR ".join(parts)


# Old K-map code
    # def k_map(self) -> str:
    #     n = len(self.variables)
    #     if n == 1: return self._k1()
    #     if n == 2: return self._k2()
    #     if n == 3: return self._k3()
    #     if n == 4: return self._k4()
    #     if n == 5: return self._k5()
    #     return "K-map not supported for this number of variables.\n"


    # # 1-variable K-map
    # def _k1(self) -> str:
    #     A = self.outputs
    #     return (
    #         "Karnaugh Map:\n"
    #         "A\n"
    #         "+---+\n"
    #         f"| {A[0]} |\n"
    #         "+---+\n"
    #         f"| {A[1]} |\n"
    #         "+---+\n"
    #     )


    # # 2-variable K-map (A,B)
    # def _k2(self) -> str:
    #     A = self.outputs

    #     grid = [
    #         [A[0], A[1]],
    #         [A[2], A[3]]
    #     ]

    #     s = "Karnaugh Map:\n\n"
    #     s += "      B\n"
    #     s += "      0   1\n"
    #     s += "    +---+---+\n"
    #     s += f"A 0 | {grid[0][0]} | {grid[0][1]} |\n"
    #     s += "    +---+---+\n"
    #     s += f"  1 | {grid[1][0]} | {grid[1][1]} |\n"
    #     s += "    +---+---+\n"
    #     return s


    # # 3-variable K-map (A,B,C)
    # def _k3(self) -> str:
    #     A = self.outputs

    #     # Gray-code reorder 00,01,11,10
    #     grid = [
    #         [A[0], A[1], A[3], A[2]],
    #         [A[4], A[5], A[7], A[6]]
    #     ]

    #     s = "Karnaugh Map:\n\n"
    #     s += "            BC\n"
    #     s += "        00  01  11  10\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"A 0   | {grid[0][0]} | {grid[0][1]} | {grid[0][2]} | {grid[0][3]} |\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"  1   | {grid[1][0]} | {grid[1][1]} | {grid[1][2]} | {grid[1][3]} |\n"
    #     s += "      +---+---+---+---+\n"
    #     return s


    # # 4-variable K-map (A,B,C,D)
    # def _k4(self) -> str:
    #     A = self.outputs

    #     # Gray-code row/column
    #     ro = [0, 1, 3, 2]
    #     co = [0, 1, 3, 2]

    #     grid = []
    #     for r in ro:
    #         row = []
    #         for c in co:
    #             idx = (r << 2) | c
    #             row.append(A[idx])
    #         grid.append(row)

    #     s = "Karnaugh Map:\n\n"
    #     s += "                 CD\n"
    #     s += "           00  01  11  10\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"AB 00 | {grid[0][0]} | {grid[0][1]} | {grid[0][2]} | {grid[0][3]} |\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"   01 | {grid[1][0]} | {grid[1][1]} | {grid[1][2]} | {grid[1][3]} |\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"   11 | {grid[2][0]} | {grid[2][1]} | {grid[2][2]} | {grid[2][3]} |\n"
    #     s += "      +---+---+---+---+\n"
    #     s += f"   10 | {grid[3][0]} | {grid[3][1]} | {grid[3][2]} | {grid[3][3]} |\n"
    #     s += "      +---+---+---+---+\n"

    #     return s


    # # 5-variable K-map (A,B,C,D,E)
    # def _k5(self) -> str:
    #     A = self.outputs

    #     ro = [0, 1, 3, 2]
    #     co = [0, 1, 3, 2, 6, 7, 5, 4]

    #     grid = []
    #     for r in ro:
    #         row = []
    #         for c in co:
    #             idx = (r << 3) | c
    #             row.append(A[idx])
    #         grid.append(row)

    #     s = "Karnaugh Map:\n\n"
    #     s += "                            DE\n"
    #     s += "           00 01 11 10  110 111 101 100\n"
    #     s += ("      +" + "---+" * 8 + "\n")

    #     labels = ["000", "001", "011", "010"]    # Gray-code ABC rows

    #     for ir, r in enumerate(grid):
    #         s += f"ABC {labels[ir]} | " + " | ".join(str(x) for x in r) + " |\n"
    #         s += ("      +" + "---+" * 8 + "\n")

    #     return s

    def kmap(self) -> str:
        A = self.outputs
        n : int = len(self.variables)
        topLevel : list[str] = self.variables[math.floor(n/2):]
        sideLevel : list[str] = self.variables[:math.floor(n/2)]
        rows = [(i ^ (i >> 1)) for i in range(1 << math.floor(n/2))]
        cols = [(i ^ (i >> 1)) for i in range(1 << n - math.floor(n/2))]
        grid : list[list[int]] = []
        for r in range(len(rows)):
            row = []
            for c in cols:
                idx = (r << math.ceil(n / 2)) | c
                row.append(A[idx])
            grid.append(row)
        s = "Karnaugh Map:\n\n"
        s += "".join(" " for i in range(len(sideLevel)))
        s += "".join(topLevel) + "\n"
        s += "".join(sideLevel) + " " + "".join(" " for i in range(len(topLevel))) + " " \
            + " ".join([bin(i)[2::].zfill(len(topLevel)) for i in cols]) + "\n"
        s += "".join(" " for i in range(len(sideLevel) + len(topLevel) + 1)) + "+" \
            + "".join(["".join(["-" for j in range(len(topLevel))]) \
            + "+" for i in range(len(cols))]) + "\n"
        for r in rows:
            s += "".join(" " for i in range(len(sideLevel))) \
                + "".join(bin(r)[2::].zfill(len(topLevel))) + " |" \
                + "".join(["".join([" " for j in range(math.floor(len(topLevel) / 2))]) \
                + "".join(str(grid[r][c])) \
                + "".join([" " for j in range(math.floor(len(topLevel) / 2))]) \
                + "|" for c in range(len(cols))]) + "\n" \
                + "".join(" " for i in range(len(sideLevel) + len(topLevel) + 1)) + "+" \
                + "".join(["".join(["-" for j in range(len(topLevel))]) + "+" for i in cols]) + "\n"
        return s

def cli_main(argv:List[str]) -> None:



    if len(argv) < 2:
        print("Missing mode.")
        return

    mode = argv[1]

    # Expression mode
    if mode == "expr":
        expr = argv[2]
        t = TruthTableExtended.from_expression(expr)

    # Manual truth table mode
    elif mode == "manual":
        n = int(argv[2])
        fname = argv[3]

        with open(fname, "r") as f:
            outs = [int(line.strip()) for line in f if line.strip() != ""]

        t = TruthTableExtended.from_manual(n, outs)

    else:
        print("Unknown mode.")
        return

    # Print results for MATLAB to capture
    print(t.print_truth_table())
    print("Boolean expression:")
    print(t.min_expression())
    print()
    print(t.kmap())



if __name__ == "__main__":
    import sys
    cli_main(sys.argv)
