from django.shortcuts import render,redirect,HttpResponse
from sys import executable
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.views.decorators.clickjacking import xframe_options_exempt
import time
import re
import base64
from django.contrib import messages
def prepare_urls(matches):
    return list({match.replace("\\u0026", "&") for match in matches})
def img_urls(match):
    txt =  match.replace("\\u0026","&")
    return txt
def get_as_base64(url):
    return ("data:image/jpeg;base64,"+base64.b64encode(requests.get(url).content).decode('utf-8'))
def getv_as_base64(url):
    return ("data:video/mp4;base64,"+base64.b64encode(requests.get(url).content).decode('utf-8'))
def getdata(url):
    user_agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    #url ="https://www.instagram.com/p/CQJaQQ3nD7n/?utm_source=ig_web_copy_link"
    options = Options()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    
    #driver = webdriver.Chrome(executable_path="/sm/chromedriver", options=options)
    userName = "_socialmate_"
    passWord = "sd712246"
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)
    try:
        driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input").send_keys(userName)
        driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input").send_keys(passWord)
        time.sleep(1)
        driver.find_element_by_css_selector("button[type=submit]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[@class='sqdOP yWX7d    y3zKF     ']").click()
    except:
        driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(userName)
        driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(passWord)
        
        driver.find_element_by_css_selector("button[type=submit]").click()
    time.sleep(1)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    #one pic
    #l = len(soup.find_all('script'))
    script = soup.find_all('script')
    data = re.search( r'window._sharedData = (\{.+?});</script>', str(script)).group(1)
    data1 = script[-2]
    #fields = dict(re.findall(pattern))
    #text=script
    #match =re.findall(r"http\S+.mp4", str(text))
    #print(match[0])
    #displayUrl = re.findall(r"display_url\":.+?(?=\")", str(data))
    #print(displayUrl[0])
    #IGimageUrl = re.findall(r"http\S", str(displayUrl))
    #ar =""
    #for x in displayUrl:
        # ar=ar+(img_urls(x))
    #print(ar.split('display_url":"'))
    #print(k["entry_data"]['PostPage'][0]['graphql']['shortcode_media']['display_url'])
    pics = []
    video = []
    try:
        try:
            check = re.findall(r"video_url\":.+?(?=\")", str(data))
            check2 = re.findall(r"video_url\":.+?(?=\")", str(data1))
            if len(check)<1:
                displayUrl = check2
            else:
                displayUrl = check
            #print(displayUrl)
            #IGimageUrl = re.findall(r"http\S", str(displayUrl))
            if(len(displayUrl)==1):
                #print(displayUrl)
                ar=""
                displayUrl = img_urls(displayUrl[0])
                #print(displayUrl)
                ar = (displayUrl.split('video_url":"'))
                #print(ar) 
                code = getv_as_base64(ar[1])
                video.append([0,code,ar[1]])
            else:
                ar=""
                for x in displayUrl:
                    ar=ar+(img_urls(x))
                print(ar)
                ar = (ar.split('video_url":"'))
                for i in range(len(ar)-1):
                    if(ar[i]=="" or ar[i]==ar[i+1]):
                        continue
                    else:
                        #print(urllib.request.urlretrieve(ar[i],f"gfg{i}.png"))
                        code = getv_as_base64(ar[i])
                        video.append([i,code,ar[i]])
                    if(i==len(ar)-2):
                        #print(urllib.request.urlretrieve(ar[i+1],f"gfg{i+1}.png"))
                        code = getv_as_base64(ar[i+1])
                        video.append([i+1,code,ar[i+1]])
        except:
            print("There is no video")
        try:
            check = re.findall(r"display_url\":.+?(?=\")", str(data))
            check2 = re.findall(r"display_url\":.+?(?=\")", str(data1))
            if len(check)<1:
                displayUrl = check2
            else:
                displayUrl = check
            #print(len(displayUrl))
            #IGimageUrl = re.findall(r"http\S", str(displayUrl))
            if(len(displayUrl)==1):
                #print(displayUrl)
                ar=""
                displayUrl = img_urls(displayUrl[0])
                #print(displayUrl)
                ar = (displayUrl.split('display_url":"'))
                #print(ar)
                code = get_as_base64(ar[1])
                pics.append([0,code,ar[1]])
                #print(pics)
            else:
                ar=""
                for x in displayUrl:
                    ar=ar+(img_urls(x))
                ar = (ar.split('display_url":"'))
                for i in range(len(ar)-1):
                    if(ar[i]=="" or ar[i]==ar[i+1]):
                        continue
                    else:
                        #print(urllib.request.urlretrieve(ar[i],f"gfg{i}.png"))
                        code = get_as_base64(ar[i])
                        pics.append([i,code,ar[i]])
                    if(i==len(ar)-2):
                        #print(urllib.request.urlretrieve(ar[i+1],f"gfg{i+1}.png"))
                        code = get_as_base64(ar[i+1])
                        pics.append([i+1,code,ar[i+1]])
            #print(pics)
        except:
            print("There is no courasel image")
    except:
        raise ConnectionError("Check your internet conection")
        print("This is a private account")
    res={"pics":pics,"video":video}
    #driver.quit()
    return res
#not_now_notif=browser.find_element_by_xpath("//button[@class='aOOlW   HoLwm ']")
# Create your views here.
def home(request):
    return render(request,'main.html')
@xframe_options_exempt
def get_insta(request):
    if request.method == "POST":
        query = request.POST['url']
        context = getdata(query)
    return render(request,"main.html",context)

def download(request,url):
    if request.method == "POST":
        name = url+"ele"
        furl = request.POST[name]
        filename =furl.split("?")[0].split("/")[-1]
        r = requests.get(furl)
        
        #file = open(filename,'rb')
        #response = FileResponse(file)
        if r.status_code == 200:
            content_type = "application/octet-stream"
            response = HttpResponse(r.content, content_type=content_type)
            response["Content-Disposition"]= "attachment; filename={}".format(filename)
                #print('Image sucessfully Downloaded: ',filename)
            messages.success(request,"File downloaded")
            return response
        else:
            print('Image Couldn\'t be retreived')
            messages.error(request,"Image Couldn't be retreived")
            return redirect(home)

#https://www.instagram.com/p/CLmnJVupe9B/?utm_source=ig_web_copy_link
