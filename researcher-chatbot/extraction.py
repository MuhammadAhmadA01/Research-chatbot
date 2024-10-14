import os
from pdfminer.high_level import extract_text
import re
import nltk
# Function to extract paragraphs directly from PDF files
def extract_paragraphs_from_pdf(pdf_path):
    paragraphs = []
    try:
        text = extract_text(pdf_path)
        # Split by empty lines to get paragraphs
        paragraphs = text.split("\n\n")
    except Exception as e:
        print(f"Error extracting paragraphs from {pdf_path}: {e}")
    return paragraphs

def filter_paragraphs(paragraphs):
    filtered_paragraphs = []
    for paragraph in paragraphs:
        # Remove references like [number], figure [number], fig [number], etc.
        cleaned_paragraph = re.sub(r'\[\d+\]|\bfig(?:ure)?\s\d+', '', paragraph, flags=re.IGNORECASE)
        # Tokenize the cleaned paragraph into sentences
        sentences = nltk.sent_tokenize(cleaned_paragraph)
        # Check if the paragraph has more than 3 sentences
        filtered_paragraphs.append(cleaned_paragraph.strip())
    return filtered_paragraphs

if __name__ == "__main__":
    # Directory to save downloaded PDFs
    save_directory = "papers"
    # Output text file path
    output_file = "uncleaned.txt"
    # Read paragraphs directly from PDFs
    with open(output_file, 'w', encoding='utf-8') as f:
        for pdf_file in os.listdir(save_directory):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(save_directory, pdf_file)
                paragraphs = extract_paragraphs_from_pdf(pdf_path)
                filtered_paragraphs = filter_paragraphs(paragraphs)
                for paragraph in filtered_paragraphs:
                    f.write(paragraph.strip() + '\n')  # Write each paragraph to file with an empty line after

    print(f"All paragraphs references removed have been written to {output_file}")