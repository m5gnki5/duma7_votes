from bs4 import BeautifulSoup
import requests
from time import sleep
from collections import defaultdict
import json

PARSER = "html.parser"

def collect_votes(doomer, page=0):
	"""Parses all the votes of a given deputy from http://vote.duma.gov.ru.

	Args:
		doomer (str): id of a Duma deputy
		page (int): number to start iteration from

	Returns:
		Dictionary of all unique projects as strings (keys)
		and deputy’s votes as lists of bools (values).

	Raises:
		ConnectTimeoutError: If site rejects your ip or something (I’ve had problem with proxy)
	"""
	url = "http://vote.duma.gov.ru/"
	params = {"deputy":doomer, "page":page}

	r = requests.get(url, timeout=30.0, params=params)
	soup = BeautifulSoup(r.text, PARSER)

	projects = soup.select(".item .item-left a")
	project_names = [p.text for p in projects]

	votes = soup.select(".item .item-right")
	voting_results = [v.text for v in votes]

	compreh_voting_dict = defaultdict(list)
	
	for p, v in zip(project_names, voting_results):
		compreh_voting_dict[p].append(v.split(":")[1].replace("\n", ""))
		compreh_voting_dict[p].append(v.split("\n")[1])

	return compreh_voting_dict


with open("rostov_duma_deputies_7th_convocation.csv", "r") as file:
	deputies = [l.split(";")[1] for l in file]
deputies.pop(0)

for i in range(10):
	portion_of_votes = collect_votes(deputies[0], i)
	with open(f"{deputies[0]}.json", "a", encoding='utf8') as output:
		json.dump(portion_of_votes, output, indent=2, ensure_ascii=False)
	sleep(1.5)
