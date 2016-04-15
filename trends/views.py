from django.shortcuts import render, redirect
from .models import Startup
from .getCompanyList import get_company_list


# Loads the main index page, basically a copy of yclist. 
def startup_list(request): 
    startups = Startup.objects.all()
    return render(request, 'trends/startup_list.html', {'startups': startups})

# Scrapes the yclist site for the startups, redirects back to index when done
def get_startups(request):
    Startup.objects.all().delete()

    # A list of dictionaries, each dictionary holding a startup's data on ycList
    company_list = get_company_list("http://yclist.com/")

    for company in company_list:
        startup = Startup()

        startup.name = company["name"]
        startup.url = company["url"]    # Not every company on yclist has a url
        startup.status = company["status"]
        startup.yc_class = company["yc_class"]
        startup.description = company["description"]            

        startup.save()

    return redirect('startup_list')