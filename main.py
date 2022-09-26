import os
import discord
from ScrappyOL import ScrappyOL
from ScrappyOL import ScrappyOLInicial
from ScrappyPPS import ScrappyPPS
from ScrappyPPS import ScrappyPPSInicial
from ScrappyProcesadores import ScrappyProcesadores
from ScrappyProcesadores import ScrappyProcesadoresInicial
from ScrappyTD import ScrappyTD
from ScrappyTD import ScrappyTDInicial
import json
from discord.ext import tasks

 
client = discord.Client()


#Variables globales que almacenan el titulo y fecha de la ultima publicacion
global ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes
global ultimaOLId,ultimaOLTitulo,ultimaOLDes
global ultimaNovedadProcesadores
global ultimaNovedadTD

ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes = "","",""
ultimaOLId,ultimaOLTitulo,ultimaOLDes = "","",""
ultimaNovedadProcesadores=""
ultimaNovedadTD=""



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
    await message.channel.send(ultimaPPSId+"\n"+ultimaPPSTitulo+"\n"+ultimaPPSDes)
    await message.channel.send("__**Ultima Oferta Laboral:**__")
    await message.channel.send(ultimaOLId+"\n"+ultimaOLTitulo+"\n"+ultimaOLDes)
    #await message.channel.send("__**Ultima Novedad de Sist. con Microprocesadores:**__")
    #await message.channel.send(ultimaNovedadProcesadores)
    #await message.channel.send("__**Ultima Novedad de Transmisiones de Datos:**__")
    #await message.channel.send(ultimaNovedadTD)

#################
#Funcion para revisar y publicar las ultimas Ofertas Laborales publicadas (cada 30min)
#################

@tasks.loop(seconds=1800)
async def ofertasLaborales():
  
  #Canal de la FACET Social Maqueta
  #channel = client.get_channel(903258671138627605)
  #Canal de JoMaGo
  channel = client.get_channel(1008524480089436261)   

  #Ejecuta Scrappy de OL
  ScrappyOL()
  des=""
  global ultimaOLId,ultimaOLTitulo,ultimaOLDes

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)

    for oferta in ofertas:
      des=""
      of = oferta
      id = "".join(of["id"])
      titulo = "".join(of["titulo"])
      fecha = "".join(of["fecha"])
      link = "".join(of["link"])
      descripcion = of["descripcion"][0]

      for d in descripcion:
        if ('\n\u2022' in d):
          des = des + d.strip("\t")
        elif ('\u2022' in d):
          des = des + "\n" + d.strip("\t")
        elif ('\u27a2' in d):
          des = des + "\n" + d.strip("\t")
        elif ('\n' in d):
          #des = des + "\n" + d.strip("\t")
          des = des + d.strip("\t")
        elif (':' in d):
          des = des + d.strip("\t") + "\n"
        else:
          des = des + d.strip("\t")
        
      msgOL = "__**Ofertas Laborales**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"

      
      if(id == ultimaOLId):
        if(titulo == ultimaOLTitulo):
          if(des == ultimaOLDes):
            break
          else:
            await channel.send(msgOL)
            ultimaOLId,ultimaOLTitulo,ultimaOLDes = ScrappyOLInicial()
            break
        else:
          await channel.send(msgOL)
          ultimaOLId,ultimaOLTitulo,ultimaOLDes = ScrappyOLInicial()
          break
      else:
        await channel.send(msgOL)  


#################
#Funcion para revisar y publicar las ultimas Pasantias publicadas (cada 30min)
#################
@tasks.loop(seconds=1800)
async def pasantias():
  
  #Canal de la FACET Social Maqueta
  #channel = client.get_channel(903258541207466034)
  #Canal de JoMaGo
  channel = client.get_channel(1008524529171185776)  

  #Ejecuta Scrappy de PPS
  ScrappyPPS()
  des=""
  global ultimaPPSTitulo,ultimaPPSId,ultimaPPSDes

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'pasantias.json'
  with open(ruta) as contenido:
    
    pasantias = json.load(contenido)
    
    for pasantia in pasantias:
      des=""
      pas = pasantia
      id = "".join(pas["id"])
      titulo = "".join(pas["titulo"])
      fecha = "".join(pas["fecha"])
      link = "".join(pas["link"])
      descripcion = pas["descripcion"][0]
      
      for d in descripcion:
        if ('\n\u2022' in d):
          des = des + d.strip("\t")
        elif ('\u2022' in d):
          des = des + "\n" + d.strip("\t")
        elif ('\u27a2' in d):
          des = des + "\n" + d.strip("\t")
        elif ('\n' in d):
          #des = des + "\n" + d.strip("\t")
          des = des + d.strip("\t")
        elif (':' in d):
          des = des + d.strip("\t") + "\n"
        else:
          des = des + d.strip("\t")

      
      msgPPS = "__**Pasantias y PPS**__\n\n"+"**"+titulo+"**"+" \n"+fecha+" \n\n"+des+" \n\n"+"***Ver mas:  ***"+link+" \n\n"+"═════════════════"

      
      if(id == ultimaPPSId):
        if(titulo == ultimaPPSTitulo):
          if(des == ultimaPPSDes):
            break
          else:
            await channel.send(msgPPS)
            ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes = ScrappyPPSInicial()
            break
        else:
          await channel.send(msgPPS)
          ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes = ScrappyPPSInicial()
          break
      else:
        await channel.send(msgPPS)
            


