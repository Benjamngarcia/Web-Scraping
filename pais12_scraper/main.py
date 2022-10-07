import requests
from bs4 import BeautifulSoup

HOME_URL = 'https://www.pagina12.com.ar'


def parse_article(article):
    try:
        articlePage = requests.get(article)
        if articlePage.status_code == 200:
            articleInfo = []
            #['tile', 'date', 'content']
            #PARSE CURRENT PAGE
            soupArticle = BeautifulSoup(articlePage.text, 'lxml')
            #GET TITLE
            titleArticle = soupArticle.find('div', attrs={'class': 'col 2-col'}).find('h1').getText()
            articleInfo.append(titleArticle)
            #GET ARTICLE DATE
            dateArticle = soupArticle.find('div', attrs={'class': 'date modification-date'}).find('span').getText()
            articleInfo.append(dateArticle)
            #GET ARTICLE CONTENT
            articleContent = soupArticle.find('div', attrs={'class': 'article-main-content article-text'}).find_all('p')
            articleContentText = [(contentText.getText()) for contentText in articleContent]
            articleContentText = ' '.join(articleContentText)
            articleInfo.append(articleContentText)

            print(articleInfo)
        else:
            raise ValueError(f'Error: {articlePage.status_code}')
    except ValueError as ve:
        print(ve)


def parse_page(link):
    try:
        section = requests.get(link)
        if section.status_code == 200:
            #PARSE CURRENT PAGE
            soupSection = BeautifulSoup(section.text, 'lxml')
            #GET FEATURED ARTICLE
            featuredArticle = soupSection.find('h1', attrs={'class': 'title-list'})
            if featuredArticle == None:
                pass
            else:
                featuredLink = HOME_URL + featuredArticle.a.get('href')
                #GET HORIZONTAL ARTICLES
                articleListH = soupSection.find_all('h2', attrs={'class': 'title-list featured-article'})
                articleLinkH = [(HOME_URL + titleH.a.get('href')) for titleH in articleListH]
                #GET VERTICAL ARTICLES
                articleListV = soupSection.find_all('h2', attrs={'class': 'is-display-inline title-list'})
                articleLinkV = [(HOME_URL + titleV.a.get('href')) for titleV in articleListV]
                #ARRAY ARTICLE LINKS
                articleLinksArr = (articleLinkH + articleLinkV)
                articleLinksArr.append(featuredLink)
                
                for article in articleLinksArr:
                    parse_article(article)
        else:
            raise ValueError(f'Error: {section.status_code}')
    except ValueError as ve:
        print(ve)



def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            #GET NAV LINKS
            listLinks = soup.find('ul', attrs = {'class': 'main-sections'}).find_all('li')
            linkArr = [link.a.get('href') for link in listLinks]
            for currentLink in linkArr:
                parse_page(currentLink)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__=='__main__':
    run()