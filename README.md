# EECE2140_Final_Project
For the final project of EECE2140 Computing Fundamentals for Engineers, by Gabriel Lau and Juan Ipina. <br>

The goal of this project was to turn string versions of boolean expressions back into boolean expressions
and obtain the correct truth tables and karnaugh maps from them.<br>

The python file was designed by both Gabriel Lau and Juan Ipina and can handle turning a string into a boolean truth table. It also displays the equation given in a semi-simplified form, as well as a karnaugh map for the equation.<br>
The Matlab file was designed entirely by Juan Ipina, and uses the python file to take in a designated string and display the truth table and a karnaugh map for the equation. It can also take in a truth table to complete the same equations. <br>
Variable names are allowed to occur multiple times, and can be longer than 1 letter. However, certain words such as "as" or "and" or "not" are not allowed as variable names because it will interfere with python's code.<br>

Our approach to the conversion from string to boolean expression was to utilize the bits_of and eval functions in python to evaluate each row and obtain an output, then line that up to the various tables we made.<br>

How to run code:
-
1. Ensure you have python and sympy on your computer
2. Open the "truth_table_ui_ipina.m" file in matlab
3. run

Results:
-
Expression entered: (A and B) or (A and C)

Truth Table:<br>
-------<br>
A B C | Y<br>
-------<br>
0 0 0 | 0<br>
0 0 1 | 0<br>
0 1 0 | 0<br>
0 1 1 | 0<br>
1 0 0 | 0<br>
1 0 1 | 1<br>
1 1 0 | 1<br>
1 1 1 | 1<br>
-------<br>


Boolean expression:<br>
(A AND B) OR (A AND C)<br>

Karnaugh Map:<br>
<br>
 B,C<br>
A     00  01  11  10 <br>
     +---+---+---+---+<br>
   0 | 0 | 0 | 0 | 0 |<br>
     +---+---+---+---+<br>
   1 | 0 | 1 | 1 | 1 |<br>
     +---+---+---+---+<br>
<br>
