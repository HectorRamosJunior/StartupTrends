import urllib
from bs4 import BeautifulSoup

def get_company_stack(company_name):
    """Scrapes a company's stack data off its stackshare profile, if
    it exists, and returns a dictionary of the stacks and technologies used.

    This assumes the webpage data is structured like the data set at 
    http://stackshare.io/standard-cyborg/standard-cyborg

    Args:
        company_name: The name of the given company to get the tech stack of

    Returns:
        stack_layer_dict: A dictionary of the stack and techologies used by the company
    """
    # Stackshare uses hyphens for spaces in the url, and all lowercase
    company_name = company_name.replace(" ", "-").lower()
    stackshare_url = "http://stackshare.io/" + company_name + "/" + company_name

    page = urllib.urlopen(stackshare_url).read()
    soup = BeautifulSoup(page, "html.parser")

    # If the page doesn't have this element, the company page doesn't exist
    if not soup.find("div", {"class": "full-stack-container app-layers"}):
        return None

    # Grab the stack layer divs from the page
    layers = soup.find("div", {"class": "full-stack-container app-layers"})
    layers = layers.findAll("div", {"style": "padding-bottom:5px"})


    stack_layer_dict = {}
    # Scrapes each stack layer for the services within
    # Adds the layer_dict to the stack_layer_dict
    for layer in layers:
        layer_title = layer.find("div", 
                                {"class": "stack-layer-title stack-layer-title-tag"}
                                ).text 
        layer_dict = {}
        
        # Grab all the services in the current layer
        services = layer.findAll("div", {"id": "stp-services"})

        # Add each service and its type (IE: language, server) to the layer_dict
        for service in services:
            service_name = service.find("a", {"class": "stack-service-name-under"}).text
            service_type = service.find("a", {"class": "function-name-under"}).text

            if not service_type in layer_dict:
                layer_dict[service_type] = []

            layer_dict[service_type].append(service_name)

        # Add the current layer's data to the stack dict
        stack_layer_dict[layer_title] = layer_dict

    return stack_layer_dict

test_dict = get_company_stack("Credit Karma")

for layer,layer_dict in test_dict.iteritems():
    for k,v in layer_dict.iteritems():
        print k,v