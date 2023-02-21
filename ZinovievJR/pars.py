import sneaky_token
from urllib.request import urlopen
import requests
import json
import re
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
ua = UserAgent()
u = ua.random


url = "https://glossary.slb.com/coveo/rest/search/v2?sitecoreItemUri=sitecore%3A%2F%2Fweb%2F%7BDDC23206-BEED-412D-B398-E51EF5878FFD%7D%3Flang%3Den%26amp%3Bver%3D1&siteName=OilfieldGlossary"


def hash_builder(raw_query):
    try:
        q_l = raw_query.split(" ")

        search_element = '%20'.join(q_l)
        return search_element
    except Exception as error:
        print(error)
    


def search_gl(query):

    for i in range(3):
        search_element = hash_builder(query)
        payload = f"actionsHistory=%5B%7B%22name%22%3A%22Query%22%2C%22value%22%3A%22{search_element}%22%2C%22time%22%3A%22%5C%222023-02-03T12%3A47%3A26.149Z%5C%22%22%7D%5D&referrer=&visitorId=159960ac-725f-4ec6-b884-2cc7ce7b55d3&isGuestUser=false&q={search_element}&aq=((%40z95xpath%3D%3D28F6D9B16B684F7C9BE6937026AB0B6B%20(%40haslayout%3D%3D1%20%40z95xtemplate%3D%3DE56888557E69403F911D10BC11CCDF5D))%20NOT%20%40z95xtemplate%3D%3D(ADB6CA4F03EF4F47B9AC9CE2BA53FF97%2CFE5DD82648C6436DB87A7C4210C7413B))&cq=(%40z95xlanguage%3D%3Den)%20(%40z95xlatestversion%3D%3D1)%20(%40source%3D%3D%22Coveo_web_index%20-%20SLB-Prod-Azure-CM%22)&searchHub=default&locale=en&maximumAge=900000&wildcards=true&partialMatch=true&partialMatchKeywords=1&partialMatchThreshold=35%25&firstResult=0&numberOfResults=12&excerptLength=200&enableDidYouMean=false&sortCriteria=relevancy&queryFunctions=%5B%5D&rankingFunctions=%5B%5D&groupBy=%5B%7B%22field%22%3A%22%40disciplinefacet%22%2C%22maximumNumberOfValues%22%3A9%2C%22sortCriteria%22%3A%22occurrences%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%2C%7B%22field%22%3A%22%40termstartletterfacet%22%2C%22maximumNumberOfValues%22%3A9%2C%22sortCriteria%22%3A%22alphaascending%22%2C%22injectionDepth%22%3A1000%2C%22completeFacetWithStandardValues%22%3Atrue%2C%22allowedValues%22%3A%5B%5D%7D%5D&facetOptions=%7B%7D&categoryFacets=%5B%5D&retrieveFirstSentences=true&timezone=Europe%2FMoscow&enableQuerySyntax=false&enableDuplicateFiltering=false&enableCollaborativeRating=false&debug=false&allowQueriesWithoutKeywords=true"


        r = requests.request("POST",url,headers=sneaky_token.get_header(), data=payload)

        print([r.status_code])
        try:

            data = r.json()
            temp_results=[]
            count=0
            for i in data["results"]:
                if count >4:
                    break
                else:
                    temp_dict = {
                        "title": i["title"],
                        "link": i["clickUri"]
                    }
                    temp_results.append(temp_dict)
                    count+=1
                
            return temp_results
        
        except json.JSONDecodeError as e:
            sneaky_token.process_browser_logs_for_network_events()
            
            

            print(f"New header:\n")
            if i < 3 - 1: # i is zero indexed
                continue
            else:
                
                raise
            break
        

def get_content(link):  
    r = requests.get(link,headers={"UserAgent":u})  
    html = bs(r.content, 'html5lib')
    # text
    title = html.find('div', attrs={'class': 'row'}).text
    all_text = []
    for i in range(4):
        if all_text == []:
            txt = (html.find('div', attrs={'class': 'content-two-col rte-tables'}).findChild().find_all_next("p")[i+1].text)
            if len(txt) > 20:
                all_text.append(txt)
                break
    
    text = all_text[0]
    #re filterring
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'.*:', ' ', text)
    text = re.sub(r'\d\.\s[A-Za-z]\.\s+\[([A-Za-z]+(\s+[A-Za-z]+)+)]',"",text)
    text = re.sub(r'see:+.*',"",text)
    text = re.sub(r'\n{3,7}',"",text)
    text = re.sub(r'\n{2,7}.*',"",text)

    #media
    try:
        images = html.find_all("img")
        imageSources = []

        for image in images:
            if image.get("alt") =="":
                imageSources.append(image.get('src'))
        
        base_url = "https://glossary.slb.com"
        img_links = [base_url+i for i in imageSources]
        img_links

    except Exception as err:
        print(err)

    return title.replace("\n",""), text, img_links




