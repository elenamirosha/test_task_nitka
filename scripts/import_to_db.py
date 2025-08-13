import sqlite3
import csv
print("Start connection to the db")
# 1. Connecting to the db
conn = sqlite3.connect("../documents.db")
cursor = conn.cursor()

print("Start creating the table")
# 2. Creating the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    doi TEXT PRIMARY KEY,
    title TEXT,
    summary TEXT,
    tags TEXT,
    year INTEGER,
    organization TEXT,
    country TEXT,
    language TEXT,
    pdf_link TEXT
)
""")
print("Finish creating the table")
print("Start inserting to the table")
# 3. Reading CSV and inserting to the table
with open("../doi_table.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # reading by column titles
    for row in reader:
        cursor.execute("""
            INSERT OR REPLACE INTO documents
            (doi, title, summary, tags, year, organization, country, language, pdf_link )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["DOI"],
            row["Title"],
            row["Summary"],
            row["Tags"],
            row["Year"],
            row["Organization"],
            row["Country"],
            row["Language"],
            row["PDF_Link"]
        ))
print("Finish inserting to the table")
# 4. Saving changes
conn.commit()
conn.close()

print("Changes saved")

print("import completed!")