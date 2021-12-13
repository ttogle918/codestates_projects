import requests
from bs4 import BeautifulSoup

from requests.models import Response

API_KEY = '3PhzBCEtpmwCyjr4qvdqaH2oeTFutHtCvpsC7iFJrOzHDDLARXY3qu1HIqqx%2BEJHdxW5JYfe6KXqgX6nK%2BmjGA%3D%3D'
BASE_URL = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'

def get_data(items, tags, len_tag) :
  # page에 주어진 data 추출
  data = []
  for item in items :
    text = item.get_text()
    start = 0
    i = 0
    temp = []
    for tag in tags :
      start = text.find(tag, start) + len_tag[i]
      end = text.find('<', start)
      i+=1
      temp.append(text[start:end].strip())
      
    data.append(temp)
  return data


def get_tag(text) :
  # tags 구하기(features)
  tags = []
  start = text.find('<', 0)
  end = 0
  while end != len(text) :
    end = text.find('>', start)
    tag = text[start : end+1]
    if len(tags) > 0 :
      if tags[0] == tag :
        break
    tags.append(tag)
    start = text.find('<', end+1)

  len_tag = []  # tag 글자 길이
  for tag in tags :
    len_tag.append(len(tag))

  print(tags)
  return tags, len_tag


def get_page(LAWD_CD, DEAL_YMD, tags, len_tag):
    """
  
    """
    # 달 별로 200개씩 데이터 불러오기
    url = f'{BASE_URL}?serviceKey={API_KEY}&pageNo=19&numOfRows=200&LAWD_CD={LAWD_CD}&DEAL_YMD={DEAL_YMD}'
    
    try :
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      text = soup.get_text()
    except Exception as Err :
      print('에러 발생')
    else :
      print("성공")

    if tags == [] :
      tags, len_tag = get_tag(text)

    total_count = soup.find('totalcount')
    # 값이 해당 페이지에 들어있지 않다면 빈 data와 0(값의 개수)를 리턴
    
    items = soup.find_all('item')

    data = get_data(items, tags, len_tag)
    # total_count : <~>value</~>이다. 여기서 text == str
    return data, int(total_count.text), tags, len_tag

