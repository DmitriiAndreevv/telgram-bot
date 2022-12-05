import telebot
import random
from telebot import types
import config
from game import get_map_cell



bot = telebot.TeleBot(config.Token)




cols, rows = 5, 5

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('🠔', callback_data = 'left'),
             telebot.types.InlineKeyboardButton('🠕', callback_data = 'up'),
             telebot.types.InlineKeyboardButton('🠗', callback_data = 'down'),
             telebot.types.InlineKeyboardButton('🠖', callback_data = 'right') )

maps = {}

def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y *(cols * 2 - 1)]:
                map_str += "🟪"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "🔲"
        map_str += "\n"

    return map_str

@bot.message_handler(commands=['play'])
def play_message(message):
	map_cell = get_map_cell(cols, rows)

	user_data = {
		'map': map_cell,
		'x': 0,
		'y': 0
	}

	maps[message.chat.id] = user_data

	bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
	user_data = maps[query.message.chat.id]
	new_x, new_y = user_data['x'], user_data['y']

	if query.data == 'left':
		new_x -= 1
	if query.data == 'right':
		new_x += 1
	if query.data == 'up':
		new_y -= 1
	if query.data == 'down':
		new_y += 1

	if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
		return None
	if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
		return None

	user_data['x'], user_data['y'] = new_x, new_y

	if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
		bot.edit_message_text( chat_id=query.message.chat.id,
							   message_id=query.message.id,
							   text="Вы выиграли,Ура!!!" )
		return None

	bot.edit_message_text( chat_id=query.message.chat.id,
						   message_id=query.message.id,
						   text=get_map_str(user_data['map'], (new_x, new_y)),
						   reply_markup=keyboard )

# bot.polling(none_stop=False, interval=0)





@bot.message_handler(commands=['start'])
def welcome(message):
    stik = open('stickers/Deadpool.webp', 'rb')
    bot.send_sticker(message.chat.id, stik)



    #клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("🎲 Рандомное число")


    markup.add(item)



    bot.send_message(message.chat.id, 'Приветствую тебя, {0.first_name}!\nДобро пожаловать,\nЯ - <b>{1.first_name}</b>, бот созданный для развлечения!'.format(message.from_user, bot.get_me()),
    parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def botmes(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
            if message.chat.type == '🏆 Начнем игру 🏆':
                bot.send_message(message.chat.id,'_')
        elif message.text == 'Привет':
            bot.send_message(message.chat.id, 'ПРИВЕТ 🙃')
        elif message.text =='Как дела ?':
            bot.send_message(message.chat.id, 'Отлично 😉, а у тебя?')
        elif message.text == 'хорошо':
            bot.send_message(message.chat.id, 'очень за тебя рад 🙃')
        
        
        else: 
            bot.send_message(message.chat.id, 'не знаю что и сказать тебе 🙄')

bot.polling(non_stop=True)


# @bot.message_handler(commands=['play'])
# def play_message(message):
# 	map_cell = get_map_cell(cols, rows)

# 	user_data = {
# 		'map': map_cell,
# 		'x': 0,
# 		'y': 0
# 	}

# 	maps[message.chat.id] = user_data

# 	bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_func(query):
# 	user_data = maps[query.message.chat.id]
# 	new_x, new_y = user_data['x'], user_data['y']

# 	if query.data == 'left':
# 		new_x -= 1
# 	if query.data == 'right':
# 		new_x += 1
# 	if query.data == 'up':
# 		new_y -= 1
# 	if query.data == 'down':
# 		new_y += 1

# 	if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
# 		return None
# 	if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
# 		return None

# 	user_data['x'], user_data['y'] = new_x, new_y

# 	if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
# 		bot.edit_message_text( chat_id=query.message.chat.id,
# 							   message_id=query.message.id,
# 							   text="Вы выиграли,Ура!!!" )
# 		return None

# 	bot.edit_message_text( chat_id=query.message.chat.id,
# 						   message_id=query.message.id,
# 						   text=get_map_str(user_data['map'], (new_x, new_y)),
# 						   reply_markup=keyboard )

# bot.polling(none_stop=False, interval=0)

