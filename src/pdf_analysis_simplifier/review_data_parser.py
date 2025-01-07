import os
import yaml

# Load YAML file
def load_yaml_file(_yaml_file_path):
    try:
        with open(_yaml_file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as _exc:
        print("Error when loading yaml file: {}".format(_exc))
        return None

# Save data to the YAML file
def save_yaml_file(_yaml_file_path, _data):
    try:
        with open(_yaml_file_path, 'w') as stream:
            yaml.dump(_data, stream)
            return True
    except yaml.YAMLError as _exc:
        print("Error when saving yaml file: {}".format(_exc))
        return False

# Get all questions for quality assessment
def get_all_questions(_yaml_file):
    # Load data parameters into a variable
    _data = load_yaml_file(_yaml_file)
    # If the file is empty, return None
    if _data is None:
        return None
    else:
        _qa_questions = _data["quality_assessment_questions"]
        return [_qa_questions["id"],_qa_questions["question"],_qa_questions["scores"]]

# Get all data extraction fields
def get_all_data_extraction_fields(_yaml_file):
    # Load data parameters into a variable
    _data = load_yaml_file(_yaml_file)
    # If the file is empty, return None
    if _data is None:
        return None
    else:
        return _data["data_extraction_fields"]