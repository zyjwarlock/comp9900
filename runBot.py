# created by z5089986 

import app.reply as rp

if __name__ == '__main__':
    while True:
        msg = input("you > : ")
        if(msg == '/quit'): quit()

        reply = rp.reply(msg)
        print("Bot > : ", reply)
