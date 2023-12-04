import json
import time
import requests
import msal

APP_CLIENT_ID = "ac8a700d-77b0-490d-a1fd-ab261a8e0209"
AUTHORITY = "https://yokotaituni.ciamlogin.com"
APP_CLIENT_SECRET = "mmF8Q~WLPf5yuPI9ehSIaZhbGsXAR4otQPPoFaQD"
SCOPES = [f"api://bb47df4f-9456-4b9b-a013-7d88cfd7d14f/.default"]
API_URL = "https://app-yokot-we-tuni.azurewebsites.net/api/v1/"

SCRAPING_ID = "news-scraping"
app = msal.ConfidentialClientApplication(
    APP_CLIENT_ID, authority=AUTHORITY, client_credential=APP_CLIENT_SECRET
)
result = None
result = app.acquire_token_silent(SCOPES, account=None)
tag = None
if not result:
    result = app.acquire_token_for_client(scopes=SCOPES)
if not result:
    print("Failed to acquire a token.")
    quit()

def getHeaders():
    return {"Authorization": "Bearer " + result["access_token"]}

def getTags():
    res = requests.post(
        API_URL + "tags", json={"name": SCRAPING_ID}, headers=getHeaders()
    )
    global tag
    tag = res.json()
    print(json.dumps(tag, indent=4))

def scrapeNews(url):
    document = requests.post(
        API_URL + "documents",
        files={
            "data": (
                None,
                json.dumps(
                    {
                        "tags": [tag["id"]],
                        "url": url,
                        "rooturl": "",
                        "maxdepth": 0,
                        "maxexternaldepth": 0,
                    }
                ),
                "application/json",
            ),
        },
        headers=getHeaders(),
    ).json()
    print(json.dumps(document, indent=4))

    document_parsed = False
    while not document_parsed:
        doc = requests.get(
            f"{API_URL}documents/{document['id']}?raw=true", headers=getHeaders()
        ).json()
        if doc["raw_text"] != "":
            document_parsed = True
        time.sleep(1)
        print("Waiting for document to be parsed...")

def getPrompt(name, age, language, location, genres):
    return f"Hello, my name is {name}. I am {age} years old. What \
    are most interesting news for me happening near {location}?.\
    Please intend every news item and separate them by empty space. Give the response in {language}."


def askRecentNews(name, age, language, location, genres):
    chat = requests.post(
        API_URL + "chats",
        json={
            "name": "Recent news",
            "tags": [tag["id"]],
            "use_internal_data": True,
        },
        headers=getHeaders(),
    ).json()
    print(json.dumps(chat, indent=4))

    message = requests.post(
        API_URL + "messages",
        json={"chat_id": chat["id"], "content": getPrompt(name, age, language, location, genres)},
        headers=getHeaders(),
    ).json()
    print(json.dumps(message, indent=4))

    messages = requests.get(
        API_URL + "messages?chat_id=" + chat["id"], headers=getHeaders()
    ).json()
    print(json.dumps(messages, indent=4))
    return messages[-1]["content"]

def scrapeAllNews():
    urls = {
        "Pori": "https://www.pori.fi/uutisarkisto/",
        "Rauma": "https://www.rauma.fi/ajankohtaista/#/",
        "Ulvila": "https://www.ulvila.fi/ajankohtaista/",
        "Eurajoki": "https://www.eurajoki.fi/category/uutiset/",
        "Eura": "https://www.eura.fi/kategoria/ajankohtaista/",
        "Nakkila": "https://nakkila.fi/#ajankohtaista",
        "Pomarkku": "https://www.pomarkku.fi/index.php/category/yleinen/",
        "Harjavalta": "https://www.harjavalta.fi/category/ajankohtaista/",
        "Kokemäki": "https://kokemaki.fi/kategoria/ajankohtaista/",
        "Huittinen": "https://www.huittinen.fi/uutishuone/ajankohtaista",
        "Jämijärvi": "https://jamijarvi.fi/ajankohtaista/",
        "Kankaanpää": "https://www.kankaanpaa.fi/category/ajankohtaista/",
        "Siikainen": "https://siikainen.fi/category/ajankohtaista/",
        "Merikarvia": "https://merikarvia.fi/category/ajankohtaista/",
        "Karvia": "https://karvia.fi/ajankohtaista"
    }
    for city, url in urls.items():
        scrapeNews(url)

if result and "access_token" in result:
    getTags()
    #scrapeAllNews()
else:
    print(result["error"])
    print(result["error_description"])
    print(result["correlation_id"])
