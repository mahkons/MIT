from os import walk
import os.path
import sys
from hashlib import sha1 as hasher


def get_hash(filename, SZ_READ=2 ** 16):
    # SZ_READ Достаточно большой, чтобы ввод был не слишком медленный
    # и не слишком большой, чтобы он не требовал много памяти
    with open(filename, mode='rb') as f:
        h = hasher()
        s = f.read(SZ_READ)
        while(s):
            h.update(s)
            s = f.read(SZ_READ)
    return h.hexdigest()


def find_duplicates(directory):
    dict_files = {}
    for path, _, filenames in walk(directory):
        for name in filenames:
            to = os.path.join(path, name)
            if name[0] != '.' and name[0] != '~' and not os.path.islink(to):
                cur = get_hash(to)
                if cur not in dict_files:
                    dict_files[cur] = []
                dict_files[cur].append(to)
    for _, lst in dict_files.items():
        if(len(lst) > 1):
            print(':'.join(lst))
    return

if __name__ == "__main__":
    find_duplicates(sys.argv[1])
