import requests
from lxml import etree
import requests
from lxml import etree
import pdfkit
from selenium import webdriver # 自動爬蟲，為了取得搜尋網址
import urllib.parse # 解決url中文字的問題

def pdftrans(filename): # 轉成pdf檔
	try :
		pdfkit.from_url( url[0], '/Users/lijicheng/Desktop/' + filename + '/' + title[0] + '.pdf') # 轉檔
	except :
		pass

keyword = input('請輸入欲搜尋的關鍵字（若有2個以上，請以空白鍵隔開）:')
pages = input('請輸入要取幾頁的搜尋結果（一頁有10筆資料，若要所有資料，請輸入"所有"）:')
file = input('要存放至桌面的哪個資料夾？（輸入資料夾名稱）：')
print('請將滑鼠游標移至米字號 ＊')

trans_keyword = urllib.parse.quote(keyword) # 編碼轉換
driver = webdriver.Safari() 
driver.get( 'https://www.google.com.tw/search' + '?q=' + trans_keyword ) # 搜尋
secondpage = driver.find_element_by_xpath('//*[@id="nav"]/tbody/tr/td[7]/a').get_property('href') # 取得完整網址
startpoint = secondpage.find('start=') # 找到要更改的位置
url_front = secondpage[ : startpoint+6 ] # 網址前半部（取到start=）
url_back = secondpage[ startpoint+8 : ] # 網址後半部

title_list = [] # 標題
url_list = [] # 網址
headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15" } 
# 用自身瀏覽器的網頁代理，假裝不是爬蟲

result = 'not_empty' 

if pages == '所有' :
	pages = 100 # 設為100頁

for i in range( int(pages) ): # 頁數代表抓取次數 
	if result == 'empty' : # 爬完了
		break
	response = requests.get( url_front + str( i*10 ) + url_back, headers = headers ) # 取得網址，reponse為200代表取得成功
	content = response.content.decode() # 單純印出content為unicode的形式，因此用decode解碼，()內沒輸入時預設為utf-8
	html = etree.HTML( content ) # 使用 xpath 選擇器來擷取數據
	for j in range( 10 ) : # 每一頁有10筆資料
		title = html.xpath( '//*[@id="rso"]/div/div/div[' + str(j+1) + ']/div/div/div[1]/a/h3/text()' ) # 通常xpath
		if title == [] :
			title = html.xpath( '//*[@id="rso"]/div/div/div[' + str(j+1) + ']/div/div/div[1]/a[1]/h3/text()' ) # 第二種xpath
		if title == [] and j == 0 : # 如果改了還是空的，而且是第一筆資料
			result = 'empty' # 爬取完畢
			break 
		url = html.xpath( '//*[@id="rso"]/div/div/div[' + str(j+1) + ']/div/div/div[1]/a/@href' ) # 已取得網址與標題
		pdftrans(file)