#################
#Funcion para revisar y publicar las ultimas novedades publicadas de Microprocesadoes (cada 15min)
#################
@tasks.loop(seconds=900)
async def novedadesProcesarores():

  #Canal de la FACET Social Maqueta
  #channel = client.get_channel(1016006450004361226)
  #Canal de JoMaGo
  channel = client.get_channel(1016006787796832266)

  #Ejecuta Scrappy de Procesadores
  ScrappyProcesadores()
  global ultimaNovedadProcesadores

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'novedadesProcesadores.json'
  with open(ruta) as contenido:
    
    novedades = json.load(contenido)
    
    for novedad in novedades:
      nov = novedad
      fecha = "".join(nov["fecha"])
      descripcion = "".join(nov["descripcion"][0])
          
      msgProcesadores = "📢 __**Nueva publicación**__\n\n"+descripcion+"**\n\nFecha: **"+fecha+"\n\n\n🔗 __**Links de Secciones:**__\n\n"+"***-📰 Cartelera de Novedades:***\n"+"https://microprocesadores.unt.edu.ar/procesadores/"+"\n***-📚 Diapositivas:***\n"+"https://microprocesadores.unt.edu.ar/procesadores/downloads/type/0/"+"\n***-📝 Prácticos/Laboratorios:***\n"+"https://microprocesadores.unt.edu.ar/procesadores/downloads/assignments/"+" \n\n"+"═════════════════"
    
      if(descripcion != ultimaNovedadProcesadores):
        await channel.send(msgProcesadores)
      else:
        nov = novedades[0]
        descripcion = "".join(nov["descripcion"][0])
        ultimaNovedadProcesadores = descripcion
        break




#################
#Funcion para revisar y publicar las ultimas novedades publicadas de Trans. de Datos (cada 15min)
#################
@tasks.loop(seconds=960)
async def novedadesTD():

  #Canal de la FACET Social Maqueta
  #channel = client.get_channel(1016424481322979328)
  #Canal de JoMaGo
  channel = client.get_channel(1016424348694876231)

  #Ejecuta Scrappy de Trans. de Datos
  ScrappyTD()
  global ultimaNovedadTD

  #Lee el archivo y publicar publicaciones nuevas si es que hay
  ruta = 'novedadesTD.json'
  with open(ruta) as contenido:
    
    novedades = json.load(contenido)
    
    for novedad in novedades:
      nov = novedad
      fecha = "".join(nov["fecha"])
      descripcion = "".join(nov["descripcion"][0])
          
      msgTD = "📢 __**Nueva publicación**__\n\n"+descripcion+"**\n\nFecha: **"+fecha+"\n\n\n🔗 __**Links de Secciones:**__\n\n"+"***-📰 Cartelera de Novedades:***\n"+"https://microprocesadores.unt.edu.ar/transmision/"+"\n***-📚 Diapositivas:***\n"+"https://microprocesadores.unt.edu.ar/transmision/downloads/type/0/"+"\n***-📝 Prácticos/Laboratorios:***\n"+"https://microprocesadores.unt.edu.ar/transmision/downloads/assignments/"+" \n\n"+"═════════════════"
    
      if (descripcion != ultimaNovedadTD):
        await channel.send(msgTD)
      else:
        nov = novedades[0]
        descripcion = "".join(nov["descripcion"][0])
        ultimaNovedadTD = descripcion
        break

        
        
#################
#Funcion inicial del servicio, inicia el bot y funciones
#################


@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()
  pasantias.start()
  #novedadesProcesarores.start()
  #novedadesTD.start()

  global ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes
  global ultimaOLId,ultimaOLTitulo,ultimaOLDes
  global ultimaNovedadProcesadores
  global ultimaNovedadTD
  
  ultimaPPSId,ultimaPPSTitulo,ultimaPPSDes = ScrappyPPSInicial()
  ultimaOLId,ultimaOLTitulo,ultimaOLDes = ScrappyOLInicial()
  #ultimaNovedadProcesadores = ScrappyProcesadoresInicial()
  #ultimaNovedadTD = ScrappyTDInicial()
  

#################
#Token del bot de Discord "UBICAR EN OTRO LUGAR"
#################
client.run(os.environ["FACETSOCIAL_TOKEN"])