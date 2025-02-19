import os
import argparse
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser("Python to Flowgorytmh/Flowchart")
parser.add_argument("input_filename", help="Input filename", type=str)
parser.add_argument("name_of_program", help="Output filename that flowgorithm will report", type=str)
parser.add_argument("authors_of_program", help="Authors of the program", type=str)
parser.add_argument("output", help="Authors of the program", type=str)
args = parser.parse_args()

name_of_program = args.name_of_program
author = args.authors_of_program
try:
    os.remove(args.output)
except FileNotFoundError:
    pass

f = open(args.output, "a")
f.write("")
f.writelines('''<?xml version="1.0"?>
<flowgorithm fileversion="4.2">
    <attributes>''')

f.writelines(f'\n        <attribute name="name" value="{name_of_program}"/>')
f.writelines(f'\n        <attribute name="authors" value="{author}"/>')
f.writelines(
'''
        <attribute name="about" value=""/>
        <attribute name="saved" value=""/>
        <attribute name="created" value=""/>
        <attribute name="edited" value=""/>
    </attributes>
    <function name="Main" type="None" variable="">
        <parameters/>
        <body>''')

with open(args.input_filename, "r") as z:
    python_code_lines = z.readlines()  # Read all lines from the file

    indent_level = 0

    for line in python_code_lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line contains a simple print statement
        if line.startswith("print("):
            # Extract the content of print and properly format it in the Flowgorithm XML
            expr = line[7:-2]  # Remove 'print(' and ')'
            f.writelines(f'            <output expression="&quot;{expr}&quot;" newline="True"/>\n')
        
        if line.startswith("input("):
            ask = line[6:-1]  # Remove 'input(' and ')'
            f.writelines(f'            <declare name={ask} type="Integer" array="False" size=""/>\n')
            f.writelines(f'            <input variable={ask}/>\n')
        # Check for 'if' statements
        elif line.startswith("if"):
            condition = line[2:].strip()  # Extract condition after "if"
            f.writelines(f"            <if expression='{condition}'>\n")
        
        # Check for 'else' statements
        elif line.startswith("else"):
            f.writelines("            <else>\n")

        # Check for 'for' or 'while' loops
        elif line.startswith("for") or line.startswith("while"):
            loop_type = "for" if line.startswith("for") else "while"
            f.writelines(f"            <loop type='{loop_type}'>\n")

        # Handle indentation and increase indent level
        if line.endswith(":"):
            indent_level += 1
        
        # Close block after handling the logic inside
        if indent_level > 0 and line == "":
            indent_level -= 1

    f.writelines("</body>\n")
    f.writelines("</function>\n")
    f.writelines("</flowgorithm>\n")
    f.close()
