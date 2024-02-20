import csv

import requests
from bs4 import BeautifulSoup

for i in range(119):
    URL = f"https://benin-immo.com/parcelle-a-vendre-au-benin-terrain/page/{str(i)}/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get url on a "class="card-image ad__card-image waves-block waves-light"
    results = soup.find_all("div",
                            class_="property_listing property_unit_type7")
    # get "a" on results
    for result in results:
        print(result.a["href"])
        with open("terrain_benin_immo.txt", "a") as file:
            file.write(result.a["href"] + "\n")
            file.close()

# iterate over the txt file
with open("terrain_benin_immo.txt", "r") as file:
    # Open the CSV file in append mode
    with open("terrain_benin_immo.csv", "a", newline="") as file_csv:
        # Create a writer object
        writer = csv.writer(file_csv)

        # Write the headers to the CSV file
        writer.writerow(
            ["title", "description", "price", "area", "location", "date"])
        for line in file:
            try:
                URL = f"{str(line)}"
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                # get txt from span "class=breadcrumb cible"
                title = soup.find("h1", class_="entry-title entry-prop").text
                price = soup.find("div", class_="price_area").text
                date = soup.find("li", class_="first_overview_date").text
                superficie = soup.find_all("ul",
                                           class_="overview_element")[-1].text
                description = soup.find("div",
                                        class_="wpestate_property_description")
                locality = soup.find("div", class_="property_categs").text
                # Write the data to the CSV file
                writer.writerow(
                    [title, description, price, superficie, locality, date])
            except Exception:
                print("An error occurred")
                continue
    file.close()
