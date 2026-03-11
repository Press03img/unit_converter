from units_data import units

def convert(value, from_unit, to_unit, category):

    if category == "温度":
        return convert_temperature(value, from_unit, to_unit)

    base = value * units[category][from_unit]

    result = base / units[category][to_unit]

    return result


def convert_temperature(v, f, t):

    if f == "℃":
        c = v
    elif f == "℉":
        c = (v - 32) * 5/9
    elif f == "K":
        c = v - 273.15

    if t == "℃":
        return c
    elif t == "℉":
        return c * 9/5 + 32
    elif t == "K":
        return c + 273.15