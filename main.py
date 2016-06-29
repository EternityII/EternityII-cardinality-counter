# -*- coding: utf-8 -*-
import argparse
import os
from pprint import pprint


def count(file_in_path):
    dirname = os.path.dirname(file_in_path)

    file_in = open(file_in_path)

    # getting information from first 3 lines
    dataorganisation = file_in.readline()  # ignored
    data = file_in.readline()  # getting information from file
    datastructure = file_in.readline()
    datacheck = file_in.readline()

    data = data.split()
    del data[0]

    size = int(data[0])
    corrotation = int(data[1])
    pcnumber = int(data[2])
    pcrotation = int(data[3])
    posx = int(data[5])
    posy = int(data[6])
    hamming = int(data[6])
    nbpieces = int(data[7])

    ispresent = [[[False for k in xrange(4)] for j in xrange(size * size)] for i in xrange(nbpieces)]

    while 1:
        lines = file_in.readlines(100000)
        if not lines:
            break
        for line in xrange(len(lines)):
            line_tab = lines[line].split(";")
            for depth in xrange(nbpieces):
                pc = line_tab[depth].split(':')
                if pc[0] != '-1':
                    if ispresent[depth][int(pc[0])][int(pc[1])] is False:
                        ispresent[depth][int(pc[0])][int(pc[1])] = True

    counter = [0 for i in xrange(nbpieces)]
    countpieces(ispresent, counter, nbpieces, size)

    plate = [[0 for j in xrange(size)] for i in xrange(size)]
    putonplate(counter, plate, posx, posy)


def putonplate(counter, plate, posx, posy):
    # TODO
    print "todo"


def countpieces(ispresent, counter, nbpieces, size):
    for i in xrange(nbpieces):
        for j in xrange(size * size):
            for k in xrange(4):
                if ispresent[i][j][k]:
                    counter[i] += 1


def main():
    parser = argparse.ArgumentParser(description="The eternity cardinality matrix")

    parser.add_argument("files_path", metavar="input-file", type=str, nargs='+', help="The file path")

    args = parser.parse_args()
    # Opening the file
    for file_path in args.files_path:
        count(file_path)
    return


if __name__ == "__main__":
    main()
