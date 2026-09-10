import argparse
import os
import sys
from pypdf import PdfReader


def select_folder_gui():
    """Open a graphical dialog to select a folder, falling back to CLI prompt if GUI fails."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        return filedialog.askdirectory(title="Select Folder with PDF Files")
    except Exception:
        return input("Enter path to folder containing PDF files: ").strip()


def pdf_to_markdown(pdf_path, md_path):
    """Extract text from a PDF file and save it as a Markdown file."""
    reader = PdfReader(pdf_path)
    markdown_content = []

    file_title = os.path.basename(pdf_path)
    markdown_content.append(f"# {file_title}\n")

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            markdown_content.append(f"## Page {i}\n")
            cleaned_text = text.replace("\r\n", "\n").strip()
            markdown_content.append(f"{cleaned_text}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))


def convert_folder_pdfs_to_md(input_folder=None, output_folder=None):
    folder_path = input_folder or select_folder_gui()

    if not folder_path or not os.path.exists(folder_path):
        print("No valid folder selected. Operation canceled.")
        return

    out_path = output_folder or folder_path
    os.makedirs(out_path, exist_ok=True)

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Starting conversion...\n")

    success_count = 0
    for file_name in pdf_files:
        pdf_path = os.path.join(folder_path, file_name)
        md_file_name = os.path.splitext(file_name)[0] + ".md"
        md_path = os.path.join(out_path, md_file_name)

        try:
            pdf_to_markdown(pdf_path, md_path)
            print(f"[SUCCESS] Converted: {file_name} -> {md_file_name}")
            success_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to convert {file_name}: {e}")

    print(f"\nConversion complete! Successfully converted {success_count}/{len(pdf_files)} files.")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert PDF files in a directory to Markdown format."
    )
    parser.add_argument(
        "-i", "--input",
        help="Path to directory containing PDFs. Opens folder selector dialog if omitted."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output directory for Markdown files. Defaults to input directory."
    )
    args = parser.parse_args()

    convert_folder_pdfs_to_md(input_folder=args.input, output_folder=args.output)


if __name__ == "__main__":
    main()