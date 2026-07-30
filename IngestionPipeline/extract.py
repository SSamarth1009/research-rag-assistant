import os
import fitz
import pdfplumber
from PIL import Image
from docx import Document
from doclayout_yolo import YOLOv10


#Adding Model for Layout Detection
LAYOUT_MODEL = YOLOv10("../models/doclayout_yolo_docstructbench_imgsz1024.pt")

###########################################################################
#---------------------Helper Functions-----------------------------
###########################################################################

def create_document(document_name: str, file_type: str):
    return {
        "metadata": {
            "document_name": document_name,
            "file_type": file_type,
            "page_count": 0,
        },
        "pages": []
    }


def create_knowledge_object(
    object_id: int,
    object_type: str,
    content=None,
    bbox=None,
    metadata=None
):
    """
    Create a standardized knowledge object.

    Every piece of extracted information
    (paragraph, table, figure, caption, etc.)
    should follow this schema.
    """

    return {
        "id": object_id,
        "type": object_type,
        "content": content,
        "bbox": bbox,
        "metadata": metadata or {}
    }


def create_page(page_number: int, text: str = ""):
    """
    Create a standardized page representation.
    """
    page = {
        "page_number": page_number,

        # Existing structures (temporary)cls
        "text_blocks": [],
        "tables": [],
        "figures": [],
        "charts": [],

        # New normalized structure
        "knowledge_objects": [],

        "regions": [],
        "metadata": {}
    }
    if text:
        page["text_blocks"].append({
            "id": 0,
            "type": "paragraph",
            "content": text
        })

        page["knowledge_objects"].append(
        create_knowledge_object(
            object_id=0,
            object_type="paragraph",
            content=text,
            metadata={
                "page_number": page_number
            }
        )
    )

    return page


###########################################################################
#---------------------PDF EXTRACTION FUNCTIONS-----------------------------
###########################################################################

def extract_pdf_tables(page):
    """
    Extract tables from a pdfplumber page while preserving structure.
    """
    tables = []

    extracted_tables = page.extract_tables()

    for table_id, table in enumerate(extracted_tables):
        tables.append({
            "id": table_id,
            "rows": table
        })

    return tables

###########################################################################
#---------------------LAYOUT DETECTION FUNCTIONS---------------------------
###########################################################################

def detect_layout(fitz_page):
    """
    Detect document layout regions (paragraphs, tables,
    figures, captions, formulas, etc.)

    Args:
        fitz_page: PyMuPDF page object

    Returns:
        List[dict]: Detected layout regions
    """

    pix = fitz_page.get_pixmap(dpi=200)

    image = Image.frombytes(
        "RGB",
        (pix.width, pix.height),
        pix.samples
    )

    results = LAYOUT_MODEL.predict(image)

    regions = []

    if not results:
        return regions

    result = results[0]

    for box in result.boxes:

        cls_id = int(box.cls)
        label = result.names[cls_id]

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        regions.append({
            "id": len(regions),
            "type": label,
            "bbox": [x1, y1, x2, y2],
            "confidence": float(box.conf)
        })

    return regions

def crop_region(fitz_page, bbox, output_path):
    """
    Crop a layout region from a PDF page using the bounding box returned
    by DocLayout-YOLO.
    """

    # Render the page at the same DPI used for layout detection
    render_pix = fitz_page.get_pixmap(dpi=200)

    image_width = render_pix.width
    image_height = render_pix.height

    pdf_width = fitz_page.rect.width
    pdf_height = fitz_page.rect.height

    scale_x = pdf_width / image_width
    scale_y = pdf_height / image_height

    x1, y1, x2, y2 = bbox
    print(f"PDF Page Size : {fitz_page.rect}")
    print(f"Rendered Size : {image_width} x {image_height}")
    print(f"YOLO BBox     : {bbox}")
    # Convert image coordinates -> PDF coordinates
    rect = fitz.Rect(
        x1 * scale_x,
        y1 * scale_y,
        x2 * scale_x,
        y2 * scale_y,
    )

    # Clip to page boundaries
    rect = rect & fitz_page.rect

    # Skip invalid boxes
    if rect.is_empty or rect.width <= 1 or rect.height <= 1:
        return False

    pix = fitz_page.get_pixmap(
        clip=rect,
        dpi=300
    )

    pix.save(output_path)
    return True

