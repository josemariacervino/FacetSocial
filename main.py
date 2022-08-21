import discord
import os
from ScrappyOL import ScrappyOL
from ScrappyPPS import ScrappyPPS
import json
from discord.ext import tasks

 
client = discord.Client()

global LastPPS 
LastPPS = "B\u00fasqueda de Pasantes \u2013 Direcci\u00f3n General de Catastro"


@client.event
async def on_message(message):
  global LastPPS
  
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  
  
  if message.content.startswith(f'$hello'):
    await message.channel.send('Buenas Buenassss,buenos dias grupo......Ahi se va Simon que no festeja la navidad por que su familia es juRia')
    
  if f'$search' in message_content:
    await message.channel.send(LastPPS)
    


@tasks.loop(seconds=60)
async def ofertasLaborales():
  
  channel = client.get_channel(1008524480089436261)  
  
  ScrappyOL()
  #sl = '. . . . . . .\n'
  des=""
  
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)

    oferta = ofertas[0]
    titulo = "".join(oferta["titulo"][0])
    fecha = "".join(oferta["fecha"][0])
    link = "".join(oferta["link"][0])
    
    descripcion = oferta["descripcion"]

    for d in descripcion:
      if('\u2022' in d):
        des = des + "\n" + d
      elif (':' in d):
        des = des + d + "\n"
      else:
        des = des + d

    msgOL = "__**Ofertas Laborales**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"

    await channel.send(msgOL)
    


@tasks.loop(seconds=60)
async def pasantias():
  
  channel = client.get_channel(1008524529171185776)  
  
  ScrappyPPS()
  des=""
  global LastPPS 
  
  ruta = 'pasantias.json'
  with open(ruta) as contenido:
    
    pasantias = json.load(contenido)
    
    for pasantia in pasantias:
      pas = pasantia
      titulo = "".join(pas["titulo"])

      if (titulo != LastPPS):
        
        fecha = "".join(pas["fecha"])
        link = "".join(pas["link"])
        descripcion = pas["descripcion"]
    
        for d in descripcion:
          if ('\u2022' in d):
            des = des + "\n" + d
          elif (':' in d):
            des = des + d + "\n"  
          else:
            des = des + d
    
        msgPPS = "__**Pasantias y PPS**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"
    
        await channel.send(msgPPS)

      else:
        pas = pasantias[0]
        titulo = pas["titulo"][0]
        LastPPS = titulo
        break



@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()

client.run("MTAwNTU3NTE2NDcwMTk2NjM5Nw.GEcqgj.Mjaad4g-s70XGZ0XNNUbIGmNDjDOgUrw5-p7Zk")