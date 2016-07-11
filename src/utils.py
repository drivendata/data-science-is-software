from __future__ import print_function

import json
import os
import sys


def print_file_tree(startpath):
    """ Prints a directory and its contents
    """
    for root, dirs, files in os.walk(startpath):

        # skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        print('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not f.startswith("."):
                print('{}{}'.format(subindent, f))


def generate_lab_from_solution(ipynb_path):
    """ Strictly removes input ant output of code cells prefixed
        with #SOLUTION from a jupyter notebook.

        This is a little hacky, but keeps the nbs in sync easily
    """
    lab_file = ipynb_path.replace('-solution', '-lab')

    raw_nb = json.load(open(ipynb_path))

    def _is_solution_cell(c):
        # source is a list of strings representing each line
        return (c['cell_type'] == 'code' and
                len(c['source']) > 0 and
                c['source'][0].startswith("#SOLUTION"))

    no_sol_cells = [c for c in raw_nb['cells'] if not _is_solution_cell(c)]

    raw_nb["cells"] = no_sol_cells

    with open(lab_file, "w") as lab_out:
        json.dump(raw_nb, lab_out)


if __name__ == "__main__":
    generate_lab_from_solution(sys.argv[1])
