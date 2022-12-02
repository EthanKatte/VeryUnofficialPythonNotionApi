import json
import requests
from enum import Enum

class BLOCKTYPE(Enum):
    paragraph = 1
    heading_one = 2
    heading_two = 3
    heading_three = 4
    callout = 5
    quote = 6
    bulleted_list_item = 7
    numbered_list_item = 8
    to_do = 9
    toggle = 10
    code = 11
    child_page = 12
    child_database = 13
    embed = 14
    image = 15
    video = 16
    file = 17
    pdf = 18
    bookmark = 19
    equation = 20
    divider = 21
    table_of_contents = 22
    breadcrumb = 23
    column_List = 24
    column = 25
    link_preview = 26
    template = 27
    link_to_page = 28
    synced_Block = 29
    table = 30
    table_row = 31

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

def updateContentOfParagraphBlock(blockID, newBlockType : str, newContent): #returns the response code of updating the content of a paragraph block in notion - replaces the content of a paragraph block
    newBlockType = newBlockType.lower()
    blockTypeId = BLOCKTYPE.newBlockType.value
    print(blockTypeId)

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


updateContentOfParagraphBlock("27231728271f4a6494969d34979b9c54", "paragraph", "Does this?")
