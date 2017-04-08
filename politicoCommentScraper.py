import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Insert URL here
commentURL = 'http://www.politico.com/story/2017/04/how-republicans-learned-to-love-obama-237017'
#
takeURL = 'https://www.facebook.com/plugins/feedback.php?api_key&channel_url=http%3A%2F%2Fstaticxx.facebook.com%2Fconnect%2Fxd_arbiter%2Fr%2FnRK_i0jz87x.js%3Fversion%3D42%23cb%3Df222bb78dee75ac%26domain%3Dwww.politico.com%26origin%3Dhttp%253A%252F%252Fwww.politico.com%252Ff845b0f631571%26relation%3Dparent.parent&colorscheme=light&href=' + commentURL + '&locale=en_US&numposts=100&sdk=joey&skin=light&version=v2.3&width=840'
page = requests.get(takeURL)
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[2]
body = list(html.children)[2]
htmlScripts = soup.find_all('script')
commentArea = htmlScripts[20]
x = ''
for child in commentArea.children:
    commentArea = '' + child
    
start = commentArea.find('"comments"')
end = commentArea.rfind(',{"__m"')

htmlJson = "{" + commentArea[start:end]

commentJson = json.loads(htmlJson)

commentSection = commentJson['comments']['idMap'].items()


comments = {}
writers = {}
for key, value in commentSection:
    if 'body' in value:
        comments[key] = (value);
    elif 'name' in value:
        writers[key] = (value);

df = pd.DataFrame()
commentDf = df.from_dict(comments)
authorDf = df.from_dict(writers)
print(authorDf)