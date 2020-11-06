from data_structure.data_store import DataValue

KEY_PATH_DELIMITER = '.'


def get_related_data(data, date_path, target_key, same_path):
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]
        for key, value in data.items():
            if not isinstance(key, int):
                if date_path:
                    result = get_related_data(value, date_path[1:], target_key, same_path and date_path[0] == key)
                else:
                    result = get_related_data(value, [], target_key, False)
                if result:
                    return result
    elif isinstance(data, list):
        if not same_path:
            return None
        return get_related_data(data[date_path[0]], date_path[1:], target_key, same_path)
    else:
        raise Exception('error')


def special_rule_1(dataTree, key_path, value, group_path, data, date_path):
    related_data = get_related_data(data, date_path, 30131, True)
    if related_data:
        related_value = DataValue(related_data, value.priority)
        dataTree.set_value(key_path.rpartition(KEY_PATH_DELIMITER)[0] + '.zhyl90001', related_value, group_path)

    related_data_2 = get_related_data(data, date_path, 30182, True)
    if related_data_2:
        related_value = DataValue(related_data_2, value.priority)
        dataTree.set_value(key_path.rpartition(KEY_PATH_DELIMITER)[0] + '.zhyl90004', related_value, group_path)
    dataTree.set_value(key_path, value, group_path)
