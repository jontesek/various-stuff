# -*- coding: utf-8 -*-
"""
GOAL: parse file to CSV file with columns: study language, field of study, university, level (bc/ing/phd), capacity
"""
import os
import re
import codecs
from TextWriter import TextWriter

# input: SK (Business and administration) - Matej Bell University in Banska Bystrica - bakalářský, magisterský navazující [kapacita 2]
reg_exp = re.compile('^([A-Z]+) \((.+)\) - (.+) - (.+) \[kapacita (\d+)\]')

studies = []

def parse_d_level(text):
    d_levels = [x.strip().encode('utf-8') for x in result.group(4).split(',')]
    r_bc = True if 'bakalářský' in d_levels else False
    r_ing = True if 'magisterský navazující' in d_levels else False
    r_phd = True if 'doktorský' in d_levels else False
    return r_bc, r_ing, r_phd


# Read file and get studies
f_obj = codecs.open("studies_in.txt", "r", encoding="utf-8")
for line in f_obj:
    # Parse line
    result = reg_exp.match(line)
    # Parse degree level
    (l_bc, l_ing, l_phd) = parse_d_level(result.group(4))
    # Save data
    row = [result.group(1), result.group(2), result.group(3), str(l_bc), str(l_ing), str(l_phd), result.group(5)]
    studies.append(row)

# Prepare header
header = [
    'study language', 'field of study', 'university', 'bc', 'ing', 'phd', 'capacity'
]
studies.insert(0, header)

# Get path to the script directory.
output_dir = os.path.dirname(os.path.realpath(__file__))
# Create a CSV file from the list.
tw = TextWriter(output_dir)
tw.write_studies_file('studies_out', studies)


