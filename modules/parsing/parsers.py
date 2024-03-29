from bs4 import BeautifulSoup
import requests
import os
import json
from config import NUM_LINKS_TO_GET, PATH_TO_JSON
from googlesearch import search
from text_handling import find_most_relevant_part
import threading
import wikipedia as wiki

def parse_google(query:str, results:list) -> list:
	texts = []
	links = search(query=query, stop=5, start=0, pause=2)

	for link in links:
		html = requests.get(link).text

		text = BeautifulSoup(html, 'lxml').text
		texts.append(text)

	results.extend(texts)


def nalog_ru_parser(query:str, results:list) -> list:
	texts, links = [], []

	url = 'https://www.nalog.gov.ru/rn78/search/?type=all&text=' + query + '&dr=3271&rm=1&type=documents&fd=&td='

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'lxml')

	a_els = soup.find_all('a', {'class' : 'results__title'})

	for a_el in a_els:
		links.append(f"https://www.nalog.gov.ru/{a_el['href']}")

	for link in links[:NUM_LINKS_TO_GET]:
		html = requests.get(link).text

		soup = BeautifulSoup(html, 'lxml')
		div_el = soup.find('div', {'class':'text_block'})

		text = BeautifulSoup(str(div_el), 'lxml').text
		texts.append(text)

	results.extend(texts)


def search_for_relevant_part_in_json(query:str, results:list) -> str:
	path_to_json = PATH_TO_JSON

	if not os.path.exists(path_to_json): raise FileNotFoundError(f"No file {path_to_json}")
	if not path_to_json.split(".")[-1] == 'json': raise TypeError(f"Your file {path_to_json} is not .json")

	with open(path_to_json, 'r', encoding='utf=8') as f:
		parts = json.loads(f.read())

	max_sim_tokens = 0

	for text in tuple(parts.values()):
		found_part, sim_tokens = find_most_relevant_part(query, text, 32)

	if sim_tokens >= max_sim_tokens:
		max_sim_tokens = sim_tokens
		best_part = found_part

	results.append((best_part, max_sim_tokens))


def wiki_parser(query:str, results:list) -> list:
	wiki.set_lang("ru")
	search_results = wiki.search(query)

	try:
		page = wiki.page(search_results[0])
		results.append(page.content)
	except IndexError:
		results.append(' ')

def multiple_parse(query:str) -> list: 
	thread_list, results = [], []

	for func in (search_for_relevant_part_in_json, parse_google, wiki_parser):
		thread = threading.Thread(target=func, args=(query,results))
		thread_list.append(thread,)
		thread.start()

		print(f'Added thread: {func.__name__}')

	for i in range(len(thread_list)):
		thread_list[i].join()

	return results