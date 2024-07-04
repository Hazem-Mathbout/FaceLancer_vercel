from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def scrapKhamsat(output, requests_session):
    # requests_session = requests.Session()
    payloadForSearchTerm = ""
    baseSoup = BeautifulSoup("", 'lxml')
    ORIGN = "https://khamsat.com"
    URL = ORIGN + "/community/requests"
    URL_LOAD_MORE = "https://khamsat.com/ajax/load_more/community/requests"
    listResult = []
    templistResult = []
    try:
        if not output:
            return []
        num_page_khamsat = output.get("num_page_khamsat")
        offset = output.get("offset_khamsat")
        limit = 25 if output.get("limit", 0) > 25 else output.get("limit", 0)

        if num_page_khamsat > 1:
            dataLoadMore = str(output.get("dataLoadMore", ""))
            response = requests_session.post(URL_LOAD_MORE, headers=HEADERS, data=dataLoadMore.removesuffix('&'))
            if response.status_code in [200, 201]:
                body = response.json()
                htmlString = body.get("content", "")
                baseSoup = BeautifulSoup(htmlString, "lxml")
        else:
            basePage = requests_session.get(URL, headers=HEADERS)
            baseSoup = BeautifulSoup(basePage.text, "lxml")

        results = baseSoup.findAll(name='tr', attrs={"class": "forum_post"})
        results = results[offset: offset+limit]

        if results:
            with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                future_to_offer = {executor.submit(taskKahmsatScraping, offer): offer for offer in results}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        if data:
                            templistResult.append(data)

                future_to_Link_offer = {executor.submit(taskScrapLinksKhamsat, offer, requests_session): offer for offer in templistResult}
                for future in concurrent.futures.as_completed(future_to_Link_offer):
                    offer = future_to_Link_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        payloadForSearchTerm += data["postId"] + "&"
                        listResult.append(data)

        try:
            listResult.sort(key=lambda x: x['dateTime'], reverse=True)
        except Exception as exc:
            print(f"Error occure when sorting offers khamsat, error is:{exc}")
        listResult.append({"all_post_id": payloadForSearchTerm})
    except Exception as exc:
        print(f"This Exception When Connect To Khamsat error is : {exc}")
    
    return listResult


def taskKahmsatScraping(res) -> dict:
    myDict = {}
    ORIGN = "https://khamsat.com"
    try:
        title = res.find('h3', attrs={"class": "details-head"}).find('a').text
        url = ORIGN + res.find('h3', attrs={"class": "details-head"}).find('a').get('href', "")
        time = res.find('td', attrs={"class": "details-td"}).find('ul').findAll('li')[1].find('span').text.strip()
        url_img = res.find('td', attrs={"class": "avatar-td text-center"}).find('img').get('src', "")
        postId = res.get('id', "").replace("forum_post-", "posts_ids%5B%5D=")

        myDict = {"postId": postId, "webSiteName": "khamsat", "title": title, "url": url, "time": time,
                "status": None, "price": None, "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From khamsat get offer the error is : {exc}")
    return myDict

def taskScrapLinksKhamsat(offer, requests_session):
    myDict = {}
    try:
        webpage2 = requests_session.get(offer["url"], headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='article', attrs={"class": "replace_urls"}).text
        content = " ".join(content.split())
        number_of_offers = soup.findAll(name='div', attrs={"class": "card-header bg-white"})[1].find(name='h3').text
        publisher = soup.find(name='a', attrs={"class": "sidebar_user"}).text
        statusOfPublisher = soup.find(name='ul', attrs={"class": "details-list"}).find(name='li').text.strip()
        dateTime = soup.findAll(name='div', attrs={"class": "col-6"})[1].find(name='span').get('title', "")
        date_time_obj = datetime.strptime(dateTime, '%d/%m/%Y %H:%M:%S GMT')
        dateTime = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        myDict = {"dateTime": dateTime, "publisher": publisher, "statusOfPublisher": statusOfPublisher,
                "content": content, "number_of_offers": number_of_offers}
        offer.update(myDict)
        return offer
    except Exception as exc:
        print(f"This Exception From khamsat get offer the error is : {exc}")
    return myDict
