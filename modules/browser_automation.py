import webbrowser
import urllib.parse
from core.speech import speak


def play_youtube_video(command: str):
    """
    Plays a video on YouTube by extracting the search term from command.
    Example: 'play shape of you on youtube' ➝ searches 'shape of you' on YouTube.
    """
    command = command.lower()
    if "play" in command and "on youtube" in command:
        search_term = command.split("play", 1)[1].split("on youtube")[0].strip()
    elif "youtube" in command:
        search_term = command.split("youtube", 1)[0].strip()
    else:
        search_term = command.strip()

    if search_term:
        query = urllib.parse.quote_plus(search_term)
        url = f"https://www.youtube.com/results?search_query={query}"
        print(f"🎬 Searching on YouTube: {search_term}")
        webbrowser.open(url)
    else:
        speak("Sorry, I couldn't extract what you want to search on YouTube.")


def open_website(site: str):
    """
    Opens any website directly (fully qualified).
    """
    if not site.startswith("http"):
        site = f"https://{site}"
    print(f"🌐 Opening: {site}")
    webbrowser.open(site)


def open_generic(command: str):
    """
    Open a generic website by extracting the domain or keyword.
    """
    command = command.lower()
    keyword = command.replace("open", "").strip()

    sites_map = {
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",
        "twitter": "https://x.com",
        "linkedin": "https://linkedin.com",
        "github": "https://github.com",
        "chat gpt": "https://chat.openai.com",
        "chatgpt": "https://chat.openai.com",
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "gmail": "https://mail.google.com",
        "google drive": "https://drive.google.com",
        "youtube studio": "https://studio.youtube.com",
        "amazon": "https://amazon.in",
        "flipkart": "https://flipkart.com",
        "netflix": "https://netflix.com",
        "prime video": "https://primevideo.com",
        "spotify": "https://open.spotify.com",
        "notion": "https://notion.so",
        "figma": "https://figma.com",
        "canva": "https://canva.com",
        "maps": "https://maps.google.com",
        "news": "https://news.google.com",
        "stackoverflow": "https://stackoverflow.com"
    }

    for key in sites_map:
        if key in keyword:
            print(f"🌐 Opening known site: {sites_map[key]}")
            webbrowser.open(sites_map[key])
            return

    if "." in keyword:
        url = f"https://{keyword}"
        print(f"🌍 Opening custom site: {url}")
        webbrowser.open(url)
    else:
        speak("Sorry, I don't recognize that site.")


def search_google(command: str):
    """
    Extract search term and search it on Google.
    """
    command = command.lower().replace("search", "").replace("on google", "").strip()
    if command:
        query = urllib.parse.quote_plus(command)
        url = f"https://www.google.com/search?q={query}"
        print(f"🔍 Searching Google: {command}")
        webbrowser.open(url)
    else:
        speak("What would you like me to search on Google?")


def search_chatgpt(command: str):
    """
    Search something on ChatGPT (openai.com).
    """
    command = command.lower().replace("search", "").replace("on chatgpt", "").replace("chat gpt", "").strip()
    if command:
        query = urllib.parse.quote_plus(command)
        url = f"https://chat.openai.com/?q={query}"
        print(f"🤖 Searching on ChatGPT: {command}")
        webbrowser.open(url)
    else:
        speak("What should I search on ChatGPT?")


def search_wikipedia(command: str):
    """
    Search a topic on Wikipedia.
    """
    command = command.lower().replace("search", "").replace("on wikipedia", "").strip()
    if command:
        query = urllib.parse.quote_plus(command)
        url = f"https://en.wikipedia.org/wiki/{query}"
        print(f"📚 Searching Wikipedia: {command}")
        webbrowser.open(url)
    else:
        speak("What topic should I look up on Wikipedia?")


def search_reddit(command: str):
    """
    Search for a topic on Reddit.
    """
    command = command.lower().replace("search", "").replace("on reddit", "").strip()
    if command:
        query = urllib.parse.quote_plus(command)
        url = f"https://www.reddit.com/search/?q={query}"
        print(f"👽 Searching Reddit: {command}")
        webbrowser.open(url)
    else:
        speak("What should I search on Reddit?")


def open_news_headlines():
    """
    Open Google News homepage.
    """
    url = "https://news.google.com"
    print("🗞️ Opening Google News")
    webbrowser.open(url)


def open_weather_forecast(location=""): 
    """
    Open the weather forecast for the specified location.
    """
    query = urllib.parse.quote_plus(location) if location else "my location"
    url = f"https://www.google.com/search?q=weather+{query}"
    print(f"🌦️ Opening weather forecast for {query}")
    webbrowser.open(url)


def open_email():
    """
    Opens Gmail in default browser.
    """
    url = "https://mail.google.com"
    print("📬 Opening Gmail")
    webbrowser.open(url)


def open_calendar():
    """
    Opens Google Calendar.
    """
    url = "https://calendar.google.com"
    print("📅 Opening Calendar")
    webbrowser.open(url)


def open_drive():
    """
    Opens Google Drive.
    """
    url = "https://drive.google.com"
    print("📂 Opening Google Drive")
    webbrowser.open(url)


def open_code_editor():
    """
    Opens VS Code online.
    """
    url = "https://vscode.dev"
    print("🖥️ Opening Visual Studio Code in browser")
    webbrowser.open(url)