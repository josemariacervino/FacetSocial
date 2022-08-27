import discord
import os
from ScrappyOL import ScrappyOL
from ScrappyOL import ScrappyOLInicial
from ScrappyPPS import ScrappyPPS
from ScrappyPPS import ScrappyPPSInicial
import json
from discord.ext import tasks

 
client = discord.Client()

global ultimaPPS 
ultimaPPS = ""

global ultimaOL
ultimaOL = ""


@client.event
async def on_message(message):
  global ultimaPPS
  
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  
  
  if message.content.startswith(f'$hello'):
    await message.channel.send('Buenos dias, soy un Bot que te mantiene al tanto de las ultimas noticias!!')
    
  if f'$search' in message_content:
    await message.channel.send("Ultima Pasatia y PPS:")
    await message.channel.send(ultimaPPS)
    await message.channel.send("Ultima Oferta Laboral:")
    await message.channel.send(ultimaOL)
    

@tasks.loop(seconds=1800)
async def ofertasLaborales():
  
  channel = client.get_channel(1008524480089436261)  
  
  ScrappyOL()
  des=""
  global ultimaOL
  
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)

    for oferta in ofertas:
      of = oferta
      titulo = "".join(of["titulo"])

      if (titulo != ultimaOL):
        
        fecha = "".join(of["fecha"])
        link = "".join(of["link"])
        descripcion = of["descripcion"]
    
        for d in descripcion:
          if('\u2022' in d):
            des = des + "\n" + d
          elif (':' in d):
            des = des + d + "\n"
          else:
            des = des + d
    
        msgOL = "__**Ofertas Laborales**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"

        
        des=""
        await channel.send(msgOL)

      else:
        of = ofertas[0]
        titulo = of["titulo"][0]
        ultimaOL = titulo
        break
    




@tasks.loop(seconds=1800)
async def pasantias():
  
  channel = client.get_channel(1008524529171185776)  
  
  ScrappyPPS()
  des=""
  global ultimaPPS 
  
  ruta = 'pasantias.json'
  with open(ruta) as contenido:
    
    pasantias = json.load(contenido)
    
    for pasantia in pasantias:
      pas = pasantia
      titulo = "".join(pas["titulo"])

      if (titulo != ultimaPPS):
        
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
    
        des=""
        await channel.send(msgPPS)

      else:
        pas = pasantias[0]
        titulo = pas["titulo"][0]
        ultimaPPS = titulo
        break



@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()

  global ultimaPPS
  ultimaPPS = ScrappyPPSInicial()
  global ultimaOL
  ultimaOL = ScrappyOLInicial()
  
  


client.run("MTAwNTU3NTE2NDcwMTk2NjM5Nw.GEcqgj.Mjaad4g-s70XGZ0XNNUbIGmNDjDOgUrw5-p7Zk")