import os
import time

import requests
from bs4 import BeautifulSoup
from notify_run import Notify

notify = Notify(endpoint=os.environ['gradoscope_channel'])
# notify.write_config()
notify.send('Hello')
universities = [['Brown', 'University'], ['Purdue', 'University'], ['Simon', 'Fraser'], ['Mcgill'], ['Toronto'],
                ['British', 'Columbia'], ['Alberta'], ['Georgia', 'Institute'], ['Waterloo']]

# universities = [['Brown', 'University']]

urls = {}
for uni in universities:
    u_str = ""
    for name in uni:
        u_str += name.lower() + "+"

    urls[uni[0]] = 'https://www.thegradcafe.com/survey/index.php?q=' + u_str + 'computer+science&t=a&o=&p=1'

responses = {}
soups = {}
t_rows = {}
rows_id_dict = {}

# Run Indefinitely
while True:
    for uni_key in urls.keys():
        # Get response
        responses[uni_key] = requests.get(urls[uni_key])

        # Init Soup
        soups[uni_key] = BeautifulSoup(responses[uni_key].text, "html.parser")

        # Extract Table Rows
        t_rows[uni_key] = \
            soups[uni_key].body.main.findAll('section', {'class': 'submissions'})[0].div.table.findAll('tr')[1:]

        # Extract Row IDs
        u = []
        for rr in t_rows[uni_key]:
            u.append(
                int(rr['onmouseover'].split(',')[1][:-2])
            )

        # Check if there is any new entry
        if uni_key in rows_id_dict.keys():  # If key exists, means not first run
            if rows_id_dict[uni_key][0] != u[0]:  # New entry found
                # Find number of new entries
                try:
                    idx = u.index(rows_id_dict[uni_key][0])
                    # Find if the newer ids were admits/rejects
                    decisions = []
                    no_r, no_a, no_o = 0, 0, 0
                    for i in range(0, idx):
                        d = str(t_rows[uni_key][i].findAll('td')[2].next).lower()
                        if 'rejected' in d:
                            no_r += 1
                        elif 'accepted' in d:
                            no_a += 1
                        elif 'other' in d:
                            no_o += 1
                    print(no_r, no_a, no_o)

                    message = str(uni_key) + "\n" + "Accept: " + str(no_a) + "\nReject: " + str(
                        no_r) + "\nOther: " + str(no_o)
                    notify.send(message)
                    print(message)
                    rows_id_dict[uni_key] = u
                except Exception:
                    print('Too many new indices')
                    notify.send(str(uni_key) + "Too many new indices")

            pass
        else:
            rows_id_dict[uni_key] = u
        time.sleep(10)

    time.sleep(300)
