import requests
from bs4 import BeautifulSoup
req = requests.get("https://www.marthastewart.com/314342/extra-dirty-martini")
soup = BeautifulSoup(req.text)
json_script = soup.find("script", type="application/ld+json")
import json
script_content = json.loads(json_script.text)
page_data = json.loads(script_content["outputItems"]["data"])