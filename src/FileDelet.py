import plotly
import plotly.plotly as py

import json
import requests
from requests.auth import HTTPBasicAuth

username = 'truedick23' # Replace with YOUR USERNAME
api_key = 'KVC5i7PjhVyvUuOK3emw' # Replace with YOUR API KEY

auth = HTTPBasicAuth(username, api_key)
headers = {'Plotly-Client-Platform': 'python'}

sites = ['https://plot.ly/~truedick23/31', 'https://plot.ly/~truedick23/30', 'https://plot.ly/~truedick23/37', 'https://plot.ly/~truedick23/36',
         'https://plot.ly/~truedick23/43', 'https://plot.ly/~truedick23/42', 'https://plot.ly/~truedick23/51']

for site in sites:
    num = site.split('/')[-1]
    print(num)
    fid = 'truedick23' + ':' + num

    requests.post('https://api.plot.ly/v2/files/'+fid+'/trash', auth=auth, headers=headers)