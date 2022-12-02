import json
import requests


try:
    configFile = open("config.json")
    privateKey = json.load(configFile)["APIKEY"]
    configFile.close()
except:
    print("Error Reading the config.json file.")
    exit()


headers = {
    "accept": "application/json",
    "Authorization": "Bearer {}".format(privateKey),
    "Notion-Version": "2021-08-16",
    "content-type": "application/json",
}

def getDB(databaseID):
    url = "https://api.notion.com/v1/databases/{}/query".format(databaseID)
    r = requests.post(url, headers={"Authorization": "Bearer {}".format(privateKey), "Notion-Version": "2021-08-16"})
    result = r.json
    print(result)

def getContentOfBlock(blockID):
    try:
        blockurl = "https://api.notion.com/v1/blocks/{}".format(blockID)
        blockResponse = requests.get(blockurl, headers=headers)
        jsonBlock = json.loads(blockResponse.text)
        return jsonBlock["paragraph"]["text"][0]["text"]["content"]
    except:
        print("Something went wrong")
        return -1

def updateContentOfParagraphBlock(blockID, newContent): #returns the response code of updating the content of a paragraph block in notion
    try:
        payload = {"paragraph" : {'color': 'default', 'text': [{'type': 'text', 'text': {'content': newContent, 'link': None}, 'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False, 'code': False, 'color': 'default'}, 'plain_text': newContent, 'href': None}]}}
        blockurl = "https://api.notion.com/v1/blocks/{}".format(blockID)
        blockResponse = requests.patch(blockurl, json=payload, headers=headers)
        return blockResponse
    except:
        print("something went wrong")
        return -1

def getBlockIdsFromPage(pageID): #returns a list of the blockID's of all the blocks in a page (empty lines are included as blocks)
    try:
        blockurl = "https://api.notion.com/v1/blocks/{}/children?page_size=100".format(pageID)
        blockResponse = requests.get(blockurl, headers=headers)
        jsonBlock = json.loads(blockResponse.text)
        result = []
        for block in jsonBlock["results"]:
            result.append(block["id"])
        return result
    except:
        print("Something went wrong")
        return -1

