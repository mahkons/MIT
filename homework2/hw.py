from os import walk
import os.path
from hashlib import sha1 as hasher


def get_hash(filename):
    with open(filename, mode='rb') as f:
        h = hasher()
        s = f.read(2 ** 16)
        while(s):
            h.update(s)
            s = f.read(2 ** 16)
        f.close()
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
    for k, lst in dict_files.items():
        if(len(lst) > 1):
            print(':'.join(lst))
    return
