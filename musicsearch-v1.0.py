
import requests

BASE_URL = "https://itunes.apple.com/search"

search_term = input("Enter a search term: ")

payloyd = {
    "term": search_term,
    "entity": "album",
    "limit": 5
}

response = requests.get(BASE_URL, params=payloyd)
response_json =response.json()

result_count = response_json["resultCount"]
print("The search returned ", result_count, "results.")

for result in response_json["results"]:
    artist = result["artistName"]
    album = result["collectionName"]
    tracks = result["trackCount"]
    print("Artist:", artist)
    print("Album:", album)
    print("Track Count:", tracks)
    
#print(f"completed url: ", {response.url})
#print(response_json)

