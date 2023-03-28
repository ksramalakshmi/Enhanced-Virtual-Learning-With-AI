import numpy as np 
import pandas as pd
import nltk
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize

import urllib
from requests_html import HTML
from requests_html import HTMLSession

from lxml import html
from tqdm.notebook import tqdm

from warnings import simplefilter

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from rake_nltk import Rake

def wikilinks():
    with open("/content/mydrive/MyDrive/Krypthon-codes/audio.txt","r") as f:
        text = f.read()
    main_topic=[]
    r=Rake()
    r.extract_keywords_from_text(text)
    phrase_df = pd.DataFrame(r.get_ranked_phrases_with_scores(), columns = ['score','phrase'])
    a=phrase_df.loc[phrase_df.score>3]
    for j in range(len(a)):
        if(len(a['phrase'][j].split())>2):
            continue
        else : 
            main_topic.append(a['phrase'][j])
            break
    
    main_subject = main_topic[0]
    
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
            'action': 'query',
            'format': 'json',
            'generator':'links',
            'titles': main_subject,
            'prop':'pageprops',
            'ppprop':'wikibase_item',
            'gpllimit':1000,
            'redirects':1
            }
    
    req = requests.get(url, params=params)
    r_json = req.json()
    linked_pages = r_json['query']['pages']
    
    page_titles = [p['title'] for p in linked_pages.values()]
    
    # select first X articles
    num_articles = 200
    pages = page_titles[:num_articles] 
    
    # make sure to keep the main subject on the list
    pages += [main_subject] 
    
    # make sure there are no duplicates on the list
    pages = list(set(pages))
    

    
    text_db = []
    for page in tqdm(pages):
        response = requests.get(
                'https://en.wikipedia.org/w/api.php',
                params={
                    'action': 'parse',
                    'page': page,
                    'format': 'json',
                    'prop':'text',
                    'redirects':''
                }
            ).json()
    
        raw_html = response['parse']['text']['*']
        document = html.document_fromstring(raw_html)
        text = ''
        for p in document.xpath('//p'):
            text += p.text_content()
        text_db.append(text)
    print('Done')
    
    
    # Create a list of English stopwords
    stop_words = stopwords.words('english')
    
    # Instantiate the class
    vec = TfidfVectorizer(
        stop_words=stop_words, 
        ngram_range=(2,2), # bigrams
        use_idf=True
        )
    
    # Train the model and transform the data
    tf_idf =  vec.fit_transform(text_db)
    
    # Create a pandas DataFrame
    df = pd.DataFrame(
        tf_idf.toarray(), 
        columns=vec.get_feature_names_out(), 
        index=pages
        )
    
    idf_df = pd.DataFrame(
        vec.idf_, 
        index=vec.get_feature_names_out(),
        columns=['idf_weights']
        )
        
    idf_df.sort_values(by=['idf_weights']).head(10)
    
    
    # (optional) Disable FutureWarning of Scikit-learn

    simplefilter(action='ignore', category=FutureWarning)
    
    # select number of topic clusters
    n_topics = 25
    
    # Create an NMF instance
    nmf = NMF(n_components=n_topics)
    
    # Fit the model to the tf_idf
    nmf_features = nmf.fit_transform(tf_idf)
    
    # normalize the features
    norm_features = normalize(nmf_features)
    
    # Create clustered dataframe the NMF clustered df
    components = pd.DataFrame(
        nmf.components_, 
        columns=[df.columns]
        ) 
    
    clusters = {}
    
    # Show top 25 queries for each cluster
    for i in range(len(components)):
        clusters[i] = []
        loop = dict(components.loc[i,:].nlargest(25)).items()
        for k,v in loop:
            clusters[i].append({'q':k[0],'sim_score': v})
    
    # Create dataframe using the clustered dictionary
    grouping = pd.DataFrame(clusters).T
    grouping['topic'] = grouping[0].apply(lambda x: x['q'])
    grouping.drop(0, axis=1, inplace=True)
    grouping.set_index('topic', inplace=True)
    
    def show_queries(df):
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x['q'])
        return df
    
    # Only display the query in the dataframe
    clustered_queries = show_queries(grouping)
    
    data = clustered_queries.to_csv("/content/sample.csv")
    
    data1=pd.read_csv('/content/sample.csv')
    
    topics = data1.iloc[0]
    
    def get_source(url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
    
        except requests.exceptions.RequestException as e:
          print(e)
    
    def scrape_google(query):
    
        query = urllib.parse.quote_plus(query)
        response = get_source("https://www.google.co.uk/search?q=" + query)
    
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')
    
        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        
        return links
        
    hlink=[]
    for i in topics:
      hlink.append(scrape_google(i))
    
    links = {}
    for i in range(len(topics)) :
        links[topics[i]] = hlink[i][0]

    return links
    
    
    
