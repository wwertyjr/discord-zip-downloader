import discord
import os
import aiohttp

from discord.ext import commands

TOKEN = 'TU TOKEN'  # Reemplaza con el token de tu bot
CHANNEL_NAME = 'CANAL'  # Reemplaza con el nombre del canal donde deseas que funcione el comando
DOWNLOAD_PATH = 'archivos/'  # Directorio donde se guardarán los archivos ZIP descargados

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=',', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot iniciado como {bot.user.name}')

def get_unique_filename(file_path):
    if not os.path.exists(file_path):
        return file_path

    base_name, extension = os.path.splitext(file_path)
    counter = 1
    while os.path.exists(file_path):
        new_file_name = f'{base_name} ({counter}){extension}'
        file_path = os.path.join(DOWNLOAD_PATH, new_file_name)
        counter += 1
    return file_path

@bot.command()
async def escanear(ctx):
    if ctx.channel.name == CHANNEL_NAME:
        num_zips = 0
        message = None
        
        async for msg in ctx.channel.history(limit=None):
            for attachment in msg.attachments:
                if attachment.filename.endswith('.zip'):
                    file_name = attachment.filename
                    file_path = os.path.join(DOWNLOAD_PATH, file_name)
                    
                    # Genera un nombre de archivo único si es necesario
                    file_path = get_unique_filename(file_path)
                    
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                data = await resp.read()
                                with open(file_path, 'wb') as f:
                                    f.write(data)
                                num_zips += 1
                                
                                # Muestra información en la consola
                                print(f'Archivo ZIP "{file_name}" descargado en "{file_path}".')
                                
                                # Actualiza el mensaje embed con la cantidad de archivos descargados
                                embed = discord.Embed(title="Archivos ZIP Descargados",
                                                      description=f"Se han descargado {num_zips} archivos ZIP.",
                                                      color=0x00ff00)  # Puedes personalizar el color
                                
                                # Envía el mensaje embed inicial o actualizado
                                if not message:
                                    message = await ctx.send(embed=embed)
                                else:
                                    await message.edit(embed=embed)

bot.run(TOKEN)
