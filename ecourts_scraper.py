import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from flask import Flask, render_template_string, request, send_file
import os

app = Flask(__name__)

BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"

def get_cause_list(state_code, district_code, complex_code, court_code, date):
    params = {
        "state_cd": state_code,
        "dist_cd": district_code,
        "court_complex_code": complex_code,
        "court_code": court_code,
        "cause_list_date": date
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Try to extract only the <pre> or actual cause list area
    cause_list_section = soup.find("pre")
    if cause_list_section:
        text_content = cause_list_section.get_text()
    else:
        # fallback to full text (but usually not needed)
        text_content = "NO CAUSE LIST FOUND OR INVALID PARAMETERS"

    text_file = f"cause_list_{date}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text_content)

    pdf = FPDF()
    pdf.add_page()
    # Unicode font (ensure DejaVuSans.ttf exists in the same directory)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=10)
    for line in text_content.split("/n"):
        pdf.cell(0, 8, txt=line.strip(), ln=True)

    pdf_file = text_file.replace(".txt", ".pdf")
    pdf.output(pdf_file)
    return pdf_file

HTML = """
<!doctype html>
<title>eCourts Cause List Scraper</title>
<h2>Cause List Fetcher</h2>
<form method="post">
  State Code: <input type="text" name="state" required><br><br>
  District Code: <input type="text" name="district" required><br><br>
  Court Complex Code: <input type="text" name="complex" required><br><br>
  Court Code: <input type="text" name="court" required><br><br>
  Date (YYYY-MM-DD): <input type="text" name="date" required><br><br>
  <input type="submit" value="Download Cause List">
</form>
{% if filename %}
  <p>Your file is ready: <a href="/download/{{ filename }}">Download PDF</a></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    filename = None
    if request.method == "POST":
        filename = get_cause_list(
            request.form["state"],
            request.form["district"],
            request.form["complex"],
            request.form["court"],
            request.form["date"]
        )
    return render_template_string(HTML, filename=filename)

@app.route("/download/<filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)