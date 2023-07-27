import requests
from bs4 import BeautifulSoup
import pandas as pd


topic_url='https://github.com/topics'
    # Download the page
response = requests.get(topic_url)
    # Check successful response
if response.status_code != 200:
    raise Exception('Failed to load page {}'.format(topic_url))
    # Parse using Beautiful soup
doc=BeautifulSoup(response.text,'html.parser')
selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = doc.find_all('p', {'class': selection_class})
desc_selector = 'f5 color-fg-muted mb-0 mt-1'
topic_desc_tags = doc.find_all('p', {'class': desc_selector})
topic_link_tags = doc.find_all('a', {'class': "no-underline flex-grow-0"})
topic_titles = []
topic_descs = []
topic_urls = []
base_url = 'https://github.com'

for tag in topic_title_tags:
    topic_titles.append(tag.text)
for tag in topic_desc_tags:
    topic_descs.append(tag.text.strip())
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
topics_dict={
    'title':topic_titles,
    'description':topic_descs,
    'url':topic_urls
}
topics_df=pd.DataFrame(topics_dict)
group=[]
repo=[]
star=[]
per=[]
prog=[]

for tags1 in topic_titles:
    base_url = 'https://github.com'
    topic_page_url = base_url+"/topics/"+tags1
    response = requests.get(topic_page_url)
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    h1_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all("h3" , {'class' :h1_selection_class})
    star_tags = topic_doc.find_all('span', { 'class': 'Counter js-social-count'})
    for tag in repo_tags:
        group.append(tags1)
        a_tags = tag.find_all('a')
        repo.append(a_tags[1].text.strip())
        per.append(a_tags[0].text.strip())
    for tag in star_tags:
        star.append(tag.text)
index=-1
lang1=[]
lang2=[]
for repos in repo:
        index=index+1
        url=base_url+"/"+per[index]+"/"+repos
        response = requests.get(url)
        repo_data = BeautifulSoup(response.text, 'html.parser')
        class1="color-fg-default text-bold mr-1"
        lang = repo_data.find_all("span" , {'class' :class1}, limit=2)
        if len(lang)==0:
            lang1.append("")
            lang2.append("")
        elif len(lang)==1:
            lang1.append(lang[0].text)
            lang2.append("")
        else :
            lang1.append(lang[0].text)
            lang2.append(lang[1].text)
repo_dict = {
    'Repo_Title': group,
    'Repo_Name': repo,
    'Manager':per,
    'Star': star,
    "language_1":lang1,
    "language_2":lang2
}
repo_df = pd.DataFrame(repo_dict)
repo_df=repo_df.to_json(orient='records')
with open('topic.json', 'w', encoding='utf-8') as f:
    f.write(repo_df)




