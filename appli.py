#!/usr/bin/env python3
from ctypes import wintypes
from unicodedata import name
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import os 
import logging
import time


#Connexion aux API
url = "https://api.rust-servers.info/status/4116"
url2 = "https://api.rust-servers.info/info/4116"

#Requetes API
reponse = requests.get(url)
reponse2 = requests.get(url2)

#Recuperer contenu API
contenu = reponse.json()
contenu2 = reponse2.json()

print(contenu2)

#Creation variables
nom = contenu["name"]
statut = contenu["status"]
joueurs = contenu["players"]
max = contenu["players_max"]
fps = contenu["fps"]
uptime = '0'
mapsize = contenu2['size']
mode = contenu2['server_mode']
cycle = contenu2['wipe_cycle']
image = contenu2['image']
link = contenu2['url']
seed = contenu2['seed']
ip = contenu2['ip']

#Affichage de la map en direct
api_endpoint = "https://rustmaps.com/api/v2/maps/"+seed+"/"+mapsize

CAT_API_KEY = os.environ.get("a5be2d75-973e-48d3-b7b0-5356e287f376")

headers = {
    "x-api-key" : "a5be2d75-973e-48d3-b7b0-5356e287f376"
}
response = requests.get(
    api_endpoint,
    headers = headers
)

map = response.json()

preview = map['imageIconUrl']

#Fichier log

logging.basicConfig(filename='wipe.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info(nom + " - " + statut + " - " + joueurs + " joueurs - " + fps + " ping - " + uptime + " secondes depuis le dernier wipe - " + mapsize + "x" 
+ mapsize + " - " + seed + " map seed - " + mode + " - " + cycle)


#Connexion au webhook
webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/932624652533108776/x20k5XUbiaLfxcm21anDYFh0bBCZyNB6i5Hq1WDlF2mQiz0P_npjViDdyTttluIFNoAj", username="Bot wipe")

#Message discord
embed = DiscordEmbed(
    title=nom, description="Viens tout juste de wipe !", color='CD412B'
)
embed.set_author(
    name="WIPE RECENT !",
    url=link,
    icon_url='https://i.pinimg.com/originals/cc/40/6a/cc406a8382d8df7eb5f395ec884d3c95.png',
)
embed.set_image(url=preview,inline=False)
embed.set_footer(text="Yohann gach")
embed.set_timestamp()
embed.add_embed_field(name="Statut", value=statut)
embed.add_embed_field(name="Joueurs", value=joueurs+"/"+max)
embed.add_embed_field(name="Ping", value=fps)
embed.add_embed_field(name="Wipe depuis", value=uptime+" Secondes")
embed.add_embed_field(name="Map", value=mapsize+"x"+mapsize)

webhook.add_embed(embed)

#Boucle 
while True:
  if uptime == '0':
    response = webhook.execute()
    print('Notif discord envoyée')
    break
  else:
    print('pas de wipe récent')
    time.sleep(300) 

