import requests
from bs4 import BeautifulSoup

"""for i in range(630):
    URL = f"https://immogroup.ahouefa.com/biens-acheter/page/{str(i)}/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get url on a "class="card-image ad__card-image waves-block waves-light"
    results = soup.find_all("a", class_="listing-featured-thumb hover-effect")
    # get href on a
    for result in results:
        print(result["href"])
        with open("immogroup.txt", "a") as file:
            file.write(result["href"] + "\n")
            file.close()
"""
# iterate over the txt file
with open("immogroup.txt", "r") as file:
    for line in file:
        try:
            URL = f"{str(line)}"
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            # get txt from span "class=breadcrumb cible"
            title = soup.find("div", class_="page-title")
            print(title)
            print("aa")
            date = soup.find("span", class_="small-text grey").text.replace(
                "Mis à jour le", ""
            )
            print(date)
            detail = soup.find("ul", class_="list-2-cols list-unstyled")
            # get all li from ul "class=list-2-cols list-unstyled"
            detail_list = detail.find_all("li")
            price = detail_list[1].text
            print(price)
            superficie = detail_list[2].text
            type_ = detail_list[3].text
            description = soup.find("div", class_="block-content-wrap").text
            locality = soup.find("address", class_="item-address").text
            # save on csv file
            with open("immogroup.csv", "a", newline="") as csvfile:
                csvfile.write(
                    f"{title}, {price}, {date}, {superficie}, {type_}, {description}, {locality}\n"
                )
            print(title)
        except Exception as e:
            print(e)
            print("An error occurred")
            continue
    file.close()
