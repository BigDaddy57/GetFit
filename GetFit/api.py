import requests

def search_food(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": "lCjwUKEmLbfcxI8ue6CxvVHyfyb5ltOCPagbsZEG",
        "query": query
    }
    response = requests.get(url, params=params)
    return response.json()
