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


def sendMessage(message, id, accesToken=''):
    url = "https://broadcast.vkforms.ru/api/v2/broadcast"

    querystring = {"token": "api_31719_5ySe6b44dlTdEfzMaES2T8G8", "list_ids": id, "run_now": "1"}

    payload = "{\n\t\"message\" : {\n\t\t\"attachment\" : [\"" + message + "\"]\n\t}\n}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fc8f2323-3e2a-b996-b0b1-76a207694541"
    }

    requests.request("POST", url, data=payload, headers=headers, params=querystring)


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
            if postText.find("#волонтерство@dobroboard_spb") > 0 or postText.find("#ДоброБорд") > 0 or \
                            postText.find("#ДоброBoard") > 0:
                sendMessage(message="wall" + postId, id="375629", accesToken=session.access_token)
                time.sleep(1)
            if postText.find("#конкурс@dobroboard_spb") > 0:
                sendMessage(message="wall" + postId, id="386268", accesToken=session.access_token)
                time.sleep(1)
            if postText.find("#событие@dobroboard_spb") > 0:
                sendMessage(message="wall" + postId, id="386269", accesToken=session.access_token)
                time.sleep(1)


def main():
    session = vk.AuthSession('5988829', '79163064478', 'popapopa', scope='wall,photos')
    vk_api = vk.API(session)
    i = 0
    while True:
        i = i + 1
        try:
            if i % 16 == 15:
                vk_api.wall.post(owner_id='465137130', message='work', v=5.52)
            getNewPostsId(vk_api, session)
            time.sleep(300)
        except:
            pass





if __name__ == '__main__':
    main()
