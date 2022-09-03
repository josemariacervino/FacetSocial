import os
import discord
from ScrappyOL import ScrappyOL
from ScrappyOL import ScrappyOLInicial
from ScrappyPPS import ScrappyPPS
from ScrappyPPS import ScrappyPPSInicial
import json
from discord.ext import tasks

 
client = discord.Client()


#Variables globales que almacenan el titulo de la ultima publicacion
global ultimaPPS
global ultimaOL
ultimaPPS = ""
ultimaOL = ""

#################
#Funcion "event", respuesta a la interaccion del usuario "hello","search"
#################
@client.event
async def on_message(message):
  
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  

  #Para el msj: $hello
  if message.content.startswith(f'$hello'):
    await message.channel.send('Buenos dias, soy un Bot que te mantiene al tanto de las ultimas noticias!!')

  #Para el msj: $search
  if f'$search' in message_content:
    await message.channel.send("Ultima Pasatia y PPS:")
    await message.channel.send(ultimaPPS)
    await message.channel.send("Ultima Oferta Laboral:")
    await message.channel.send(ultimaOL)
  

#################
#Funcion para revisar y publicar las ultimas Ofertas Laborales publicadas (cada 30min)
#################
@tasks.loop(seconds=1800)
async def ofertasLaborales():
  
  channel = client.get_channel(903258671138627605)  

  #Ejecuta Scrappy de OL
  ScrappyOL()
  des=""
  global ultimaOL

  #Lee el archivo y publicar publicaciones nuevas si es que hay
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
    


#################
#Funcion para revisar y publicar las ultimas Pasantias publicadas (cada 30min)
#################
@tasks.loop(seconds=1800)
async def pasantias():
  
  channel = client.get_channel(903258541207466034)  

  #Ejecuta Scrappy de PPS
  ScrappyPPS()
  des=""
  global ultimaPPS 

  #Lee el archivo y publicar publicaciones nuevas si es que hay
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


        
#################
#Funcion inicial del servicio, inicia el bot, funciones y corre scrappy para obtener titulo de la ultima publicacion de OL y PPS
#################
@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()

  global ultimaPPS
  ultimaPPS = ScrappyPPSInicial()
  global ultimaOL
  ultimaOL = ScrappyOLInicial()
  
  

#################
#Token del bot de Discord "UBICAR EN OTRO LUGAR"
#################
client.run(os.environ["FACETSOCIAL_TOKEN"])