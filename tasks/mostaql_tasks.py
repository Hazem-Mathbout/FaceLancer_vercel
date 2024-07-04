from bs4 import BeautifulSoup
import concurrent.futures

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def scrapmostaql(output, requests_session):
    offset = output["offset_mostaql"]
    limit = 25 if output["limit"] > 25 else output["limit"]
    budget_max = 10000 if output["budget_max"] == "None" else output["budget_max"]
    budget_min = 0.00 if output["budget_min"] == "None" else output["budget_min"]
    num_bage_mostaql = 1 if output["num_bage_mostaql"] == "None" or 0 else output["num_bage_mostaql"]
    category_mostaql = output["category_mostaql"]
    delivery_duration_for_mostaql = "" if output[
        "delivery_duration_for_mostaql"] == "None" else output["delivery_duration_for_mostaql"]
    skills_for_mostaql = output["skills_for_mostaql"]
    searchTerm = output["searchTerm"]

    # finalRes = {}
    listResult = []

    if category_mostaql == "None":
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    else:
        URL = f"https://mostaql.com/projects?page={num_bage_mostaql}&keyword={searchTerm}&category={category_mostaql}&skills={skills_for_mostaql}&duration={delivery_duration_for_mostaql.removesuffix(',')}&budget_min={budget_min}&budget_max={budget_max}&sort=latest"
    try:
        sourcPage = requests_session.get(URL, headers=HEADERS)
        sourcSoup = BeautifulSoup(sourcPage.text, "lxml")
        tempRes = sourcSoup.findAll(name='tr', attrs={"class": "project-row"})
        tempRes = tempRes[offset: offset+limit]
        print(f"temp result length in mostaql is: {len(tempRes)}")
        if (len(tempRes) != 0):
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_offer = {executor.submit(
                    taskScrapMostaql, offer, requests_session): offer for offer in tempRes}
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
                    #  listResult.append({"postId" : postId , "dateTime" : dateTime , "publisher" : publisher , "statusOfPublisher" : None ,  "webSiteName" : "mostaql" , "title" : title , "content" : content , "url" : url , "time" : time , "status" : status , "price" : price , "number_of_offers" : number_of_offers , "url_img" : url_img})
        print(f'Number Offer mostaql is: {len(listResult)}')
    except Exception as exc:
        print(f"This Exception When Connect to Mostaql the error is : {exc}")
    try:
        listResult.sort(key=lambda x: x['dateTime'], reverse=True)
    except Exception as exc:
        print(f"Error occure when sorting offers mostaql, error is:{exc}")

    return listResult

def taskScrapMostaql(res, requests_session) -> dict:
    myDict = {}
    try:
        title = res.find('a').text
        url = res.find('a').get_attribute_list('href')[0]
        time = res.find('time').text.strip()
        time = "".join(time.split())
        number_of_offers = res.find('ul').findAll('li')[2].text.strip()
        postId = url.split('-')[0].split('/')[-1]
        ########################################################
        webpage2 = requests_session.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage2.text, "lxml")
        content = soup.find(name='div', attrs={
                    "class": "text-wrapper-div carda__content"}).text
        content = " ".join(content.split())
        publisher = soup.find(name='h5', attrs={
                    "class": "postcard__title profile__name mrg--an"}).find(name='bdi').text
        status = soup.find(name='bdi', attrs={
                    "class": "label label-prj-open"}).text
        price = soup.find(name='span', attrs={"dir": "rtl"}).text
        url_img = soup.find(name='div', attrs={
                    "class": "profile-card--avatar dsp--f small_avatar_container"}).find('img').get_attribute_list('src')[0]
        dateTime = soup.find(name='td', attrs={
                    "data-type": "project-date"}).find(name='time').get_attribute_list('datetime')[0]
        ########################################################
        myDict = {"postId": postId, "dateTime": dateTime, "publisher": publisher, "statusOfPublisher": None,  "webSiteName": "mostaql", "title": title,
                    "content": content, "url": url, "time": time, "status": status, "price": price, "number_of_offers": number_of_offers, "url_img": url_img}
    except Exception as exc:
        print(f"This Exception From mostaql get offer the error is : {exc}")
    return myDict
