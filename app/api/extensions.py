def compare(dict_first, dict_second):
    """
            Validates the auth token
            :param dict_second: second dict to compare
            :param dict_first: first dict to compare
            :return: dict with keys from the first dict and boolean values
    """

    result = dict()
    for key in dict_second.keys():
        if dict_first[key] and dict_first[key] == dict_second[key]:
            result[key] = True
        else:
            result[key] = False
    return result


class Check:
    pass
