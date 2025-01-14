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
    def get_all_quality_assessment_fields(self):
        # Load data parameters into a variable
        data = self.load_yaml_file()

        # If the file is empty, return None
        if data is None:
            print("Error when loading yaml file")
            return False
        else:
            qa_questions = data["quality_assessment_questions"]
            return [{"id": q["id"], "question": q["question"], "scores": q["scores"]} for q in qa_questions]

    # Get all data extraction fields
    def get_all_data_extraction_fields(self):
        # Load data parameters into a variable
        data = self.load_yaml_file()

        # If the file is empty, return None
        if data is None:
            print("Error when loading yaml file")
            return False
        else:
            de_fields = data["data_extraction_fields"]
            return [{"key": data["key"], "description": data["description"]} for data in de_fields]

    # Retrieve the cutoff score from config file
    def get_cutoff_score(self):
        data = self.load_yaml_file()

        if data is None:
            print("Error when loading yaml file")
            return False
        else:
            return data["cutoff_score"]

    # Return prompt for quality assessment type: "qa" or "de"
    def get_analysis_prompt(self):
        prompt = ""
        prompt += "Hello ChatGPT, imagine you are a researcher, I want you to perform a systematic analysis on the following PDF. Please be concise and exact, following the next parameters. \n"

        # Retrieve all analysis fields
        qa_fields = self.get_all_quality_assessment_fields()
        data_extraction_fields = self.get_all_data_extraction_fields()
        cutoff_score = self.get_cutoff_score()

        prompt += "The quality assessment questions and scores are: \n"

        if not qa_fields:
            print("No questions found")
            return False

        for qa_field in qa_fields:
            # Convert the scores list to a string
            scores_str = ", ".join(map(str, qa_field["scores"]))
            prompt += qa_field["id"] + "\n" + qa_field["question"] + "\n" + scores_str + "\n\n"

        prompt += "And the respective data extraction fields below:\n\n"

        if not data_extraction_fields:
            print("No data extraction fields found")
            return False

        for data_field in data_extraction_fields:
            prompt += data_field["key"] + ": " + data_field["description"] + "\n"

        prompt += (
            f"In your answers, just include the ID of the quality assessment questions, a brief explanation of it, and the score, something like this: \n"
            "QE1: brief explanation \n"
            "QE1 Score: score \n\n"
            f"For data extraction fields, if the sum of the scores is equal to or higher than the cutoff score, which is equal to {cutoff_score}, give me an answer like this: \n"
            f"data_field_1: brief explanation \n"
            "data_field_2: brief explanation \n\n"
            "Please also return the score for the paper in the following format: \n"
            "#score: score \n"
            "and so on. Thank you for your help."
        )

        # Replace newlines with spaces or another delimiter
        prompt = prompt.replace("\n", " ")

        return prompt