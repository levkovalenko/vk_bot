import requests
import vk
import time


def getSomeId(SomeFile):
    fileSomeId = open(SomeFile, 'r')
    someId = []
    for line in fileSomeId.readlines():
        someId.append(line[0:-1])
    return someId


def putNewPosts(newPosts):
    fileExistedPosts = open("ExistedPosts.txt", 'a')
    for postId in newPosts:
        fileExistedPosts.write(postId + '\n')


def sendMessage(message, accesToken=''):
    url = "https://broadcast.vkforms.ru/api/v2/broadcast"

    querystring = {"token": "api_31326_SzwsTxLtFT1B8brORL6OcawI", "list_ids": "371921", "run_now": "1"}

    payload = "{\n\t\"message\" : {\n\t\t\"attachment\" : [\"" + message + "\"]\n\t}\n}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fc8f2323-3e2a-b996-b0b1-76a207694541"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)


def getNewPostsId(vkApi, session):
    groupsId = getSomeId("GroupsId.txt")
    existedPosts = getSomeId("ExistedPosts.txt")
    keyWords = getSomeId("KeyWords.txt")
    for groupId in groupsId:
        posts = vkApi.wall.get(owner_id=groupId, v=5.52, count=10)['items']
        for post in posts:
            postId = groupId + '_' + str(post['id'])
            new = True
            for id in existedPosts:
                if id == postId:
                    new = False
            postText = post['text'].lower()
            if new:
                putNewPosts([str(postId)])
            else:
                continue
            counter = 0
            for word in keyWords:
                if postText.find(word) > 0:
                    counter += 1
            if counter > 9:
                sendMessage(message="wall" + postId, accesToken=session.access_token)
                # vkApi.wall.repost(object='wall'+postId, v=5.52)
                time.sleep(1)


def main():
    # https://api.vk.com/method/wall.get?owner_id=-30666517&v=5.52

    session = vk.AuthSession('5988829', '79163064478', 'popapopa', scope='wall,photos')
    vk_api = vk.API(session)
    getNewPostsId(vk_api, session)


# print(vk_api.wall.repost(object='wall-154469416_51', v=5.52))



# sendMessage(message="dfhfавпапот", accesToken=session.access_token)
if __name__ == '__main__':
    main()
