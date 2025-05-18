import requests

def get_book_description(title):
    seach_url = f"https://openlibrary.org/search.json"
    response = requests.get(seach_url, params={"title": title})
    if response.status_code != 200:
        return None
    results = response.json().get("docs", [])
    if not results:
        return None
    
    book_key = results[0].get("key")
    if not book_key:
        return None
    
    details_url = f"https://openlibrary.org{book_key}.json"
    details_response = requests.get(details_url)
    if details_response.status_code != 200:
        return None
    
    detail_data = details_response.json()
    description = detail_data.get("description")
    if isinstance(description, dict):
        return description.get("value")
    return description or None
    