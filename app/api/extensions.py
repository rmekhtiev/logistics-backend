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


def wrap(dictionary):
    """
            wraps the income dictionary with 'id' key and 'attributes' key, where 'id' is the dictionaries 'id'
            and the 'attributes' are the other values from the income dictionary
            :param dictionary: second dict to compare
            :return: dictionary with new keys 'id' and 'attributes'
    """
    newDict = {}
    keys = dictionary.getkeys()

    if 'id' not in keys:
        return dictionary
    else:
        keys.remove('id')
    # todo добавить кэтч для ключа id

    newDict['id'] = dictionary['id']
    newDict['attributes'] = {}

    for key in keys:
        newDict['attributes'][key] = dictionary[key]
    return newDict
