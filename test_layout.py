import fitz
from PIL import Image
from doclayout_yolo import YOLOv10

model = YOLOv10("models/doclayout_yolo_docstructbench_imgsz1024.pt")

pdf = fitz.open("docs/Neural Machine Translation of Rare Words with Subword Units.pdf")      # Use any PDF you already have

page = pdf[0]

pix = page.get_pixmap(dpi=200)

img = Image.frombytes(
    "RGB",
    [pix.width, pix.height],
    pix.samples
)

results = model.predict(img)

print(results)