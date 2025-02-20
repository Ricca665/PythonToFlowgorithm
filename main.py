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
        line = line.strip()

        # Check if the line contains a simple print statement
        if line.startswith("print("):
            expr = line[7:-2]  # Remove 'print(' and ')'
            f.writelines(f'            <output expression="&quot;{expr}&quot;" newline="True"/>\n')
        
        if line.startswith("input("):
            ask = line[6:-1]  # Remove 'input(' and ')'
            f.writelines(f'            <declare name={ask} type="Integer" array="False" size=""/>\n')
            f.writelines(f'            <input variable={ask}/>\n')

    f.writelines("</body>\n")
    f.writelines("</function>\n")
    f.writelines("</flowgorithm>\n")
    f.close()
