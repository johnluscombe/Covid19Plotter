def array_to_lower_case(arr):
    for i in range(len(arr)):
        arr[i] = arr[i].lower()
    return arr


def get_array_diffs(arr):
    if len(arr) > 0:
        diffs = arr[:1]
        for i in range(1, len(arr)):
            diffs.append(arr[i] - arr[i - 1])
        return diffs
    return []