from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def parse_search_links(url:str) -> list:
	html = requests.get(url).text
	soup = BeautifulSoup(html, "html.parser")

	a_els = soup.find_all("a", {"class" : "search-results__link"})

	search_links = []

	for el in a_els:
		if not ("login" in el['href']): search_links.append(el['href'])

	links = []

	for search_link in tqdm(search_links, desc='Collecting links'):
		html = requests.get(search_link).text

		link_soup = BeautifulSoup(html, "html.parser")
		div_els = link_soup.find_all("div", {"class": "document-page__toc"})

		div_soup = BeautifulSoup(str(div_els), "html.parser")
		law_links = div_soup.find_all("a")

		for el in law_links:
			if "Глава" not in el.contents[0]:
				links.append(f"http://www.consultant.ru{el['href']}")

	return links


def parse_texts(links:list) -> list:
	texts = []

	for url in tqdm(links, desc='Collecting texts from links'):
		html = requests.get(url).text
		soup = BeautifulSoup(html, "html.parser")

		div_el = soup.find_all("div", {"class": "document-page__content"})

		soup = BeautifulSoup(str(div_el), "html.parser")
		p_els = soup.find_all('p')

		for p_el in p_els:
			try:
				if p_el != '':
					texts.append(p_el.text)

			except TypeError:
				continue
				
	return texts