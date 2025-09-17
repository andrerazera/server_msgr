# %%
# ok bd de mensagens
    # ok remover mensagens ja enviadas
# ok pegar mensagem random
# TODO enviar tgrm
# TODO agendar no serv para enviar td dia
# TODO add mais frases pelo menos 360

# TODO segundo script - rodar de hora em hora com lembretes - relacionar com planilha

# ok anotar como mensagem enviada - salva db


import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import sys
# pip install python-dotenv
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()



agora = datetime.now().isoformat(sep=' ', timespec='seconds')



# %%
# DB
conn = sqlite3.connect('db_msgs.db')  # Arquivo .db será criado no diretório atual
cursor = conn.cursor()

# Criação da tabela com id, numero e timestamp

# 🚨 ADMIN
# limpar tabela 🚨🚨🚨🚨
DROP = False

if DROP == True:

    cursor.execute("""
    DROP TABLE eventos 
    """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_frase INTEGER NOT NULL,
    timestamp TEXT NOT NULL
)
""")

conn.commit()



# %%
# sortear frase a ser enviada


# TODO filtrar frases ja enviadas --------

# Conectar ao banco
# conn = sqlite3.connect('db_msgs.db')

# Ler a tabela como DataFrame
df_msgs_enviadas = pd.read_sql_query("SELECT * FROM eventos", conn)

# # Exibir o DataFrame
# display(df_msgs_enviadas)
# # Fechar conexão
# conn.close()

# ----------------------------------------

# DF de mensagens a sortear
df_msgs = pd.read_csv("db_msgs2.csv", sep=";")

    # filtrar mensagens já enviadas
df_msgs_filtro = df_msgs[~df_msgs['ID'].isin(df_msgs_enviadas['numero_frase'])]


if len(df_msgs_filtro) == 0:
    print("🚨🚨🚨 Acabaram as frases!! 🚨🚨🚨")
    #TODO mandar essa frase no telegram
    sys.exit()

else:
    numero_frase = int(df_msgs_filtro['ID'].sample(1).iloc[0])
    print(f"Frase Sorteada: {numero_frase}")

# %%
len(df_msgs_filtro)

# %%
# output construção da frase 


mensagem = df_msgs[df_msgs['ID'] == numero_frase]['Mensagem'].iloc[0]
autor = df_msgs[df_msgs['ID'] == numero_frase]['Autor/Fonte'].iloc[0]

mensagem_ouput = f"{mensagem} - {autor}"



print(mensagem_ouput)


# TODO envio telegrm



# TODO adicionar as frases enviadas

cursor.execute("INSERT INTO eventos (numero_frase, timestamp) VALUES (?, ?)", (numero_frase, agora))
conn.commit()
# conn.close()
print(f"Registro inserido: frase #{numero_frase} em {agora}")




# %%
# Visualizar no db


# Conectar ao banco
conn = sqlite3.connect('db_msgs.db')

# Ler a tabela como DataFrame
df_msgs_enviadas = pd.read_sql_query("SELECT * FROM eventos", conn)

# Exibir o DataFrame
print(df_msgs_enviadas)
# Fechar conexão
conn.close()

# %%
numero_frase

# %%


# %%
# TODO botar no .env

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# %%
mensagem_ouput

# %%
# enviar a mensagem para o Telegram

from telegram import Bot
import asyncio


### usando notebook:
# bot = Bot(token=TOKEN)
# await bot.send_message(chat_id=CHAT_ID, text=mensagem_ouput)

async def main(): 
    bot = Bot(token=TOKEN) 
    await bot.send_message(chat_id=CHAT_ID, text=mensagem_ouput) 
    
if __name__ == "__main__": asyncio.run(main())







# %%
# async def enviar(texto):
#     async with Bot(TOKEN) as bot:
#         await bot.send_message(chat_id=CHAT_ID, text=mensagem_ouput)

# %%



