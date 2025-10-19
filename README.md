# eCourts PDF Scraper

## Developed by
**Shyam Kumar**

## Description
This project automates the download of *cause list PDFs* from the eCourts website based on user input.

Users can select:
- State
- District
- Court Complex
- Court Name
- Date

The system fetches and downloads the cause list PDFs **in real time** directly from the eCourts website.

## How to Run
1. Install required packages:
pip install flask requests beautifulsoup4
2. Run the application:
python ecourts_scraper.py
3. Open the browser at:
http://127.0.0.1:5000/
4. Enter court details → Click “Fetch Cause List”.


