import requests

def get_definitions(word_id):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_id.lower()}"
    response = requests.get(url)
    if response.status_code != 200:
        return False

    data = response.json()
    try:
        definitions = []
        meanings = data[0]['meanings']
        for meaning in meanings:
            for definition in meaning['definitions']:
                definitions.append(f"👉 {definition['definition']}")

        audio_url = None
        phonetics = data[0].get('phonetics', [])
        for p in phonetics:
            if 'audio' in p and p['audio']:
                audio_url = p['audio']
                break

        return {
            'definitions': "\n".join(definitions),
            'audio': audio_url
        }
    except (IndexError, KeyError):
        return False
