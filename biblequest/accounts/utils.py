import requests

def fetch_bible_data(book, chapter=None, verse=None):
    """
    Fetch Bible data (verse, chapter, or book) from the King James Bible API.
    :param book: The name of the book (e.g., "John", "Genesis").
    :param chapter: The chapter number (optional).
    :param verse: The verse number (optional).
    :return: The text of the requested data or an error message.
    """
    base_url = "https://bible-api.com/"
    if verse:
        url = f"{base_url}{book}+{chapter}:{verse}?translation=kjv"  # Fetch specific verse
    elif chapter:
        url = f"{base_url}{book}+{chapter}?translation=kjv"  # Fetch entire chapter
    else:
        url = f"{base_url}{book}?translation=kjv"  # Fetch entire book

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'verses' in data:
                return data['verses']  # Return list of verses for chapters or books
            else:
                return data['text']  # Return single verse text
        else:
            return f"Error: Unable to fetch data (Status Code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to connect to the API. Details: {str(e)}"