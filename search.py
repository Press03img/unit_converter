from units_data import units

def search_unit(keyword):

    result = []

    for cat, u in units.items():

        for name in u:

            if keyword.lower() in name.lower():

                result.append((cat,name))

    return result