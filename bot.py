from javascript import require, On
import time
import random
mineflayer = require('mineflayer')

allowedChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def getUsername():
    return 'ApostleAuth_' + ''.join(random.choices(allowedChars, k=10))

def connect():
    try:
        username = getUsername()
        bot = mineflayer.createBot({
            'host': '6b6t.org',
            'port': 25565,
            'username': username
        })

        @On(bot, 'spawned')
        def handle_spawned(*args):
            print(f'{username} spawned')
            print(bot.teamMap)

        @On(bot, 'end')
        def handle_end(*args):
            print(f'{username} ended')
            time.sleep(5)
            connect()

        @On(bot, 'kicked')
        def handle_kicked(*args):
            print(f'{username} kicked')
            time.sleep(5)
            connect()
    except Exception as e:
        print(e)
        time.sleep(5)
        connect()

connect()