import numpy as np


p = ['↑', '←', '↓', '→']


def get_char_list():
    return list(map(str, input().split()))


def print_iterable(p):
    print("  ".join(map(str, p)))


def action(l, i, j, o):
    if o == 0:
        i = max(0, i-1)
    elif o == 2:
        i = min(len(l)-1, i+1)
    elif o == 1:
        j = max(0, j-1)
    else:
        j = min(len(l[0])-1, j+1)
    return i, j


def value(l, i, j, q, prob, y, d):
    a = i
    b = j
    val = 0
    i, j = action(l, i, j, q)
    if d[i][j] != 'X':
        val += prob*y*l[i][j]
    i = a
    j = b
    i, j = action(l, i, j, (q+1) % 4)
    if d[i][j] != 'X':
        val += ((1-prob)/2) * y * l[i][j]
    i = a
    j = b
    i, j = action(l, i, j, (q-1) % 4)
    if d[i][j] != 'X':
        val += ((1-prob)/2) * y * l[i][j]
    return val


def opt_val(l, i, j, prob, y, d):
    a0 = value(l, i, j, 0, prob, y, d)
    a1 = value(l, i, j, 1, prob, y, d)
    a2 = value(l, i, j, 2, prob, y, d)
    a3 = value(l, i, j, 3, prob, y, d)
    if a0 == max(a0, a1, a2, a3):
        return a0, 0
    if a1 == max(a0, a1, a2, a3):
        return a1, 1
    if a2 == max(a0, a1, a2, a3):
        return a2, 2
    if a3 == max(a0, a1, a2, a3):
        return a3, 3


def error(a, l):
    e = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            e += (a[i][j]-l[i][j])*(a[i][j]-l[i][j])
    return e


def bellman(l, d, prob, y, e, ite):
    a = [[0 for x in range(len(l[0]))] for y in range(len(l))]
    for i in range(len(l)):
        for j in range(len(l[0])):
            if d[i][j] == 'G' or d[i][j] == 'B' or d[i][j] == 'X':
                a[i][j] = l[i][j]
            else:
                a[i][j], q = opt_val(l, i, j, prob, y, d)
                d[i][j] = p[q]
    if error(a, l) > e and ite < 980:
        bellman(a, d, prob, y, e, ite+1)
    else:
        for i in range(len(d)):
            for j in range(len(d[0])):
                if d[i][j] == 'X':
                    d[i][j] = ' '
        for k in range(len(d)):
            print_iterable(d[k])
        print("")
        print("Total number of iterations is " + str(ite+1))
        print("")
        s = input("Would you like to see the final value matrix? [Y/N]: ")
        if s == 'Y':
            print("")
            print(np.matrix(a))


def main():
    n = int(input("Enter the number of rows in the maze: "))
    m = int(input("Enter the number of columns in the maze: "))
    print("")
    print("NOTE:")
    print("_ represent walkable paths")
    print("X represent obstacles")
    print("G represent good ending blocks")
    print("B represent bad ending blocks")
    print("P.S. Leave a space between 2 blocks in a single row while typing in the maze")
    print("")
    print("For reference:")
    print("")
    print("_ _ _ G")
    print("_ X _ B")
    print("_ _ _ _")
    print("")
    print("Enter the maze using _, X, G and B: ")
    d = [['_' for x in range(m)] for y in range(n)]
    ls = [[0 for x in range(m)] for y in range(n)]
    for i in range(n):
        d[i] = get_char_list()
    for i in range(n):
        for j in range(m):
            if d[i][j] == 'G':
                ls[i][j] = 1
            elif d[i][j] == 'B':
                ls[i][j] = -1
    print("")
    prob = float(input("Enter a probability between 0 and 1 of the player to take the right path: "))
    print("")
    print("NOTE:")
    print("Discount factor is a value between 0 and 1 that depicts how much the player cares about future rewards. For best results, value should be close to 0.9")
    print("")
    y = float(input("Enter the discount factor: "))
    print("")
    for k in range(len(d)):
        print_iterable(d[k])
    print("")
    print("")
    print("FINAL RESULT:")
    print("")
    bellman(ls, d, prob, y, 1e-10, 0)


if __name__ == '__main__':
    main()
