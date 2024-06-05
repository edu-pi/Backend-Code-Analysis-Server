import json
from dataclasses import asdict


def nodes_to_json(nodes):
    # Node 객체 리스트를 사전 목록으로 변환
    nodes_dict_list = [asdict(node) for node in nodes]

    # 사전 목록을 JSON 형식 문자열로 변환
    return json.dumps(nodes_dict_list, indent=4)
