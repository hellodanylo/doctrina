def implode_tree(tree: dict, separator: str) -> dict:
    imploded_tree = {}

    for key, value in tree.items():
        if type(value) != dict:
            imploded_tree[key] = value
            continue

        imploded_value = implode_tree(value, separator)
        imploded_value = {
            key + separator + subkey: subvalue
            for subkey, subvalue in imploded_value.items()
        }

        imploded_tree.update(imploded_value)

    return imploded_tree


def explode_tree(flat_tree: dict, separator: str) -> dict:
    part_tree = {tuple(k.split(separator)): v for k, v in flat_tree.items()}
    exploded_tree = dict()

    for (parts, value) in part_tree.items():
        location = exploded_tree
        for part in parts[:-1]:
            if part not in location:
                location[part] = dict()
            location = location[part]

        location[parts[-1]] = value

    return exploded_tree