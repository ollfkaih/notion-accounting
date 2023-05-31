from bs4 import BeautifulSoup


def get_data_from_html(html, tag):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(tag)
    text_lines = [e.get_text(strip=True) for e in elements if not e.find(
        tag) and e.get_text(strip=True)]
    return remove_unnecessary_data(text_lines)


def remove_unnecessary_data(data):
    words_to_remove = ["Hei!", "Direkte", "Billigst"]
    data = [element for element in data if all(
        word not in element.split() for word in words_to_remove)]

    substrings_to_remove = [
        "Google", "Alle besparelser og all statistikk", "Var denne e-posten nyttig?", "Se flere flyreiser", "Vis alle flyreisene"]
    data = [element for element in data if not any(
        word in element for word in substrings_to_remove)]

    data = [item.replace('\xa0', '') for item in data]

    return data
