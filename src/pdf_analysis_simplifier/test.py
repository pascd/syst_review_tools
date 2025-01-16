import sys, os

# Dynamically add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.pdf_analysis_simplifier.pdf_to_excel import PDFToExcelProcessor
from src.pdf_analysis_simplifier.review_data_parser import ReviewDataParser
from src.pdf_analysis_simplifier.excel_data_parser import ExcelDataParser

if __name__ == '__main__':
    review_parser = ReviewDataParser(config="./review_data.yaml")
    excel_parser = ExcelDataParser(excel_file_path="/home/pedrodias/Documents/git-repos/syst_review_tools/src/pdf_analysis_simplifier/excel-files/analysis_excel_file.xlsx")

    response = """
    "QE1: The methodology (Constrained Decomposition Grid - CDG) is adequately tailored to the challenges of disassembly tasks, addressing task sequencing and destructive vs. non-destructive methods effectively."
    "QE1 Score: 1.0"
    
    "QE2: The robotic cell setup and components are described conceptually but lack detailed descriptions of individual hardware components, focusing more on algorithms and simulation results."
    "QE2 Score: 1.0"
    
    "QE3: Discussions and conclusions are thorough, supported by metrics such as IGD, hypervolume, and epsilon metrics, showcasing the CDG's superiority."
    "QE3 Score: 1.0"
    
    "QE4: The research is primarily simulation-based, which is clearly stated in the methodology and experimental results sections."
    "QE4 Score: 1.0"
    
    "QE5: No mention is made of publicly available implementation or data used in the study."
    "QE5 Score: 0.0"
    
    "QE6: The proposed solution is explicitly focused on disassembly tasks, addressing disassembly line balancing and destructive/non-destructive operations."
    "QE6 Score: 1.0"
    
    "QE7: Comparative results with other methods (MOEA/D and NSGAII) are presented to validate findings."
    "QE7 Score: 1.0"
    
    "QE8: The paper provides a moderately updated review of the state of the art in disassembly line balancing, referencing recent advancements in the field."
    "QE8 Score: 0.5"
    
    "Total Score:"
    "#score: 6.5"
    
    "Data Extraction:"
    "Author: SiQi Lei et al."
    "Year: 2021"
    "Number of Manipulators: Not specified; uses general 'robots' at workstations."
    "Manipulator: Not described in detail."
    "Automated Cell Components: Focuses on robotic workstations and algorithms (CDG implementation)."
    "Vision System: Not mentioned."
    "Use of CAD Model: Not specified."
    "Level of Implementation: Simulation."
    "Level of Automation: Fully automated."
    "Process Steps: Destructive and non-destructive disassembly tasks."
    "Efficiency Considerations: Cost and time optimization."
    "Optimization of Disassembly Task: Task sequencing and resource allocation."
    "Challenges: Balancing workload, handling destructive/non-destructive decisions, and precedence constraints."
    "How To: Uses CDG with crossover and mutation operators to optimize task sequencing under constraints."
    "Results: Demonstrates CDG's superior convergence and solution quality compared to MOEA/D and NSGAII."
    """

    qa_sheet_name = "qa_sheet"
    de_sheet_name = "de_sheet"
    cutoff_score = 6.5

    # Initialize the Excel sheets
    excel_parser.create_excel_file()
    qa_fields = review_parser.get_all_quality_assessment_fields()
    qa_identifiers = []
    for qa in qa_fields:
        qa_identifiers.append(f"{qa["id"]}")
        qa_identifiers.append(f"{qa["id"]} Score")

    #qa_identifiers = [qa["id"] for qa in qa_fields]
    excel_parser.apply_excel_template(qa_sheet_name, qa_identifiers + ["Total Score"])
    data_extraction_fields = review_parser.get_all_data_extraction_fields()

    de_identifiers = [de["key"] for de in data_extraction_fields]
    excel_parser.apply_excel_template(de_sheet_name, de_identifiers)
    print(de_identifiers)

    # Extract QA data and calculate average score
    qa_data = review_parser.get_quality_assessment_text(response)
    paper_score = qa_data.pop("Total Score", 0)
    if qa_data:
        print(qa_data)
        excel_parser.fill_excel_with_data(qa_sheet_name, {**qa_data, "Total Score": paper_score})
        print(f"Total QA Score: {paper_score}")
    else:
        print(f"No QA data found for response")

    # Extract and write DE data only if the score meets the cutoff
    if paper_score and paper_score >= cutoff_score:
        print(f"Paper score ({paper_score}) meets the cutoff ({cutoff_score}). Extracting DE data...")
        de_data = review_parser.get_data_extraction_text(response)
        if de_data:
            excel_parser.fill_excel_with_data(de_sheet_name, de_data)
        else:
            print(f"No DE data found for response.")
