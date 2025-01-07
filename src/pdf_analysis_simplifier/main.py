import os
import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load GPT-J model and tokenizer from Hugging Face
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to chunk text for token limit (2048 tokens max)
def chunk_text(text, chunk_size=2048):
    # Split the document text into smaller chunks to fit within the model's token limit
    tokens = tokenizer.encode(text)
    for i in range(0, len(tokens), chunk_size):
        yield tokenizer.decode(tokens[i:i + chunk_size])

# Function to interact with GPT-J based on document content
def chat_with_document(pdf_path, user_message):
    # Extract text from the PDF
    document_text = extract_pdf_text(pdf_path)

    # Chunk the document text if it's too long
    document_chunks = list(chunk_text(document_text))

    # Process each chunk and get the response
    full_answer = ""
    for chunk in document_chunks:
        prompt = f"Document: {chunk}\nUser: {user_message}\nAssistant:"

        # Tokenize and make sure to reset position indices by truncating the input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

        # Ensure position indices are within the allowed range by resetting for each chunk
        input_ids = inputs["input_ids"]
        position_ids = torch.arange(input_ids.size(1), device=input_ids.device).unsqueeze(0)
        inputs["position_ids"] = position_ids

        # Generate the model's response
        outputs = model.generate(**inputs, max_new_tokens=512, num_return_sequences=1, temperature=0.7)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        full_answer += response.split("Assistant:")[-1].strip() + " "

    return full_answer.strip()

# Function to process all PDF files in a folder
def process_pdfs_in_folder(folder_path, user_message):
    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    # Process each PDF file
    for pdf_filename in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_filename)
        print(f"\nProcessing file: {pdf_filename}")

        # Ask the question and get the answer for each file
        answer = chat_with_document(pdf_path, user_message)
        print(f"Answer for {pdf_filename}: {answer}")

# Example usage
folder_path = "./pdf-files/"  # Specify the folder where PDFs are stored
user_message = "What are the main conclusions of this document?"  # The user's question

# Process all PDFs in the folder
process_pdfs_in_folder(folder_path, user_message)
