import ast
import csv
import re
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

for i in range(119):
    URL = f"https://bj.coinafrique.com/search?sort_by=last&category=49&page={str(i)}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get url div class="card ad__card round small hoverable  undefined"
    results = soup.find_all("div", class_="col s6 m4 l3")
    for result in results:
        print(result.a["href"])
        try:
            # a with class="card-image ad__card-image waves-block waves-light"
            a = result.a["href"]
            # div with class="card-title ad__card-timesince"
            div = result.find("div", class_="card-title ad__card-timesince").text
            # save on txt file
            with open("terrain_coinafrique.txt", "a") as file:
                file.write(str([a, div]) + "\n")

                print([a, div])
                file.close()
        except Exception as e:
            print(e)
            continue

# numbers of href on the txt file
with open("terrain_coinafrique.txt", "r") as file:
    print(len(file.readlines()))
    file.close()

# iterate over the txt file
with open("terrain_coinafrique.txt", "r") as file:
    # Open the CSV file in append mode
    with open("terrain_coinafrique.csv", "a", newline="") as file_csv:
        # Create a writer object
        writer = csv.writer(file_csv)

        # Write the headers to the CSV file
        writer.writerow(["title", "description", "price", "area", "date"])

        for line in file:
            try:
                line = ast.literal_eval(line)
                print(line)
                URL = f"https://bj.coinafrique.com{line[0]}"
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                # get txt from span "class=breadcrumb cible"
                title = soup.find("span", class_="breadcrumb cible").text
                price = soup.find("p", class_="price").text
                superficie = soup.find("span", class_="qt").text
                description = soup.find(
                    "div", class_="ad__info__box ad__info__box-descriptions"
                ).text
                if "heures" in line[1]:
                    date = datetime.now()
                elif "jour" in line[1]:
                    numbers = re.findall(r"\d+", line[1])
                    int_numbers = [int(number) for number in numbers]
                    date = datetime.now() + timedelta(days=int_numbers[0])
                elif "mois" in line[1]:
                    numbers = re.findall(r"\d+", line[1])
                    int_numbers = [int(number) for number in numbers]
                    date = datetime.now() + timedelta(days=int_numbers[0] * 30)
                else:
                    numbers = re.findall(r"\d+", line[1])
                    int_numbers = [int(number) for number in numbers]
                    date = datetime.now() + timedelta(days=int_numbers[0] * 365)
                # Write the data to the CSV file
                writer.writerow([title, description, price, superficie, date])
            except Exception as e:
                print(e)
                print("An error occurred")
                continue
    file.close()
