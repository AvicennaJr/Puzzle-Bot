"""

A Telegram Puzzle Game

By Mojo
"""

from pyrogram import Client, filters, emoji
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import random


app = Client("puzzle")


##### PUZZLE LOGIC #####

answer_list = ['KEYCAP_DIGIT_ONE','KEYCAP_DIGIT_TWO','KEYCAP_DIGIT_THREE','KEYCAP_DIGIT_FOUR','KEYCAP_DIGIT_FIVE','KEYCAP_DIGIT_SIX','KEYCAP_DIGIT_SEVEN','KEYCAP_DIGIT_EIGHT',"WHITE_LARGE_SQUARE"]
answer_list = [emoji.__getattribute__(e) for e in answer_list]

#output:three rows, three columns
def output(list1):
    
    return f'{list1[0]}\t\t\t{list1[1]}\t\t\t{list1[2]}\n\n\n{list1[3]}\t\t\t{list1[4]}\t\t\t{list1[5]}\n\n\n{list1[6]}\t\t\t{list1[7]}\t\t\t{list1[8]}'
    
#produce a sovable 9-puzzle
def produce_9number():
    
    while True:
        
        list1 = ['KEYCAP_DIGIT_ONE','KEYCAP_DIGIT_TWO','KEYCAP_DIGIT_THREE','KEYCAP_DIGIT_FOUR','KEYCAP_DIGIT_FIVE','KEYCAP_DIGIT_SIX','KEYCAP_DIGIT_SEVEN','KEYCAP_DIGIT_EIGHT',"WHITE_LARGE_SQUARE"]
        list1 = [emoji.__getattribute__(e) for e in list1]
        
        list2 = []
        random.shuffle(list1)
        #to make sure it is solvable, the inverse number must be even
        inverse_number=0
        for i in list1:
            list2.append(i)
        list2.remove(emoji.__getattribute__("WHITE_LARGE_SQUARE"))
        for n in range(7):
            for i in range(n+1,8):
                if list2[n] > list2[i]:
                    inverse_number += 1
        if inverse_number%2 == 0:
            return list1, output(list1)
        #if the inverse number is odd, then reproduce the puzzle
        else:
            continue
       

#tell the computer how to move            
def move(p_number, p_puzzle_number, instruction, list1):
    for i in range(p_puzzle_number):
        if list1[i] == emoji.__getattribute__('WHITE_LARGE_SQUARE'):
            a=i
    if instruction == 'l':
        list1[a],list1[a+1]=list1[a+1],list1[a]
        return output(list1)
    if instruction == 'r':
        list1[a],list1[a-1]=list1[a-1],list1[a]
        return output(list1)
    if instruction == 'u':
        list1[a],list1[a+p_number]=list1[a+p_number],list1[a]
        return output(list1)
    if instruction == 'd':
        list1[a],list1[a-p_number]=list1[a-p_number],list1[a]
        return output(list1)



##### TELEGRAM ####

@app.on_message(filters.command(commands='start'))
async def start(client:Client, message:Message):


    list1, message_output = produce_9number()
    await message.reply(text='`'+message_output+'`',
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Up",
                    callback_data=f"u"
                )
            ],
            [
                InlineKeyboardButton(
                    "Left",
                    callback_data=f"l"
                ),

                InlineKeyboardButton(
                    "Right",
                    callback_data=f"r"
                )
            ],
            [
                InlineKeyboardButton(
                    "Down",
                    callback_data=f"d"
                )
            ]
        ]
    ))


@app.on_callback_query()
async def instruction_move_9(client:Client, query:CallbackQuery):

    
    list1 = query.message.text.split()


    await query.answer()

    instruction = query.data

    if list1[0] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'd' or instruction == 'r':
            return
    if list1[1] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'd':
            return
    if list1[2] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'd' or instruction == 'l':
            return
    if list1[3] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'r':
            return
    if list1[4] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        pass
    if list1[5] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'l':
            return
    if list1[6] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'r' or instruction == 'u':
            return 
    if list1[7] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if instruction == 'u':
            return
    if list1[8] == emoji.__getattribute__("WHITE_LARGE_SQUARE"):
        if list1 == answer_list:
            pass
        else:
            if instruction == 'l' or instruction == 'u':
                return 
    
    await query.edit_message_text(text='`'+move(3,9, instruction, list1)+'`',
    
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Up",
                    callback_data="u"
                )
            ],
            [
                InlineKeyboardButton(
                    "Left",
                    callback_data="l"
                ),

                InlineKeyboardButton(
                    "Right",
                    callback_data="r"
                )
            ],
            [
                InlineKeyboardButton(
                    "Down",
                    callback_data="d"
                )
            ]
        ]))

    if list1 == answer_list:
        await query.edit_message_text(text="Congratulations!")
        return


app.run()