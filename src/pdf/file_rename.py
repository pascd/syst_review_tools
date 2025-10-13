import os
import re
import csv
from pathlib import Path
try:
    import PyPDF2
    PDF_EXTRACTION_AVAILABLE = True
except ImportError:
    PDF_EXTRACTION_AVAILABLE = False

def clean_title(title):
    """Clean and format extracted title"""
    if not title:
        return "Title not found"
    
    # Remove extra whitespace and newlines
    title = re.sub(r'\s+', ' ', title.strip())
    
    # Remove common PDF artifacts
    title = re.sub(r'^(.*?)(doi:|DOI:|http)', r'\1', title, flags=re.IGNORECASE)
    title = re.sub(r'^\d+\s*', '', title)  # Remove leading numbers
    
    # Limit length
    if len(title) > 100:
        title = title[:100] + "..."
    
    return title

def extract_title_from_pdf(pdf_path):
    """Extract title from PDF using multiple methods"""
    if not PDF_EXTRACTION_AVAILABLE:
        return "PyPDF2 not available - install with: pip install PyPDF2"
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Method 1: Try to get title from metadata
            if pdf_reader.metadata and pdf_reader.metadata.get('/Title'):
                title = pdf_reader.metadata['/Title']
                if title and len(title.strip()) > 3:
                    return clean_title(title)
            
            # Method 2: Extract from first page
            if len(pdf_reader.pages) > 0:
                first_page = pdf_reader.pages[0]
                text = first_page.extract_text()
                
                if text:
                    lines = text.split('\n')
                    # Look for title in first few lines
                    for line in lines[:10]:
                        line = line.strip()
                        if len(line) > 10 and len(line) < 200:
                            # Skip common header elements
                            skip_patterns = [
                                r'^\d+$',  # Just numbers
                                r'^page \d+',  # Page numbers
                                r'^www\.',  # URLs
                                r'^http',   # URLs
                                r'^\w+@\w+', # Emails
                            ]
                            
                            should_skip = any(re.match(pattern, line, re.IGNORECASE) 
                                            for pattern in skip_patterns)
                            
                            if not should_skip:
                                return clean_title(line)
            
            return "Could not extract title"
            
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def rename_pdfs_in_directory(directory_path, dry_run=True):
    """
    Rename all PDF files in directory to paper_1.pdf, paper_2.pdf, etc.
    
    Args:
        directory_path (str): Path to directory containing PDFs
        dry_run (bool): If True, only show what would be renamed without actually renaming
    
    Returns:
        list: List of dictionaries with old names, new names, and titles
    """
    
    directory = Path(directory_path)
    if not directory.exists():
        print(f"Directory {directory_path} does not exist!")
        return []
    
    # Get all PDF files
    pdf_files = [f for f in directory.glob("*.pdf") if f.is_file()]
    
    if not pdf_files:
        print("No PDF files found in the directory!")
        return []
    
    # Sort files by name for consistent ordering
    pdf_files.sort(key=lambda x: x.name.lower())
    
    results = []
    
    print(f"Found {len(pdf_files)} PDF files")
    print(f"{'DRY RUN - ' if dry_run else ''}Processing files...\n")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        new_name = f"paper_{i}.pdf"
        new_path = directory / new_name
        
        # Extract title
        print(f"Processing {pdf_file.name}...")
        title = extract_title_from_pdf(pdf_file) if PDF_EXTRACTION_AVAILABLE else "Install PyPDF2 to extract titles"
        
        result = {
            'original_name': pdf_file.name,
            'new_name': new_name,
            'title': title,
            'success': True
        }
        
        # Check if target file already exists
        if new_path.exists() and new_path != pdf_file:
            result['success'] = False
            result['error'] = f"Target file {new_name} already exists"
            print(f"  ⚠️  Cannot rename: {new_name} already exists")
        else:
            if not dry_run:
                try:
                    pdf_file.rename(new_path)
                    print(f"  ✅ Renamed to: {new_name}")
                except Exception as e:
                    result['success'] = False
                    result['error'] = str(e)
                    print(f"  ❌ Error: {str(e)}")
            else:
                print(f"  📋 Would rename to: {new_name}")
        
        print(f"  📄 Title: {title}\n")
        results.append(result)
    
    return results

def save_title_mapping(results, output_file="paper_titles.csv"):
    """Save the mapping of paper names to titles in a CSV file"""
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['paper_number', 'filename', 'title', 'original_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for i, result in enumerate(results, 1):
            if result['success']:
                writer.writerow({
                    'paper_number': i,
                    'filename': result['new_name'],
                    'title': result['title'],
                    'original_name': result['original_name']
                })
    
    print(f"Title mapping saved to: {output_file}")

# Main execution
if __name__ == "__main__":
    # Configuration
    DIRECTORY_PATH = "/home/pedro/Downloads/part4-analysis/analysed/Checked"  # Current directory - change this to your PDF folder path
    DRY_RUN = False  # Set to False to actually rename files
    
    print("PDF File Renamer with Title Extraction")
    print("=" * 50)
    
    if not PDF_EXTRACTION_AVAILABLE:
        print("⚠️  PyPDF2 not found. Install it with: pip install PyPDF2")
        print("   Title extraction will be limited without this library.\n")
    
    print(f"Directory: {DIRECTORY_PATH}")
    print(f"Mode: {'DRY RUN (preview only)' if DRY_RUN else 'ACTUAL RENAMING'}")
    print()
    
    # Process files
    results = rename_pdfs_in_directory(DIRECTORY_PATH, dry_run=DRY_RUN)
    
    if results:
        # Save title mapping
        save_title_mapping(results)
        
        # Summary
        successful = len([r for r in results if r['success']])
        print(f"\nSummary:")
        print(f"  Total files processed: {len(results)}")
        print(f"  {'Would be renamed' if DRY_RUN else 'Successfully renamed'}: {successful}")
        print(f"  Failed: {len(results) - successful}")
        
        if DRY_RUN:
            print(f"\n🔄 To actually rename files, change DRY_RUN to False and run again.")
    
    print("\nDone!")