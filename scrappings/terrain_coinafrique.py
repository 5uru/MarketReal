import requests
from bs4 import BeautifulSoup

for i in range(119):
    URL = f"https://bj.coinafrique.com/search?sort_by=last&category=49&page={str(i)}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get url on a "class="card-image ad__card-image waves-block waves-light"
    results = soup.find_all(
        "a", class_="card-image ad__card-image waves-block waves-light")

    # get href on a "class="card-image ad__card-image waves-block waves-light" and save on txt file
    for result in results:
        print(result["href"])
        with open("terrain_coinafrique.txt", "a") as file:
            file.write(result["href"] + "\n")
            file.close()
# numbers of href on the txt file
with open("terrain_coinafrique.txt", "r") as file:
    print(len(file.readlines()))
    file.close()

# iterate over the txt file
with open("terrain_coinafrique.txt", "r") as file:
    for line in file:
        try:
            print(line)
            URL = f"https://bj.coinafrique.com{str(line)}"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            # get txt from span "class=breadcrumb cible"
            title = soup.find("span", class_="breadcrumb cible").text
            price = soup.find("p", class_="price").text
            superficie = soup.find("span", class_="qt").text
            description = soup.find(
                "div", class_="ad__info__box ad__info__box-descriptions").text
            # save on csv file
            with open("terrain_coinafrique.csv", "a") as file_csv:
                file_csv.write(
                    f"{title}, {price}, {superficie}, {description}\n")
        except Exception:
            print("An error occurred")
            continue
    file.close()
