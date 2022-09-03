import os
import discord
from ScrappyOL import ScrappyOL
from ScrappyOL import ScrappyOLInicial
from ScrappyPPS import ScrappyPPS
from ScrappyPPS import ScrappyPPSInicial
import json
from discord.ext import tasks

 
client = discord.Client()


#Variables globales que almacenan el titulo y fecha de la ultima publicacion
global ultimaPPSTitulo
global ultimaPPSFecha
global ultimaOLTitulo
global ultimaOLFecha
ultimaPPSTitulo = ""
ultimaPPSFecha = ""
ultimaOLTitulo = ""
ultimaOLFecha = ""


#################
#Funcion "event", respuesta a la interaccion del usuario "hello","latest"
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

  #Para el msj: $latest
  if f'$latest' in message_content:
    await message.channel.send("__**Ultima Pasatia y PPS:**__")
    await message.channel.send(ultimaPPSTitulo)
    await message.channel.send(ultimaPPSFecha)
    await message.channel.send("__**Ultima Oferta Laboral:**__")
    await message.channel.send(ultimaOLTitulo)
    await message.channel.send(ultimaOLFecha)
  

#################
#Funcion para revisar y publicar las ultimas Ofertas Laborales publicadas (cada 30min)
#################

@tasks.loop(seconds=1800)
async def ofertasLaborales():
  
  channel = client.get_channel(1008524480089436261)  

  #Ejecuta Scrappy de OL
  ScrappyOL()
  des=""
  global ultimaOLTitulo
  global ultimaOLFecha

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)

    for oferta in ofertas:
      of = oferta
      titulo = "".join(of["titulo"])
      fecha = "".join(of["fecha"])
      link = "".join(of["link"])
      fechaS = "".join(of["fechaScrappy"])
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
      
      if (titulo != ultimaOLTitulo):
        await channel.send(msgOL)
      elif (titulo == ultimaOLTitulo and fechaS > ultimaOLFecha):
        await channel.send(msgOL)
      else:
        of = ofertas[0]
        titulo = of["titulo"][0]
        fechaS = of["fechaScrappy"][0]
        ultimaOLTitulo = titulo
        ultimaOLFecha = fechaS
        break
    


#################
#Funcion para revisar y publicar las ultimas Pasantias publicadas (cada 30min)
#################
@tasks.loop(seconds=1800)
async def pasantias():
  
  channel = client.get_channel(1008524529171185776)  

  #Ejecuta Scrappy de PPS
  ScrappyPPS()
  des=""
  global ultimaPPSTitulo 
  global ultimaPPSFecha 

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'pasantias.json'
  with open(ruta) as contenido:
    
    pasantias = json.load(contenido)
    
    for pasantia in pasantias:
      pas = pasantia
      titulo = "".join(pas["titulo"])
      fecha = "".join(pas["fecha"])
      link = "".join(pas["link"])
      fechaS = "".join(pas["fechaScrappy"])
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

      if (titulo != ultimaPPSTitulo):
        await channel.send(msgPPS)
      elif (titulo == ultimaPPSTitulo and fechaS > ultimaPPSFecha):
        await channel.send(msgPPS)
      else:
        pas = pasantias[0]
        titulo = pas["titulo"][0]
        fechaS = pas["fechaScrappy"][0] 
        ultimaPPSTitulo = titulo
        ultimaPPSFecha = fecha
        break


        
#################
#Funcion inicial del servicio, inicia el bot, funciones y corre scrappy para obtener titulo de la ultima publicacion de OL y PPS
#################

@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()

  global ultimaPPSTitulo
  global ultimaPPSFecha
  ultimaPPSTitulo, ultimaPPSFecha = ScrappyPPSInicial()
  global ultimaOLTitulo
  global ultimaOLFecha
  ultimaOLTitulo, ultimaOLFecha = ScrappyOLInicial()
  
  

#################
#Token del bot de Discord "UBICAR EN OTRO LUGAR"
#################
client.run(os.environ["FACETSOCIAL_TOKEN"])