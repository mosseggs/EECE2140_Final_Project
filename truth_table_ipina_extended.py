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



def bits_of(i: int, width: int) -> List[int]:
    '''
    convert integer to list of bits (binary).

    :param i: int to get bits of.
    :type i: int
    :param width: width of the bits to get the values of.
    :type width: int
    :return: bits of i.
    :rtype: List[int]
    '''
    return [(i >> (width - 1 - b)) & 1 for b in range(width)]



def sympy_obj_to_words(expr: Any, variables: List[str]) -> str:
    '''
    Convert SymPy expression into readable word-based form

    :param expr: Expressions to change
    :type expr: Any
    :param variables: List of variables
    :type variables: List[str]
    :return: Changed expression
    :rtype: str
    '''
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



def detect_xor_xnor(expr_str: str, variables: List[str]) -> str:
    '''
    Detect XOR and XNOR patterns after simplification

    :param expr_str: Expression to change
    :type expr_str: str
    :param variables: List of Variables
    :type variables: List[str]
    :return: Changed expression
    :rtype: str
    '''
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
            if c not in ["and", "or", "not", "^", "=="]:
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
        norm = norm.replace("xor", "^")
        norm = norm.replace("xnor", "==")
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
        s += "".join(" " for i in range(sum(len(s) for s in sideLevel) + len(sideLevel) - 1))
        s += ",".join(topLevel) + "\n"
        s += ",".join(sideLevel) + " "
        s += "".join(" " for i in range(sum(len(s) for s in topLevel) + len(topLevel) - 1)) + " " \
            + " ".join([bin(i)[2::].zfill(len(topLevel)) \
            + "".join(" " for j in range(2 * math.floor(len(topLevel) / 2) \
                + 1 - len(topLevel))) for i in cols]) + "\n"
        s += "".join(" " for i in range(sum(len(s) for s in sideLevel) \
            + sum(len(s) for s in topLevel) + len(sideLevel) + len(topLevel) - 1)) + "+"
        s += "".join(["".join(["-" for j in range(2 * math.floor(len(topLevel) / 2) + 1)]) \
            + "+" for i in range(len(cols))]) + "\n"
        for r in rows:
            s += "".join(" " for i in range(sum(len(s) for s in sideLevel) \
                + sum(len(s) for s in topLevel) + len(topLevel) - 2))
            s += "".join(bin(r)[2::].zfill(len(sideLevel))) + " |" \
                + "".join(["".join([" " for j in range(math.floor(len(topLevel) / 2))]) \
                + "".join(str(grid[r][c])) \
                + "".join([" " for j in range(math.floor(len(topLevel) / 2))]) \
                + "|" for c in range(len(cols))]) + "\n" \
                + "".join(" " for i in range(sum(len(s) for s in sideLevel) \
                    + sum(len(s) for s in topLevel) + len(sideLevel) + len(topLevel) - 1)) + "+" \
                + "".join(["".join(["-" for j in range(2 * math.floor(len(topLevel) / 2) + 1)]) \
                    + "+" for i in cols]) + "\n"
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