def extract_pdf_figures(fitz_page, document_name, regions):

    figures = []

    document_stem = os.path.splitext(document_name)[0]

    figure_dir = os.path.join(
        "figures",
        document_stem
    )

    os.makedirs(figure_dir, exist_ok=True)

    figure_id = 0

    for region in regions:

        if region["type"] != "figure":
            continue

        image_path = os.path.join(
            figure_dir,
            f"page_{fitz_page.number+1}_figure_{figure_id+1}.png"
        )

        success = crop_region(
                fitz_page,
                region["bbox"],
                image_path
            )
        if not success:
            continue

        figures.append({

            "id": figure_id,

            "page_number": fitz_page.number + 1,

            "image_path": image_path,

            "bbox": region["bbox"],

            "confidence": region["confidence"],

            "caption": None,

            "ocr_text": None,

            "metadata": {}

        })

        figure_id += 1

    return figures


def extract_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    pdf = fitz.open(pdf_path)
    plumber_pdf = pdfplumber.open(pdf_path)
    document_name = os.path.basename(pdf_path)
    document = create_document(document_name, "pdf")

    for page_number, (fitz_page, plumber_page) in enumerate(zip(pdf, plumber_pdf.pages),start=1):
        text = fitz_page.get_text().strip()
        page_data = create_page(page_number, text)

        regions = detect_layout(fitz_page)
        page_data["regions"] = regions
        print(f"\nLayout Regions (Page {page_number})")

        for region in regions:
            print(
                f"{region['type']:<15}"
                f"{region['confidence']:.2f}"
            )

        tables = extract_pdf_tables(plumber_page)
        figures = extract_pdf_figures(fitz_page, document_name, regions)

        page_data["tables"] = tables
        page_data["figures"] = figures

        document["pages"].append(page_data)
        print(
        f"Page {page_number}: "
        f"Text={len(page_data['text_blocks'])}, "
        f"Tables={len(page_data['tables'])}, "
        f"Figures={len(page_data['figures'])}"
        )
        document["metadata"]["page_count"] = pdf.page_count

    pdf.close()
    plumber_pdf.close()

    return document


###########################################################################
#---------------------DOCX EXTRACTION FUNCTIONS-----------------------------
###########################################################################

def extract_docx(docx_path):
    """
    Extract text from a DOCX file.
    """
    doc = Document(docx_path)

    content = "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )

    document = create_document(os.path.basename(docx_path),"docx")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


###########################################################################
#---------------------TXT EXTRACTION FUNCTIONS-----------------------------
###########################################################################

def extract_txt(txt_path):
    """
    Extract text from a TXT file.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    document = create_document(os.path.basename(txt_path),"txt")
    document["pages"].append(create_page(1, content))
    document["metadata"]["page_count"] = 1

    return document


def extract_document(file_path):
    """
    Detect file type and call the appropriate extractor.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)
    elif extension == ".docx":
        return extract_docx(file_path)
    elif extension == ".txt":
        return extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

if __name__ == "__main__":
    docs_folder = "../docs"

    for file in os.listdir(docs_folder):
        file_path = os.path.join(docs_folder, file)
        data = extract_document(file_path)

        print("\n" + "=" * 60)
        print(f"Document : {data['metadata']['document_name']}")
        print(f"Type     : {data['metadata']['file_type']}")
        print(f"Pages    : {data['metadata']['page_count']}")

        if data["pages"]:
            first_page = data["pages"][0]
            print(f"\nPage {first_page['page_number']}")
            if first_page["text_blocks"]:
                print(first_page["text_blocks"][0]["content"][:300])
            else:
                print("<No text found on this page>")
    