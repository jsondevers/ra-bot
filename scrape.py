import requests
from bs4 import BeautifulSoup


# scrapes data from umd dining menu
def getFood():
    page = requests.get("http://nutrition.umd.edu/")  # not secured smh
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("a")
    food = set()

    for i in range(12, len(elements)):
        item = str(elements[i])
        item = item[item.find(">") + 1 :].replace(
            "</a>", ""
        )  # locate food, and remove tags

        # don't add the leftover tags
        if not (
            item.startswith(" <span") or item.startswith("(") or item.startswith("http")
        ):
            food.add(item)

    f = open("food.txt", "w")
    for item in food:
        f.write(item + "\n")

    return food
