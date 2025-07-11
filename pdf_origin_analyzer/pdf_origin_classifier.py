import os
import csv
from PyPDF2 import PdfReader
# Correct import for PdfReadError in PyPDF2 3.x
from PyPDF2.errors import PdfReadError

# Ask user for folder path
folder_path = input("Enter the folder path containing PDF files: ").strip('"')

# Prepare output CSV
output_csv = os.path.join(folder_path, "pdf_origin_report.csv")

# Function to determine PDF type
def classify_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text_found = False
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                text_found = True
                break
        if text_found:
            return "Born-digital (text-based)"
        else:
            return "Scanned (image-based)"
    except (PdfReadError, Exception) as e:
        return f"Error: {str(e)}"

# Collect results
results = []

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        result = classify_pdf(pdf_path)
        print(f"{filename}: {result}")
        results.append([filename, result])

# Save to CSV
with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Type"])
    writer.writerows(results)

print(f"\nResults saved to {output_csv}") 