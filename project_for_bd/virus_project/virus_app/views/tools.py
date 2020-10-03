def create_two_elems_in_row(lst):
    result = []
    for i in range(len(lst) // 2):
        result.append([lst[i * 2], lst[i * 2 + 1]])
    if (len(lst) % 2 == 1):
        result.append([lst[len(lst) - 1], None])
    return result