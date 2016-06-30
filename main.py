# -*- coding: utf-8 -*-
import argparse
# import os # unused
from sys import stdout


def count(file_in_path, output):
    # dirname = os.path.dirname(file_in_path) # unused

    file_in = open(file_in_path)

    # getting information from first 3 lines
    dataorganisation = file_in.readline()  # ignored
    data = file_in.readline()  # getting information from file
    datastructure = file_in.readline()  # unused
    datacheck = file_in.readline()  # unused

    data = data.split()
    del data[0]

    size = int(data[0])
    # corrotation = int(data[1])  # unused
    # pcnumber = int(data[2])  # unused
    # pcrotation = int(data[3])  # unused
    pos_x = int(data[4])
    pos_y = int(data[5])
    hamming = int(data[6])
    nb_pieces = int(data[7])

    is_present = [[[False for k in xrange(4)] for j in xrange(size * size)]
                  for i in xrange(nb_pieces)]
    stdout.write("processing lines (this may take a while) ")
    stdout.flush()
    for idx, line in enumerate(file_in):
        if idx % 100000 == 0:
            stdout.write(".")
            stdout.flush()

        line_tab = line.split(";")
        for depth in xrange(nb_pieces):
            pc = line_tab[depth].split(':')
            if pc[0] != '-1':
                if is_present[depth][int(pc[0])][int(pc[1])] is False:
                    is_present[depth][int(pc[0])][int(pc[1])] = True

    counter = [0 for i in xrange(nb_pieces)]
    plate = [[0 for j in xrange(size)] for i in xrange(size)]

    count_pieces(is_present, counter, nb_pieces, size)

    put_on_plate(counter, size, plate, pos_x, pos_y, hamming)

    display_plate(plate, file_in_path, output)


def put_on_plate(counter, size, plate, pos_x, pos_y, hamming):
    cpt = 0
    if pos_x < size:
        plate[pos_x][pos_y] = counter[cpt]
    cpt += 1
    for i in xrange(1, hamming + 1):
        pos_x += 1
        for j in xrange(i):
            if 0 <= pos_x < size and 0 <= pos_y < size:
                plate[pos_x][pos_y] = counter[cpt]
            cpt += 1
            pos_x -= 1
            pos_y += 1
        for j in xrange(i):
            if 0 <= pos_x < size and 0 <= pos_y < size:
                plate[pos_x][pos_y] = counter[cpt]
            cpt += 1
            pos_x -= 1
            pos_y -= 1
        for j in xrange(i):
            if 0 <= pos_x < size and 0 <= pos_y < size:
                plate[pos_x][pos_y] = counter[cpt]
            cpt += 1
            pos_x += 1
            pos_y -= 1
        for j in xrange(i):
            if 0 <= pos_x < size and 0 <= pos_y < size:
                plate[pos_x][pos_y] = counter[cpt]
            cpt += 1
            pos_x += 1
            pos_y += 1


def display_plate(plate, file_in_path, output):
    s = [[str(e) for e in row] for row in plate]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    stdout.write("\r")
    stdout.flush()
    if output:
        file_out = open("stat_" + file_in_path, "w+")
        file_out.writelines('\n'.join(table))
    else:
        print '\n'.join(table)


def count_pieces(is_present, counter, nb_pieces, size):
    for i in xrange(nb_pieces):
        for j in xrange(size * size):
            for k in xrange(4):
                if is_present[i][j][k]:
                    counter[i] += 1


def main():
    parser = argparse.ArgumentParser(
        description="The eternity cardinality matrix")

    parser.add_argument("files_path", metavar="input-file", type=str,
                        nargs='+', help="The file path")
    parser.add_argument("-o", "--output", action="store_true",
                        help="saves the count in file stat_[input-file]")

    args = parser.parse_args()
    # Opening the file
    for file_path in args.files_path:
        print "File : " + file_path
        count(file_path, args.output)
    return


if __name__ == "__main__":
    main()
