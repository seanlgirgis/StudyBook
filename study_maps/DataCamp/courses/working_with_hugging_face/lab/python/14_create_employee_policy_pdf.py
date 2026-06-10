from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

output = Path(__file__).with_name("US_Employee_Policy.pdf")

pages = [
    [
        "US Employee Policy",
        "",
        "Resignation Policy",
        "Employees who choose to resign must provide two weeks written notice.",
        "The notice should be submitted to the employee's manager and Human Resources.",
    ],
    [
        "Leave Policy",
        "",
        "Eligible employees receive paid vacation according to tenure and company policy.",
        "Requests should be submitted in advance whenever possible.",
    ],
]

pdf = canvas.Canvas(str(output), pagesize=LETTER)
width, height = LETTER

for page_lines in pages:
    y = height - 72
    for line in page_lines:
        pdf.drawString(72, y, line)
        y -= 22
    pdf.showPage()

pdf.save()
print(f"Created: {output}")
