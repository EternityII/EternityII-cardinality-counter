# -*- coding: utf-8 -*-
import argparse
import os
from sys import stdout


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
    posx = int(data[4])
    posy = int(data[5])
    hamming = int(data[6])
    nbpieces = int(data[7])

    ispresent = [[[False for k in xrange(4)] for j in xrange(size * size)] for i in xrange(nbpieces)]
    stdout.write("processing lines:")
    stdout.flush()
    for line in file_in:
        line_tab = line.split(";")
        for depth in xrange(nbpieces):
            pc = line_tab[depth].split(':')
            if pc[0] != '-1':
                if ispresent[depth][int(pc[0])][int(pc[1])] is False:
                    ispresent[depth][int(pc[0])][int(pc[1])] = True

    counter = [0 for i in xrange(nbpieces)]
    countpieces(ispresent, counter, nbpieces, size)

    plate = [[0 for j in xrange(size)] for i in xrange(size)]
    putonplate(counter, size, plate, posx, posy, hamming)


def putonplate(counter, size, plate, posx, posy, hamming):
    cpt = 0
    if posx < size:
        plate[posx][posy] = counter[cpt]
    cpt += 1
    for i in xrange(1, hamming + 1):
        posx += 1
        for j in xrange(i):
            if 0 <= posx < size and 0 <= posy < size:
                plate[posx][posy] = counter[cpt]
            cpt += 1
            posx -= 1
            posy += 1
        for j in xrange(i):
            if 0 <= posx < size and 0 <= posy < size:
                plate[posx][posy] = counter[cpt]
            cpt += 1
            posx -= 1
            posy -= 1
        for j in xrange(i):
            if 0 <= posx < size and 0 <= posy < size:
                plate[posx][posy] = counter[cpt]
            cpt += 1
            posx += 1
            posy -= 1
        for j in xrange(i):
            if 0 <= posx < size and 0 <= posy < size:
                plate[posx][posy] = counter[cpt]
            cpt += 1
            posx += 1
            posy += 1

    s = [[str(e) for e in row] for row in plate]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    stdout.write("\r")
    stdout.flush()
    print '\n'.join(table)


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
        print "File : " + file_path
        count(file_path)
    return


if __name__ == "__main__":
    main()
