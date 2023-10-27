"""
do not wash your kitty too often
"""
import hashlib
import os
import glob
import json
from kitty_ast.wrappedParser import parse_file_to_ast


def filter_files_by_sources_json(folder_path):
    """Filter files based on sources.json content."""
    sources_json_path = os.path.join(folder_path, 'sources.json')
    if not os.path.exists(sources_json_path):
        return [f for f in glob.glob(os.path.join(folder_path, '*.sol')) if os.path.isfile(f)]

    with open(sources_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        prefixes = [item['prefix'] for item in data if item.get('selected', False)]

    sol_files = [f for f in glob.glob(os.path.join(folder_path, '*.sol'))
                 if any(prefix in f for prefix in prefixes)]

    return sol_files


def get_solidity_files(path: str):
    all_files = []
    for root, dirs, files in os.walk(path):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in ['lib', 'scripts', 'node_modules', 'mocks', 'test', ".deps"]]

        # Add .sol files from the current directory that match conditions in sources.json
        all_files.extend(filter_files_by_sources_json(root))

    return all_files


def get(node, key):
    if key in node.keys():
        if node.get(key) is None:
            return " "
        return " " + node.get(key)
    else:
        return " "


def kitty_hash(s):
    return hashlib.md5(s.encode()).hexdigest()[:8]


def wash(node):
    if node is None:
        return ""
    node_type = node.get("type", "")
    result = ""
    # 特定节点类型的特定属性
    if node_type == "SourceUnit":
        result += ""
    elif node_type == "ImportDirective":
        result += f"{kitty_hash(get(node,'path'))}\n"
    elif node_type == "PragmaDirective":
        result += f"{node['value']}\n"
    elif node_type == "ContractDefinition":
        result += f"{node['name']}\n"
    elif node_type == "InterfaceDefinition":
        result += f"{node['name']}\n"
    elif node_type == "FunctionDefinition":
        result += f"{node['name']}\n"
    elif node_type == "VariableDeclaration":
        result += f"{node['name']}\n"
    elif node_type == "StateVariableDeclaration":
        for child_node in node["variables"]:
            result += wash(child_node)
        result += wash(node["initialValue"])
    elif node_type == "EventDefinition":
        result += f"{node['name']}\n"
    elif node_type == "ModifierDefinition":
        result += f"{node['name']}\n"
    elif node_type == "ModifierDefinition":
        result += f"{node['name']}\n"
    elif node_type == "CustomErrorDefinition":
        result += f"{node['name']['name']}\n"
    elif node_type == "StructDefinition":
        result += f"{node['name']}\n"
        for child_node in node["members"]:
            result += wash(child_node)
    elif node_type == "FunctionCall":
        result += f"{node['expression']['name']}\n"
        for child_node in node["arguments"]:
            result += wash(child_node)
    # else:
    #     print(node_type)
    # 递归处理子节点
    if "children" in node.keys():
        for child_node in node["children"]:
            result += wash(child_node)
    if "subNodes" in node.keys():
        for child_node in node["subNodes"]:
            result += wash(child_node)
    return result


def wash_kitty(path: str, result_path):
    sol_files = get_solidity_files(path)
    washed_kitty = ""
    for sol in sol_files:
        try:
            ast = parse_file_to_ast(sol)
            washed_kitty += wash(ast)
        except:
            continue
    f = open(result_path, "w")
    f.write(washed_kitty)
    f.close()


if __name__ == "__main__":
    project = "/Users/cong.zhang/dev/autobuild/tests/testcases/2023-08-chainlink"
    result_path = "./result.txt"
    wash_kitty(project, result_path)

