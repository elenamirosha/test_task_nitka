import requests
from bs4 import BeautifulSoup

print('Start of the application')

def getSchiHubPDF(html):
    result = None
    soup = BeautifulSoup(html, "html.parser")

    # Different ways of PDF defined in the SchiHub page markup
    iframe = soup.find(id='pdf')
    plugin = soup.find(id='plugin')
    embedScihub = soup.find("embed")

    if iframe is not None:
        result = iframe.get("src")

    if plugin is not None and result is None:
        result = plugin.get("src")

    if result is not None and result[0] != "h":
        result = "https:" + result

    if embedScihub is not None and result is None:
        result = embedScihub.get("original-url")

    return result


def downloadPdf(doi):
    searchUrl = f"https://sci-hub.se/{doi}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"} # Important for avoiding blocks

    # Initial page with the requested DOI
    response = requests.get(searchUrl, headers=headers)
    # Here we parse the page to find the PDF file if it exists
    pdfLink = getSchiHubPDF(response.text)

    if pdfLink:
        # Get the exact PDF file
        pdfResponse = requests.get(pdfLink)
        if pdfResponse.status_code == 200:
            filename = f"downloads/{doi.replace("/", "_").replace("\n", "")}.pdf"
            with open(filename, 'wb') as f:
                f.write(pdfResponse.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download PDF from {pdfLink}")
    else:
        print("No direct PDF link found.")

# We store DOIs in the file
filename= '../dois.txt'

with open(filename) as file:
    for line in file:
        downloadPdf(line)


print('End of the application')