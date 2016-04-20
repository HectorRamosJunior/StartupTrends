from django.shortcuts import render, redirect
from .models import Startup, Service, Technology
from .getCompanyList import get_company_list
from .getCompanyStack import get_company_stack


# Loads the main index page, basically a copy of yclist. 
def startup_list(request): 
    startups = Startup.objects.all()
    return render(request, 'trends/startup_list.html', {'startups': startups})

def stack_list(request):
    services = Service.objects.all()
    return render(request, 'trends/stack_list.html', {'services': services})

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

# Scrapes the stackshare site for the stacks to each startup
# Then redirects back to the index when done
def get_stacks(request):
    startups = Startup.objects.all()

    for startup in startups:
        # A dictionary of dictionaries for each layer in the startup's stack
        stack_layer_dict = get_company_stack(startup.name)

        # The company page didn't exist on stackshare at the guessed url
        if not stack_layer_dict:
            continue

        for layer, layer_dict in stack_layer_dict.iteritems():
            for service_name, techology_array in layer_dict.iteritems():
                (service, exists) = Service.objects.get_or_create(name=service_name)
                service.name = service_name
                service.save()

                for technology_name in technology_array:
                    (technology, exists2) = Technology.objects.get_or_create(name=technology_name)

                    technology.name = technology_name
                    technology.startups.add(startup)
                    technology.save()

                    service.technologies.add(technology)
                    service.save()


    return redirect('stack_list')
