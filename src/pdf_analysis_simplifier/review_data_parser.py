import os
import yaml

class ReviewDataParser:

    def __init__(self, config):
        self.config = config

    # Load YAML file
    def load_yaml_file(self):
        try:
            with open(self.config, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as _exc:
            print("Error when loading yaml file: {}".format(_exc))
            return None

    # Save data to the YAML file
    def save_yaml_file(self, data):
        try:
            with open(self.config, 'w') as stream:
                yaml.dump(data, stream)
                return True
        except yaml.YAMLError as _exc:
            print("Error when saving yaml file: {}".format(_exc))
            return False

    # Get all questions for quality assessment
    def get_all_questions(self):
        # Load data parameters into a variable
        data = self.load_yaml_file()

        # If the file is empty, return None
        if data is None:
            return None
        else:
            qa_questions = data["quality_assessment_questions"]
            return [qa_questions["id"],qa_questions["question"],qa_questions["scores"]]

    # Get all data extraction fields
    def get_all_data_extraction_fields(self):
        # Load data parameters into a variable
        data = self.load_yaml_file()

        # If the file is empty, return None
        if data is None:
            return None
        else:
            return data["data_extraction_fields"]