import json
from dataclasses import asdict


def nodes_to_json(nodes):
    # Node 객체 리스트를 사전 목록으로 변환
    nodes_dict_list = [asdict(node) for node in nodes]

    # 사전 목록을 JSON 형식 문자열로 변환
    return json.dumps(nodes_dict_list, indent=4)


def convert_to_json(data):
    def convert_item(item):
        if isinstance(item, list):
            return [convert_item(sub_item) for sub_item in item]
        elif isinstance(item, dict):
            return {key: convert_item(value) for key, value in item.items()}
        else:
            return item.__dict__ if hasattr(item, '__dict__') else item

    return json.dumps(convert_item(data), default=str, indent=2)