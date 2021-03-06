# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import time
import telepot
import logging
import urllib.request, json
from money import Money
from telepot.loop import MessageLoop
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.request import urlopen
from telegram.ext import Updater, CommandHandler, Job
from telegram import ParseMode


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Logica para conferir se não existe em todas as 15 posições
checkExist = '[(0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,)]'

def _format_money(price):
    project_money = Money(amount=price, currency='BRL')
    return project_money.format('pt_BR', 'R$ #,##0.00')

# Função que contém o algoritmo para pegar o buffer de PRONACs e fazer conferência se ja existem
def alarm(bot, job):
    # fazendo conexão com banco de dados
    conn=sqlite3.connect('bot.db')
    # Coletando da API do salic as informações dos ultimos PRONCAs
    with urllib.request.urlopen("http://api.salic.cultura.gov.br/v1/projetos/?limit=15&sort=PRONAC:desc&format=json") as url:
        data = json.loads(url.read().decode('utf-8'))
    
    array = ([])
    noticia = data 
    # Colocando os dados recebidos da API em um array 
    for i in range(15):
        array.append(noticia['_embedded']['projetos'][i]['PRONAC'])
    

    posicoes = range(15)

    # Laço feito para conferência se há novidades e então mandar a mensagem do bot
    for x in reversed(posicoes):
        
        linkBotao = str('http://versalic.cultura.gov.br/#/projetos/' + noticia['_embedded']['projetos'][x]['PRONAC'])
        keyboard = [[InlineKeyboardButton("Ver mais detalhes...", callback_data='1',url=linkBotao)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menssagem =  """
        Nova Proposta de #Projeto aceita pelo MinC:

        *Nome*: {nome}

        *Resumo*: {resumo}

        *Cidade*: {cidade} - {estado}  

        *Area*: {area}  

        *Segmento*: {segmento} 

        *Valor*: `{valor_proposta}` 


        Mais sobre a Lei Rouanet em Rouanet.cultura.gov.br



        """.format(
            nome=noticia['_embedded']['projetos'][x]['nome'],
            area=noticia['_embedded']['projetos'][x]['area'],
            segmento=noticia['_embedded']['projetos'][x]['segmento'],
            cidade=noticia['_embedded']['projetos'][x]['municipio'],
            estado=noticia['_embedded']['projetos'][x]['UF'],
            valor_proposta=_format_money(noticia['_embedded']['projetos'][x]['valor_proposta']),
            pronac=noticia['_embedded']['projetos'][x]['PRONAC'],
            resumo=noticia['_embedded']['projetos'][x]['resumo']
            )
        params =  (noticia['_embedded']['projetos'][x]['PRONAC'],)
        
        sql = 'SELECT PRONAC = ? FROM salicBot WHERE cod = 1'
        curs = conn.cursor()
        teste = curs.execute(sql,params)
        teste2 = curs.fetchall()

        # Verificando se existe no Banco
        if checkExist == str(teste2):
            
            bot.sendMessage(job.context, text=menssagem, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    # Laço feito para guardar no banco a ultima atualização da API para criação de um buffer
    for p in posicoes:

        params1 =  (noticia['_embedded']['projetos'][p]['PRONAC'],(p+1))
        sql1 = 'UPDATE salicBot SET PRONAC = ? WHERE id = ?'
        curs = conn.cursor()
        curs.execute(sql1,params1)
        conn.commit()
      

    conn.close()


# Função onde é feita a conta do tempo de quando a função que manda mensagem será chamada
def set(bot, update, job_queue, chat_data):

    chat_id = '@infoNovasRouanet'
    # chat_id = '@projetosMinc'
    #Para usar o bot enviando a mensagem diretamente no bate-papo
    #diretamente para quem mandou a mensagem, utilize o código abaixo.
    # chat_id = update.message.chat_id

    try:
        
        due = 1 #* 60 #essa multiplicação é para tornar em minutos!!!!!
        if due < 0:
            update.message.reply_text('Não podemos ir para o futuro!')
            return

        
        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Agora você receberá os Projetos aprovados do Salic no Canal @infoNovasRouanet')

    except (IndexError, ValueError):
        update.message.reply_text('Use: /start')

def easter(bot, update):
    chat_id = update.message.chat_id
    wut = """
    ────▒▒▒▒▒────▒▒▒▒▒───▄████▄────────
    ─▒─▄▒─▄▒──▒─▄▒─▄▒─███▄█▀─────────
    ─▒▒▒▒▒▒▒─▒▒▒▒▒▒▒▐████──█──█──█─
    ─▒▒▒▒▒▒▒─▒▒▒▒▒▒▒─█████▄────────
    ─▒─▒─▒─▒──▒─▒─▒─▒──▀████▀────────
    """
    bot.sendMessage(chat_id=chat_id, text=wut, parse_mode=ParseMode.MARKDOWN)

def main():

    updater = Updater(os.environ.get('SALIC_BOT_TOKEN'))



    dp = updater.dispatcher



    dp.add_handler(CommandHandler("start", set,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("easter", easter))


    updater.start_polling(timeout=240,clean=False)

    updater.idle()


if __name__ == '__main__':
    main()

