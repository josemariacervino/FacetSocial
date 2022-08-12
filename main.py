import discord
import os
from ScrappyOL import ScrappyOL
import json
from discord.ext import tasks


client = discord.Client()


@client.event
async def on_message(message): 
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  

  
  if message.content.startswith(f'$hello'):
    await message.channel.send('Buenas Buenassss, buenos dias grupo......Ahi se va Simon que no festeja la navidad por que su familia es juRia')
    
''''  if f'$search' in message_content:
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

'''@tasks.loop(seconds=600)
async def ofertasLaborales():
  
  channel = client.get_channel(695251314459934722)  
  
  ScrappyOL()
  
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)
    
    oferta = ofertas[0]
    titulo = oferta["titulo"][0]
    fecha = oferta["fecha"][0]
    link = oferta["link"][0]
    descripcion = oferta["descripcion"]
    
    await channel.send("**Oferta Laboral**")
    await channel.send(titulo)
    await channel.send(fecha)
    
    for des in descripcion:
      await channel.send(des)
      
    await channel.send("**Ver mas**: "+link)
    await channel.send('══════════════════════════')'''


@tasks.loop(seconds=60)
async def ofertasLaborales():
  
  channel = client.get_channel(695251314459934722)  
  
  ScrappyOL()
  ofertas_a = []
  item = []
  ruta = 'ofertas.json'
  with open(ruta) as contenido:
    
    ofertas = json.load(contenido)
    
    oferta = ofertas
    pub_titulo = oferta["titulo"]
    pub_fecha = oferta["fecha"]
    pub_link = oferta["link"]
    pub_descripcion = oferta["descripcion"]

    ofertas_a.append({
      #'oferta': pub_oferta,
      'titulo': pub_titulo,
      'fecha': pub_fecha,
      'link': pub_link,
      'descripción': pub_descripcion
    }
    )

    item = [
        f"\n'{x['titulo']}'" \
        f"\nIr a la publicación: '{x['link']}" \
        #f"'\nURL en la publicación: '{x['url dentro de la publicacion']}'"
        f"\n {x['descripción']}" \
        f" Publicado el {x['fecha']}" \
        f"══════════════════════════\n"
        for x in ofertas_a]

    

    #await channel.send("*Oferta Laboral*")
    await channel.send(item)


@client.event
async def on_ready():
  print(f'{client.user} is now online!')
  ofertasLaborales.start()

client.run("MTAwNTU3NTE2NDcwMTk2NjM5Nw.GEcqgj.Mjaad4g-s70XGZ0XNNUbIGmNDjDOgUrw5-p7Zk")