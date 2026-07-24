import camelot

pdf_path = "docs/Billion-scale similarity search with GPUs.pdf"

print("Trying Stream...\n")

tables = camelot.read_pdf(
    pdf_path,
    pages="all",
    flavor="stream"
)

print(f"Tables found: {tables.n}")

for i, table in enumerate(tables):
    print("\n" + "=" * 80)
    print(f"Table {i+1}")
    print(table.df)