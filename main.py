from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.files.file import File
import uvicorn
import urllib.request
import ssl
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.


# ID/PW 인증 : sharepoint내 파일 리스트 조회 (python 직접)
@app.get("/list2")
async def list2(request: Request, question:str = 'donald trump'):

    url = 'https://aipjt-sharepoint-list-id.koreacentral.inference.ml.azure.com/score'
    api_key = 'Bv6nwhfsCzpfpq7SYSUEg6sPqF2KzZc6YkVNDCPoLC6CLhKNXbJAJQQJ99BCAAAAAAAAAAAAINFRAZML3HyR'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {}
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return error.info()


# ID/PW 인증 : sharepoint내 파일 리스트 조회 (promptflow 사용)
@app.get("/list")
async def list(request: Request, question:str = 'donald trump'):

    url = 'https://aipjt-sharepoint-search-odqhq.koreacentral.inference.ml.azure.com/score'
    api_key = 'd2vfEOcV3iXUiGqXiR7h0BAcwoQovX7BhBApPxAOkpT9Estu8Xy9JQQJ99BBAAAAAAAAAAAAINFRAZML4FyQ'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {"question": question}
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return error.info()


# Index 사용 : sharepoint 질의응답
@app.get("/index")
async def index_search(request: Request, question:str):

    # Sharepoint 권한별 검색 및 생성형 답변
    # ID 가져옴
    # ID와 

    url = 'https://aipjt-sharepoint-index-0227.koreacentral.inference.ml.azure.com/score'
    api_key = '9EWSwRLJ5qjz0xVexmApROwZKbAVndJIZ1bAyogU4soi2GxtHrXhJQQJ99BBAAAAAAAAAAAAINFRAZML1Q2q'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {"question1": question}
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return error.info()


# token으로 sharepoint 조회하는 기능
@app.get("/sptoken")
async def token_search(request: Request, question:str = ''):

    url = 'https://aipjt-sharepoint-token-0226.koreacentral.inference.ml.azure.com/score'
    api_key = 'Ff5VQIP05srzuoZVUmXgQDnmsXxR8o9pIiGbbrNp7V2lrR2LkGFLJQQJ99BBAAAAAAAAAAAAINFRAZML3LQV'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {"topic": question}
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return error.info()