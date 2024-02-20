import csv

import requests
from bs4 import BeautifulSoup

for i in range(455):
    URL = f"https://www.logerchic.com/fr/buy-category/terrain/page-{str(i)}.html/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get url on a "class="card-image ad__card-image waves-block waves-light"
    results = soup.find_all("a", class_="uk-text-primary")
    # get href on a
    for result in results:
        print(result["href"])
        with open("logerchic.txt", "a") as file:
            file.write(result["href"] + "\n")
            file.close()

# iterate over the txt file
with open("logerchic.txt", "r") as file:
    # Open the CSV file in append mode
    with open("logerchic.csv", "a", newline="") as file_csv:
        # Create a writer object
        writer = csv.writer(file_csv)

        # Write the headers to the CSV file
        writer.writerow(["title", "description", "price", "area", "location", "date"])
        for line in file:
            try:
                URL = f"https://www.logerchic.com{str(line)}"
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                # get txt from span "class=breadcrumb cible"
                title = soup.find("h2", class_="uk-h3 uk-margin-remove-bottom").text
                date = soup.find_all("div", class_="uk-margin-small-left")
                for i in date:
                    if "Publi" in i.text:
                        date = i.text
                        break
                detail = soup.find(
                    "ul",
                    class_="uk-card uk-card-default  uk-card-body uk-width-1-1 uk-margin-top",
                )
                location = soup.find("span", class_="address_details").text
                price = soup.find("span", class_="price1 uk-margin-left").text
                superficie = soup.find("table", class_="uk-table uk-table-striped").text

                # Write the data to the CSV file
                writer.writerow([title, detail, price, superficie, location, date])
            except Exception as e:
                print(e)
                print("An error occurred")
                continue
