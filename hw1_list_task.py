# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]


def remove_adjacent(lst):
    i = 0
    while i + 1 < len(lst):
        if lst[i] == lst[i + 1]:
            lst.pop(i + 1)
        i += 1
    print(lst)
    return

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]


def linear_merge(lst1, lst2):
    i = 0
    j = 0
    lst = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            lst.append(lst1[i])
            i += 1
        else:
            lst.append(lst2[j])
            j += 1
    while i < len(lst1):
        lst.append(lst1[i])
        i += 1
    while j < len(lst2):
        lst.append(lst2[j])
        j += 1
    print(lst)
    return
