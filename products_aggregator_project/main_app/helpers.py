import datetime as dt
from uuid import UUID


def is_valid_datetime(value: str) -> bool:
    try:
        dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z')
        return True
    except Exception as e:
        return False


def rearrange_data(bad_data):
    data = []
    for node in bad_data:
        fields_node = node["fields"]
        new_node = {"id": node["pk"],
                    "parent_id": fields_node["parent_id"],
                    "name": fields_node["name"],
                    "price": fields_node["price"],
                    "updated_dt": fields_node["updated_dt"],
                    "type": fields_node["type"],
                    "children": None if fields_node["type"] == "OFFER" else []
                    }
        data.append(new_node)
    return data


def create_get_node_result(nodes: list[dict], root_node_id: UUID) -> dict:
    id_to_node = dict()
    for node in nodes:
        id_to_node[node["id"]] = node

    for node in id_to_node.values():
        if node["id"] == str(root_node_id):
            continue

        parent_node = id_to_node[node["parent_id"]] if node["parent_id"] else None
        parent_node["children"].append(node)

    root_node = id_to_node[str(root_node_id)]
    calculate_price_date(root_node)

    return root_node


def calculate_price_date(node: dict) -> tuple[int, int, str]:
    if node["type"] == "OFFER":
        return node["price"], 1, node["updated_dt"]

    total_price = 0
    total_count = 0
    max_date = node["updated_dt"]
    for child in node["children"]:
        price, count, date = calculate_price_date(child)
        total_price += price
        total_count += count
        max_date = max(max_date, date)

    node["price"] = total_price // total_count if total_count > 0 else None
    node["updated_dt"] = max_date
    return total_price, total_count, max_date