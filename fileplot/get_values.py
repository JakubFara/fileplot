from fileplot.plot import load_array_from_file
import numpy as np


def get_value(rule: str, filename: str, key: str, point: list = None, get_arg: 'str' = None):
    array = load_array_from_file(filename)
    if isinstance(key, str):
        values = array.get(key)
    else:
        values = key(array)
    if array is None:
        print(f"key {key} not found")
        return None
    if rule == "max":
        if get_arg is None:
            return np.max(values[100:])
        return {
                key: np.max(values),
                get_arg: array[get_arg][np.argmax(values)]
            }
    if rule == "min":
        if get_arg is None:
            return np.min(values)
        return {
                key: np.min(values),
                get_arg: array[get_arg][np.argmin(values)]
            }

    if rule == "mean":
        return np.mean(values)
    if rule == "atpoint":
        if point == None:
            print("you need to specify point")
            return None
        unknown = np.array(array.get(point[0]))
        if unknown is None:
            print(f"not found key {point[0]}")
            return None
        # np.where(unknown == point[1])
        idx = (np.abs(unknown - point[1])).argmin()
        if unknown[idx] != point[1]:
            print("warning point does not exist clossest it {unknown[idx]}")
        return {key: values[idx], point[0]: point[1]}
