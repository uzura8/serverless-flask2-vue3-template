def get_striped(vals, key,  def_val=''):
    val = vals.get(key, '').strip()
    if len(val) == 0:
        val = def_val
    return val


def keys_from_dicts(dicts, key):
    tmp = {}
    for i in dicts:
        k = i[key]
        tmp[k] = 1
    return list(tmp.keys())


def conv_flat_dict_to_nested(original_dict, delimiter='.'):
    new_dict = {}
    for k, v in original_dict.items():
        parts = k.split(delimiter)
        if len(parts) > 1:
            if parts[0] not in new_dict:
                new_dict[parts[0]] = {}
            new_dict[parts[0]][parts[1]] = v
        else:
            new_dict[k] = v
    return new_dict
