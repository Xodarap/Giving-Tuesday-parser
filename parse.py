from bs4 import BeautifulSoup
import re
from pathlib import Path

output_file = open("output_dates.csv", "w", encoding='utf-8')

def parse_file(filename):
  f = open(filename, "r", encoding='utf-8')
  printable_name = ('- '.join(filename.split('- ')[1:]))[0:-5]
  html_text = f.read()
  soup = BeautifulSoup(html_text, 'html.parser')
  donation_strings = [handle_donation(d) for d in soup.select('div.j83agx80.cbu4d94t.ew0dbk1b.irj2b8pg')]
  for donation in donation_strings:
    if '$' in donation:   # without a $ it's a title and not a donation
      combined = printable_name.replace(',','') +',' + donation
      output_file.write(combined +'\n')
      # print( combined )

def handle_donation(donation):
  headers = donation.select('h2.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl.aahdfvyu.hzawbc8m')
  if len( headers) == 0:
    return ''
  donation_strings = headers[0].text.split(' donated ')
  printable = [v.replace(',','') for v in donation_strings]
  single_line =  ','.join(printable).encode("utf-8").decode('utf-8')[0:-1]
  return single_line + ',' + get_date(donation)

def get_date(donation):
  date_elements = donation.select('span.b6zbclly span.b6zbclly')
  if date_elements is None:
    return ''
  visible = list(filter(lambda v: not (v.has_attr('style')), date_elements))
  combined = ''.join([d.text for d in visible])
  if combined[0:2] == 'ec':
    return 'D' + combined
  elif combined[0:2] == 'es':
    return 'Y' + combined
  elif combined[0:2] == 'ov':
    return 'N' + combined
  return combined

for path in Path('new/2020-12-03').rglob('*.html'):
  parse_file('new/2020-12-03/' + path.name)
  print( path.name )
# parse_file('new/2020-12-03/Giving Tuesday 2020- Albert Schweitzer Foundation via ACE.html')
output_file.close()