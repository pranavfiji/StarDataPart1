from attr import attrs
from selenium import webdriver
from bs4 import BeautifulSoup
import csv,time,requests

url="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("chromedriver.exe")
browser.ger(url)
time.sleep(12)
newStarData=[]
starData=[]
headers=["Name","Distance","Mass","Radius"]


def getData():
    
    for i in range(0,1):
        while True:
            time.sleep(1)
            soup=BeautifulSoup(browser.page_source,"html.parser")
            currentPage=int(soup.find_all("inputs",attrs={"class","page_num"})[0].get("value"))
            if currentPage<i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/table')
            else:
                break


            for ul_tag in soup.find_all("ul",attrs={"class","stars"}):
                li_tags = ul_tag.find_all("li")
                temp_list=[]
            for index,li_tag in enumerate(li_tags):
                if index  == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])

                    except:
                        #double quotes means dont do anything
                        temp_list.append("")
                        # if it stops somewhere, write continue and continue to next block
                        continue

            hyper_link_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki"+hyper_link_li_tag.find_all("a",href=True)[0]["href"])

            starData.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def fetchInfo(hyperLink):
    try:
        page = requests.get(hyperLink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class","fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:

                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class","value"})[0].contents[0])

                except:
                    temp_list.append("")
            newStarData.append(temp_list)
    
    except:
        time.sleep(10)
        fetchInfo(hyperLink)

for index,data in enumerate(starData):
    fetchInfo(data[5])

final = []
for index,data in enumerate(starData):
    newData = newStarData[index]
    newData = [i.replace("\n","")for i in newData]
    newData = newData[:7]
    final.append(data+newData)


with open("newStarData.csv","w") as f:
    f1 = csv.writer(f)
    f1.writerow(headers)
    f1.writerows(starData)