
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt

project = Path(__file__).resolve().parent
images = project / "screenshots"
output = project / "Module9_SQL_Report.docx"

items = [
    ("SQL code 1.png", "Create Users Table",
     "Created the users table with a primary key and unique username and email fields."),
    ("SQL code2.png", "Create Calculations Table",
     "Created the calculations table with a foreign key connecting calculations to users."),
    ("SQL 3.png", "Insert Users",
     "Inserted two sample users, Alice and Bob."),
    ("SQL 4.png", "Insert Calculations",
     "Inserted three calculations associated with the correct users."),
    ("SQL code 5.png", "Select Users",
     "Retrieved all records from the users table."),
    ("SQL CODE 6.png", "Select Calculations",
     "Retrieved all three calculations from the database."),
    ("SQL code 7.png", "JOIN Tables",
     "Combined the users and calculations tables to display usernames with their calculations."),
    ("SQL code 8.png", "Update Record",
     "Updated the result of calculation ID 1 from 5 to 6."),
    ("SQL CODE 9.png", "Delete Record",
     "Deleted calculation ID 2 from the database."),
    ("Docker.png", "Docker Compose Services",
     "Verified that FastAPI, PostgreSQL, and pgAdmin containers were running successfully."),
]

missing = [name for name, _, _ in items if not (images / name).is_file()]
if missing:
    raise SystemExit("Missing screenshots: " + ", ".join(missing))

doc = Document()
section = doc.sections[0]
section.header_distance = Inches(0.4)

normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10)

doc.add_heading("Module 9: SQL Operations Report", 0)
doc.add_paragraph(
    "FastAPI Calculator | PostgreSQL | pgAdmin | Docker Compose"
)
doc.add_paragraph(
    "This report documents the SQL operations performed in pgAdmin "
    "and verifies that the three Docker Compose services were running."
)

for number, (filename, heading, explanation) in enumerate(items, 1):
    doc.add_page_break()
    doc.add_heading(f"{number}. {heading}", level=1)
    doc.add_paragraph(explanation)
    doc.add_picture(str(images / filename), width=Inches(6.2))
    doc.add_paragraph(f"Figure {number}: {heading}")

doc.save(output)
print(f"Report created: {output}")
