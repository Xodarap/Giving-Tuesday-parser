from bs4 import BeautifulSoup
import re
from pathlib import Path
from datetime import datetime

output_file = open("output_dates.csv", "w", encoding='utf-8')

def parse_file(filename):
  f = open(filename, "r", encoding='utf-8')
  printable_name = filename[5:-5]
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
  def extract_date(donation):
    date_elements = donation.select('span.l9j0dhe7 span.l9j0dhe7:not(.vw7X6QX):not(.idG4), span.l9j0dhe7 span.nc684nl6:not(.vw7X6QX):not(.idG4)')
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
  extracted = extract_date(donation)
  try:
    return datetime.strptime(extracted, '%B %d at %I:%M %p').replace(year = 2021).__str__()
  except ValueError:
    # try:
    return datetime.strptime(extracted, 'Yesterday at %I:%M %p').replace(year = 2021, month=12, day=1).__str__()
    # except ValueError:
      # return extracted

for path in Path('data').rglob('*.html'):
  print( path.name )
  parse_file('data/' + path.name)
# parse_file('new/2020-12-03/Giving Tuesday 2020- Albert Schweitzer Foundation via ACE.html')
output_file.close()