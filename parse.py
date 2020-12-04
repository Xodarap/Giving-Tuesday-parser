from bs4 import BeautifulSoup
import re
from pathlib import Path

def parse_file(filename):
  f = open(filename, "r", encoding='utf-8')
  printable_name = filename.split('- ')[1][0:-5]
  html_text = f.read()
  soup = BeautifulSoup(html_text, 'html.parser')
  headers = soup.select('h2.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl.aahdfvyu.hzawbc8m')
  donation_strings = [(header.text.split(' donated ')) for header in headers]
  for donation in donation_strings:
    printable = [v.encode("utf-8").decode('utf-8').replace(',','') for v in donation]
    # todo: there's still some weird stuff with UTF encoding here
    print( printable_name.replace(',','') +',' + ','.join(printable).encode("utf-8").decode('utf-8')[0:-1])

for path in Path('2020-12-03-20201204T021819Z-001/2020-12-03').rglob('*.html'):
  parse_file('2020-12-03-20201204T021819Z-001/2020-12-03/' + path.name)