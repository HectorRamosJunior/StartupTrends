from django.shortcuts import render, redirect
from .models import Startup
# For the company/startup list generation
import urllib
from bs4 import BeautifulSoup


# Loads the main index page, basically a copy of yclist. 
def startup_list(request): 
    startups = Startup.objects.all()
    return render(request, 'trends/startup_list.html', {'startups': startups})

# Scrapes the yclist site for the startups, redirects back to index when done
def get_startups(request):
    Startup.objects.all().delete()

    company_list = get_company_list("http://yclist.com/")
    for company in company_list:
        startup = Startup()

        startup.name = company["name"]
        startup.status = company["status"]
        startup.yc_class = company["yc_class"]
        startup.description = company["description"]

        # URL field can be None type
        if company["url"] == None:
            startup.url = None
        else:
            startup.url = (company["url"])

        startup.save()

    return redirect('startup_list')

def get_company_list(base_url):
    """Scrapes the comany data off a given webpage and returns a 
    list of dictionaries, each dictionary containing a startup's data.

    This assumes the webpage data is structured like the data set at 
    http://yclist.com/

    Args:
        base_url: The base website url to scape data from

    Returns:
        company_list: List of dictionaries containing startup data.
    """
    company_list = []

    page = urllib.urlopen(base_url).read()
    soup = BeautifulSoup(page, "html.parser")

    # Parses for all the companies a tags in the table on the page
    table_rows = soup.find("tbody").findAll("tr")

    # Scrapes the company data from each tr in the tbody
    for row in table_rows:
        company_dict = {}
        # columns is a list of all the td tags within the row element
        columns = row.findAll("td")

        company_dict["name"] = columns[1].text
        company_dict["yc_class"] = columns[3].text.replace("\n","").strip()
        company_dict["status"] = columns[4].text
        company_dict["description"] = columns[5].text

        # Company doesn't always have a url given
        if columns[2].find("a"):
            company_dict["url"] = columns[2].find("a").get("href")
        else:
            company_dict["url"] = None

        company_list.append(company_dict)

    return company_list