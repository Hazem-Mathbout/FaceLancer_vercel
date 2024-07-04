from bs4 import BeautifulSoup
import concurrent.futures

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def scrapkafiil(output, requests_session, isFuncInternal):
    num_bage_kafiil = 1 if output["num_bage_kafiil"] == "None" else output["num_bage_kafiil"]
    category_kafiil = output["category_kafiil"]
    delivery_duration_for_kafiil = "" if output[
        "delivery_duration_for_kafiil"] == "None" else output["delivery_duration_for_kafiil"]
    budget_max = 10000 if output["budget_max"] == "None" else output["budget_max"]
    budget_min = 0.00 if output["budget_min"] == "None" else output["budget_min"]
    searchTerm = output["searchTerm"]
    offset = output["offset_kafiil"]
    limit = 25 if output["limit"] > 25 else output["limit"]

    listResult = []

    if category_kafiil == "None":
        URL = f"https://kafiil.com/projects?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    else:
        URL = f"https://kafiil.com/projects/{category_kafiil}?delivery_duration={delivery_duration_for_kafiil.removesuffix(',')}&page={num_bage_kafiil}&search={searchTerm}&source=web"
    try:
        sourcPage = requests_session.get(URL, headers=HEADERS)
        sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
        tempRes = sourcSoup.findAll(
            name='div', attrs={"class": "project-box active"})
        tempRes = tempRes[offset: offset+limit]
        print(f"tempRes befor apply operation is: {len(tempRes)}")
        if len(tempRes) != 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_offer = {executor.submit(
                    taskScrapKafiil, offer, requests_session, budget_min, budget_max): offer for offer in tempRes}
                for future in concurrent.futures.as_completed(future_to_offer):
                    offer = future_to_offer[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (offer, exc))
                    else:
                        print("***************************************************")
                        if len(data) != 0:
                            print(data)
                            listResult.append(data)
        print(f"Number offers in kafiil {len(listResult)}")

    except Exception as exc:
        print(f"This Exception When connect To Kafiil the error is : {exc}")
    try:
        listResult.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as axc:
        print(f"Error occure when sorting offers kafiil, error is:{exc}")
        
    return listResult

def taskScrapKafiil(res, requests_session, budget_min, budget_max) -> dict:
    myDict = {}
    price = res.findAll('p')[0].text.strip()
    list_price = price.split('-')
    numMin = int(list_price[0].strip().removeprefix('$'))
    numMax = int(list_price[1].strip().removeprefix('$'))
    budget_max = int(float(budget_max))
    budget_min = int(float(budget_min))
    if ((budget_min > 0 or budget_max < 10000) and not (numMin >= budget_min and numMax <= budget_max)):
        return
    try:
        title = res.findAll('a')[1].text.split()
        if (title[0] != "قيد"):
            title = " ".join(title[1:])
        else:
            title = " ".join(title[2:])
        url = res.findAll('a')[1].get_attribute_list('href')[0]
        time = res.findAll('span')[1].text.strip()
        status = res.findAll('span')[0].text
        number_of_offers = res.findAll('span')[2].text.strip()
        url_img = res.find('img').get_attribute_list('src')[0]
        postId = url.split('-')[0].split('/')[-1]
        #################################################
        webpage2 = requests_session.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='p', attrs={"class": ""}).text
        content = " ".join(content.split())
        publisher = soup.find(
            name='div', attrs={"class": "user-info-row"}).find('div').find('a').text
        publisher = " ".join(publisher.split())
        dateTime = soup.find(name='span', attrs={
                "data-toggle": "tooltip"}).get_attribute_list('title')[0]
        myDict = {"postId": postId, "dateTime": dateTime, "publisher": publisher, "statusOfPublisher": None,  "webSiteName": "kafiil", "title": title,
                "content": content, "url": url, "time": time, "status": status, "price": price, "number_of_offers": number_of_offers, "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From kafiil get offer the error is : {exc}")
    return myDict