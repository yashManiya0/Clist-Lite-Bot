# import all the commands from dot.py file located in the same directory
import bot

def test_clear(n):
    try:
        bot.clear(n)
    except:
        raise Exception()
    else:
        print('No errors, code ran perfectly')
    

def test_register(discord_mem, handle):
    try:
        bot.register(discord_mem, handle)
    except:
        raise Exception()
    else:
        print('No errors, code ran perfectly')


def test_userinfo(handle):
    try:
        bot.userinfo(handle)
    except:
        raise Exception()
    else:
        print('No errors, code ran perfectly')

def test_stalk(handle):
    try:
        bot.stalk(handle)
    except:
        raise Exception('an unexpected error occurred') # this error may occur due to Codeforces API
    else:
        print('No errors, code ran perfectly')

def test_clist():
    try:
        bot.clist()
    except:
        raise Exception()
    else:
        print('No errors, code ran perfectly')