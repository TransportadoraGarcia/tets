import asyncio
import time
from collections import deque
from pyrogram import Client, filters

# Configuração das credenciais da conta de usuário
api_id = '24182997'
api_hash = '9371c4dd29bf0056b4acdc6eca0ea7bb'

# Configuração dos IDs dos canais
canal_origem_id = -1001946579778  # ID do canal de origem
canal_destino_id = -1001770622838  # ID do canal de destino

# ID do sticker para separar as mensagens
sticker_id = 'CAACAgEAAxkBAAEhZzxkaWnzf1XxW745DJNgQHITgZQfGAACeQIAAnTEoETK2cGKebH5BS8E'

# Inicialização do cliente do Pyrogram
app = Client("nome_da_sessao", api_id=api_id, api_hash=api_hash)


# Fila para armazenar as mensagens a serem processadas
fila_mensagens = deque()

# Função para adicionar mensagens à fila
def adicionar_mensagem(mensagem):
    fila_mensagens.append(mensagem)

# Função para processar as mensagens da fila
async def processar_fila():
    while True:
        if fila_mensagens:
            mensagem = fila_mensagens.popleft()
            # Obtém a descrição da mensagem, se houver
            descricao = mensagem.caption if mensagem.caption else ""
            
            # Remove todo o conteúdo que envolve o "@"
            if '@' in descricao:
                partes = descricao.split('@')
                if len(partes) > 1:
                    descricao = partes[0].strip() + partes[1][partes[1].find(' '):].strip()
            
            texto = f"{descricao}\nFilme postado no telegram @wfilmes"
            
            # Encaminha a mídia com a descrição modificada para o canal de destino
            if mensagem.photo:
                await app.send_photo(chat_id=canal_destino_id, photo=mensagem.photo.file_id, caption=texto)
            elif mensagem.video:
                await app.send_video(chat_id=canal_destino_id, video=mensagem.video.file_id, caption=texto)
            
            # Envia o sticker para separar as mensagens
            await app.send_sticker(chat_id=canal_destino_id, sticker=sticker_id)
            
            # Exibe uma mensagem no console
            print("Mídia encaminhada com sucesso!")
        
        # Aguarda 5 segundos antes de processar a próxima mensagem
        await asyncio.sleep(300)

# Função para manipular as mensagens recebidas
@app.on_message(filters.chat(canal_origem_id) & (filters.photo | filters.video))
async def encaminhar_mensagem(client, mensagem):
    adicionar_mensagem(mensagem)

# Iniciar o cliente do Pyrogram
app.start()

# Executar a função de processar a fila de forma assíncrona
asyncio.get_event_loop().run_until_complete(processar_fila())

# Parar o cliente do Pyrogram
app.stop()
