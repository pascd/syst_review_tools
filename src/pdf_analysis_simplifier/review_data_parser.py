import os
import yaml
import re
from src.pdf_analysis_simplifier.response_handler import ResponseHandler

class ReviewDataParser:

    def __init__(self, config):
        self.config = config
        self.response_handler = ResponseHandler()

    def load_yaml_file(self):
        try:
            with open(self.config, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            return None

    def save_yaml_file(self, data):
        try:
            with open(self.config, 'w') as stream:
                yaml.dump(data, stream)
                return True
        except yaml.YAMLError as exc:
            print(f"Error saving YAML file: {exc}")
            return False

    def get_all_quality_assessment_fields(self):
        data = self.load_yaml_file()
        if not data or "quality_assessment_questions" not in data:
            print("Invalid or missing quality assessment questions.")
            return []
        return [{"id": q["id"], "question": q["question"], "scores": q["scores"]} for q in data["quality_assessment_questions"]]

    def get_all_data_extraction_fields(self):
        data = self.load_yaml_file()
        if not data or "data_extraction_fields" not in data:
            print("Invalid or missing data extraction fields.")
            return []
        return [{"key": field["key"], "description": field["description"]} for field in data["data_extraction_fields"]]

    def get_cutoff_score(self):
        data = self.load_yaml_file()
        return data.get("cutoff_score", 0)

    def get_analysis_prompt(self):
        qa_fields = self.get_all_quality_assessment_fields()
        de_fields = self.get_all_data_extraction_fields()
        cutoff_score = self.get_cutoff_score()

        if not qa_fields or not de_fields:
            print("Missing required fields for analysis prompt.")
            return ""

        prompt = "Hello, perform a systematic analysis. Parameters:\n"
        prompt += "Quality Assessment Questions:\n"
        for qa in qa_fields:
            prompt += f"{qa['id']} - {qa['question']} (Scores: {', '.join(map(str, qa['scores']))})\n"

        prompt += "Data Extraction Fields:\n"
        for de in de_fields:
            prompt += f"{de['key']}: {de['description']}\n"

        prompt += (f"Cutoff Score: {cutoff_score}.\nFormat your answers as instructed."
                   f"The Quality assessment should be formated like this: \n"
                   f"QE1: Brief description \n"
                   f"QE1 Score: score \n\n"
                   f""
                   f"QE2: Brief description \n"
                   f"QE2 Score: score \n\n"
                   f""
                   f"About Data extraction Fields:\n"
                   f"Author: \n"
                   f"Year: \n"
                   f"Title: \n"
                   f"ẽtc."
                   f"Write everything in different lines, without bullet points, and always using the format I am asking you. Thank you.")
        return prompt

    def preprocess_qa_data(self, qa_data, total_score):
        flattened_data = {}

        for qa_key, qa_info in qa_data.items():
            # Check if qa_info is a dictionary
            if isinstance(qa_info, dict):
                # Add description and score to flattened dictionary
                flattened_data[qa_key] = qa_info.get(qa_key, "")
                flattened_data[f"{qa_key} Score"] = qa_info.get("Score", "")
            else:
                # Handle unexpected cases (e.g., if qa_info is a float or string)
                flattened_data[qa_key] = str(qa_info)
                flattened_data[f"{qa_key} Score"] = ""

        # Add total score
        flattened_data["Total Score"] = total_score

        return flattened_data

    def get_quality_assessment_text(self, response):

        qa_data = {}
        total_score = 0

        qa_pattern = re.compile(r"(QE\d+):\s*(.*?)\s*QE\d+\s*Score:\s*([0-9.]+)", re.DOTALL)
        matches = qa_pattern.findall(response)

        for match in matches:
            question_id, description, score = match
            score = float(score.strip())
            qa_data[question_id] = {
                f"{question_id}": description.strip().replace('"', ""),
                "Score": score
            }
            total_score += score

        # Add total and average scores
        qa_data["Total Score"] = total_score

        return self.preprocess_qa_data(qa_data, total_score)


    def get_data_extraction_text(self, response):

        de_data = {}
        de_section_pattern = re.compile(r"Data Extraction:\s*(.*?)\Z", re.DOTALL)
        de_section_match = de_section_pattern.search(response)
        if not de_section_match:
            return de_data

        de_content = de_section_match.group(1)
        de_lines = de_content.splitlines()

        for line in de_lines:
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                # Remove double quotes from both key and value
                key = key.replace('"', "")
                value = value.replace('"', "")
                de_data[key] = value

        return de_data
