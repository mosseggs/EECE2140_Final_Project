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