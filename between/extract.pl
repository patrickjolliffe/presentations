import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_pdf_content(pdf_path, output_dir):
    """Extract text and images from a PDF file"""
    # Create output directories
    output_dir = Path(output_dir)
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Open PDF
    doc = fitz.open(pdf_path)
    markdown_content = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract text
        text = page.get_text()
        if text.strip():
            markdown_content.append(f"# Slide {page_num + 1}\n\n{text}\n")
        
        # Extract images
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"slide_{page_num + 1}_image_{img_index + 1}.{image_ext}"
            
            with open(images_dir / image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            
            # Add image reference to markdown
            markdown_content.append(f"![{image_filename}](images/{image_filename})\n")
    
    # Write markdown file
    with open(output_dir / "presentation.md", "w", encoding="utf-8") as md_file:
        md_file.write("\n".join(markdown_content))

# Example usage
extract_pdf_content("pres_tanel.pdf", "output_folder")