from javascript import require, On
import time
import random
import requests
mineflayer = require('mineflayer')

allowedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

webhook_url = "https://discord.com/api/webhooks/1350822392850546709/pyDfo-aarTvbzWs-rf09a8YRuv7_f7FIXcajAqDO85vj8mT9Rs1GmoZ08UuRurytZKop"

def getUsername():
    return 'Apostle_' + ''.join(random.choices(allowedChars, k=7))

def connect():
    try:
        username = getUsername()
        bot = mineflayer.createBot({
            'host': '6b6t.org',
            'port': 25565,
            'username': username,
            'version': '1.19.4'
        })

        @On(bot, 'spawn')
        def handle_spawned(*args):
            print(f'{username} spawned')
            oldAccsInAuth = []

            while True:
                newAccsInAuth = []
                for i in bot.teamMap:
                    try:
                        if bot.teamMap[i]['color'] == 'white':
                            for member in bot.teamMap[i].membersMap:
                                newAccsInAuth.append(member)
                    except:
                        pass

                for acc in newAccsInAuth:
                    if acc not in oldAccsInAuth:
                        requests.post(webhook_url, json={'content': f'🔑 **{acc}** joined auth server'})

                for acc in oldAccsInAuth:
                    passedAuth = False
                    if acc not in newAccsInAuth:
                        for i in bot.teamMap:
                            try:
                                for j in bot.teamMap[i].membersMap:
                                    if j == acc:
                                        requests.post(webhook_url, json={'content': f'✅ **{acc}** passed auth'})
                                        passedAuth = True
                                        break
                            except:
                                pass
                        if not passedAuth:
                            requests.post(webhook_url, json={'content': f'❌ **{acc}** left auth'})

                oldAccsInAuth = newAccsInAuth
                time.sleep(5)

        @On(bot, 'end')
        def handle_end(*args):
            print(f'{username} ended')
            time.sleep(5)
            connect()

        @On(bot, 'kicked')
        def handle_kicked(*args):
            print(f'{username} kicked')
            print(args)
            time.sleep(5)
            connect()

    except Exception as e:
        print(e)
        time.sleep(5)
        connect()

connect()