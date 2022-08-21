import discord
import os
from ScrappyOL import ScrappyOL
from ScrappyPPS import ScrappyPPS
import json
from discord.ext import tasks

 
client = discord.Client()
global tituloOLD 
tituloOLD = "B\u00fasqueda de Pasantes \u2013 Direcci\u00f3n General de Catastro"


@client.event
async def on_message(message): 
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  
  
  if message.content.startswith(f'$hello'):
    await message.channel.send('Buenas Buenassss,buenos dias grupo......Ahi se va Simon que no festeja la navidad por que su familia es juRia')
    
  '''if f'$search' in message_content:
    ScrappyOL()
    
    ruta = 'ofertas.json'
    with open(ruta) as contenido:
      ofertas = json.load(contenido)

      for oferta in ofertas:
        titulo = oferta["titulo"][0]
        fecha = oferta["fecha"][0]
        descripcion = oferta["descripcion"]
        
        await message.channel.send(titulo)
        await message.channel.send(fecha)
        
        #for des in descripcion:
         # await message.channel.send(des)
      
      await message.channel.send(f'\n═════════════')'''

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
  
  ruta = 'pasantias.json'
  with open(ruta) as contenido:
    
    pasantias = json.load(contenido)
    
    pasantia = pasantias[0]
    titulo = "".join(pasantia["titulo"][0])
    fecha = "".join(pasantia["fecha"][0])
    link = "".join(pasantia["link"][0])
    
    descripcion = pasantia["descripcion"]

    for d in descripcion:
      if ('\u2022' in d):
        des = des + "\n" + d
      elif (':' in d):
        des = des + d + "\n"  
      else:
        des = des + d

    msgPPS = "__**Pasantias y PPS**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"

    await channel.send(msgPPS)
    


@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()

client.run("MTAwNTU3NTE2NDcwMTk2NjM5Nw.GEcqgj.Mjaad4g-s70XGZ0XNNUbIGmNDjDOgUrw5-p7Zk")