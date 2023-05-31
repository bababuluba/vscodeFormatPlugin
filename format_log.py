import sys
import json
import re

def extract_json_from_log(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()

    json_parts = re.findall(r'\{(?:[^{}]|(?R))*\}', log_contents, re.DOTALL)
    extracted_json = []

    for json_part in json_parts:
        try:
            json_obj = json.loads(json_part)
            extracted_json.append(json_obj)
        except json.JSONDecodeError:
            # Ignore invalid JSON parts
            pass
    print(extracted_json)
    return extracted_json

def reformat_json_parts(json_parts):
    reformatted_json = []

    for json_obj in json_parts:
        reformatted_json.append(json.dumps(json_obj, indent=4))
    print(reformatted_json)
    return reformatted_json

def update_log_file(log_file_path, reformatted_json):
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()

    json_parts = re.findall(r'\{(?:[^{}]|(?R))*\}', log_contents, re.DOTALL)
    updated_log_contents = log_contents

    for i, json_part in enumerate(json_parts):
        if i < len(reformatted_json):
            updated_log_contents = updated_log_contents.replace(json_part, reformatted_json[i], 1)

    with open(log_file_path, 'w') as log_file:
        log_file.write(updated_log_contents)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python log_formatter.py <log_file_path>')
    else:
        log_file_path = sys.argv[1]
        extracted_json = extract_json_from_log(log_file_path)
        reformatted_json = reformat_json_parts(extracted_json)
        update_log_file(log_file_path, reformatted_json)
        print('Log file updated successfully.')
