#!/usr/bin/python

from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import range
import sys
from optparse import OptionParser

import forgi.graph.bulge_graph as cgb

def main():

    usage = """
        Usage: ./dotbracket_to_element_string.py file.dotbracket"

        Convert a dotbracket notation to an element-type notation
        where the type of each element is shown.

        For example, the string '..((..))..' will be converted
        to 'ffsshhsstt' to indicate the presence of a fiveprime,
        stem, hairpin, and threeprime section.
        """

    parser = OptionParser(usage = usage)
    parser.add_option('-s', '--secondary-structure', dest='sec_struct', default=False, help="Display the dotbracket represenation of the secondary structure along with the element string.", action='store_true')
    parser.add_option('-n', '--numbers', dest='numbers', default=False, help='Display numbers for the nucleotides', action='store_true')
    parser.add_option('-e', '--element-numbers', dest='element_numbers', default=False, help='Display numbers for the elements. This is used to distinguish stem "s1" from "s2" etc.', action='store_true')

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        sys.exit(1)

    if args[0] == '-':
        f = sys.stdin
    else:
        f = open(args[0])

    brackets = "".join(f.readlines()).replace('\n', '')
    bg = cgb.BulgeGraph()


    if len(brackets.strip()) == 0:
        print("Invalid input", file=sys.stderr)
        sys.exit(1)

    bg.from_dotbracket(brackets)

    if options.sec_struct:
        print(bg.dotbracket_str)

    print(bg.to_element_string(options.element_numbers))

    out_strs = []
        
    if options.numbers:
        if options.element_numbers:
            print('-'*bg.seq_length)
        l = bg.seq_length
        mult = 1

        while int(l/mult) > 0:
            out_str = ''
            for i in range(bg.seq_length):
                out_str += str((int(i/mult)) % 10)
            out_strs += [out_str]
            mult *= 10

        print("\n".join(out_strs))
            

if __name__ == "__main__":
    main()
