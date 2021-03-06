import numpy as np
import sys


def matrix_prod(a, b):
    if(a.shape[0] <= 2):
        return np.dot(a, b)
    a = np.vsplit(a, 2)
    a[0] = np.hsplit(a[0], 2)
    a[1] = np.hsplit(a[1], 2)
    b = np.vsplit(b, 2)
    b[0] = np.hsplit(b[0], 2)
    b[1] = np.hsplit(b[1], 2)
    p1 = matrix_prod(a[0][0] + a[1][1], b[0][0] + b[1][1])
    p2 = matrix_prod(a[1][0] + a[1][1], b[0][0])
    p3 = matrix_prod(a[0][0], b[0][1] - b[1][1])
    p4 = matrix_prod(a[1][1], b[1][0] - b[0][0])
    p5 = matrix_prod(a[0][0] + a[0][1], b[1][1])
    p6 = matrix_prod(a[1][0] - a[0][0], b[0][0] + b[0][1])
    p7 = matrix_prod(a[0][1] - a[1][1], b[1][0] + b[1][1])
    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6
    return np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))


def print_matrix(c, n):
    for i in range(n):
        for j in range(n):
            print(c[i, j], end=' ')
        print()
    return


def get_pw_2(n):
    pw_2 = 1
    while(pw_2 < n):
        pw_2 = pw_2 * 2
    return pw_2


def get_matrix(n):
    pw_2 = get_pw_2(n)
    a = np.zeros((pw_2, n), dtype=int)
    for i in range(n):
        a[i] = input().split()
    a = np.hstack((a, np.zeros((pw_2, pw_2 - n), dtype=int)))
    return a


def get_and_print_matrix():
    n = int(input())
    a = get_matrix(n)
    b = get_matrix(n)
    c = matrix_prod(a, b)
    print_matrix(c, n)
    return

if __name__ == "__main__":
    get_and_print_matrix()
