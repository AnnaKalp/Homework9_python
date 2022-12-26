# Создайте программу для игры в ""Крестики-нолики"" при помощи виртуального
# окружения и PIP.


import os
import random
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

import strings as st
print("Server start")

def getToken():
    token = ''
    if os.path.isfile(st.BOT_TOKEN_FILENAME):
        f = open(st.BOT_TOKEN_FILENAME, "r")
        token = f.read()
        f.close()
    else:
        print("Создайте файл 'token.txt' и поместите туда токен")
        sys.exit()  
    return token

def isWin(arr, whoWin):
    if (((arr[0] == whoWin) and (arr[4] == whoWin) and (arr[8] == whoWin)) or
            ((arr[2] == whoWin) and (arr[4] == whoWin) and (arr[6] == whoWin)) or
            ((arr[0] == whoWin) and (arr[1] == whoWin) and (arr[2] == whoWin)) or
            ((arr[3] == whoWin) and (arr[4] == whoWin) and (arr[5] == whoWin)) or
            ((arr[6] == whoWin) and (arr[7] == whoWin) and (arr[8] == whoWin)) or
            ((arr[0] == whoWin) and (arr[3] == whoWin) and (arr[6] == whoWin)) or
            ((arr[1] == whoWin) and (arr[4] == whoWin) and (arr[7] == whoWin)) or
            ((arr[2] == whoWin) and (arr[5] == whoWin) and (arr[8] == whoWin))):
        return True
    return False

def finedCells(cellArray):
    counter = 0
    for i in cellArray:
        if i == st.SYMBOL_UNDEF:
            counter += 1
    return counter

def game(callBackData):
    message = st.ANSW_YOUR_TURN  
    alert = None

    buttonNumber = int(callBackData[0])  
    if not buttonNumber == 9:  
        charList = list(callBackData)  
        charList.pop(0)
        if charList[buttonNumber] == st.SYMBOL_UNDEF:  
            charList[buttonNumber] = st.SYMBOL_X  
            if isWin(charList, st.SYMBOL_X):
                message = st.ANSW_YOU_WIN
            else:  
                if finedCells(charList) != 0:  
            
                    isCycleContinue = True
                    while (isCycleContinue):
                        rand = random.randint(0, 8)  
                        if charList[rand] == st.SYMBOL_UNDEF:  
                            charList[rand] = st.SYMBOL_O
                            isCycleContinue = False 
                            if isWin(charList, st.SYMBOL_O):  
                                message = st.ANSW_BOT_WIN

        else:
            alert = st.ALERT_CANNOT_MOVE_TO_THIS_CELL
        if finedCells(charList) == 0 and message == st.ANSW_YOUR_TURN:
            message = st.ANSW_DRAW
 
        callBackData = ''
        for c in charList:
            callBackData += c
    if message == st.ANSW_YOU_WIN or message == st.ANSW_BOT_WIN or message == st.ANSW_DRAW:
        message += '\n'
        for i in range(0, 3):
            message += '\n | '
            for j in range(0, 3):
                message += callBackData[j + i * 3] + ' | '
        callBackData = None  

    return message, callBackData, alert

def getKeyboard(callBackData):
    keyboard = [[], [], []]  

    if callBackData != None:  
        for i in range(0, 3):
            for j in range(0, 3):
                keyboard[i].append(InlineKeyboardButton(callBackData[j + i * 3], callback_data=str(j + i * 3) + callBackData))

    return keyboard

def newGame(update, _):
    data = ''
    for i in range(0, 9):
        data += st.SYMBOL_UNDEF
    
    update.message.reply_text(st.ANSW_YOUR_TURN, reply_markup=InlineKeyboardMarkup(getKeyboard(data)))

def button(update, _):
    query = update.callback_query
    callbackData = query.data  

    message, callbackData, alert = game(callbackData) 
    if alert is None:  
        query.answer()   
        query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(getKeyboard(callbackData)))
    else:  
        query.answer(text=alert, show_alert=True)

def help_command(update, _):
    update.message.reply_text(st.ANSW_HELP)

if __name__ == '__main__':
    updater = Updater(getToken())  

    updater.dispatcher.add_handler(CommandHandler('start', newGame))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, help_command))  
    updater.dispatcher.add_handler(CallbackQueryHandler(button)) 

    updater.start_polling()
    updater.idle()