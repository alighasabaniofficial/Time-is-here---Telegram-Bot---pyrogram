from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import jdatetime
from __api_key__ import api_id, api_hash, bot_token
from datetime import datetime
import pytz
from collections import defaultdict
from hijri_converter import Hijri, Gregorian


# Time Is Here Telegram Bot - V1.0.0 - by t.me/alipython1


app = Client(
    'TimeBot',
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)


def Tree():
    return defaultdict(Tree)


user_pocket = Tree()

start_text = '''
به ربات زمان خوش آمدید. 🌱
از منو گزینه مورد نظر رو انتخاب کن.
'''
current_time_in_iran_hour = 0
current_time_in_iran = 0


# when user starts bot, bot says this.
def start_time_update():
    global start_text
    global current_time_in_iran
    global current_time_in_iran_hour

    timezone = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(timezone)
    current_time_in_iran = current_time.strftime("%H:%M:%S")

    current_time_in_iran_hour = current_time.strftime("%H")
    current_time_in_iran_hour = int(current_time_in_iran_hour)

    start_text_morning = '''
صبح بخیر ☀️
به ربات زمان خوش آمدید. 🌱
از منو گزینه مورد نظر رو انتخاب کن.
'''
    start_text_noon = '''
ظهر بخیر ☀️
به ربات زمان خوش آمدید. 🌱
از منو گزینه مورد نظر رو انتخاب کن.
'''
    start_text_afternoon = '''
عصر بخیر
به ربات زمان خوش آمدید. 🌱
از منو گزینه مورد نظر رو انتخاب کن.
'''
    start_text_night = '''
شب بخیر 🌙
به ربات زمان خوش آمدید. 🌱
از منو گزینه مورد نظر رو انتخاب کن.
'''

    if 3 <= current_time_in_iran_hour < 12:
        start_text = start_text_morning
        return start_text
    elif 12 <= current_time_in_iran_hour < 16:
        start_text = start_text_noon
        return start_text
    elif 16 <= current_time_in_iran_hour < 19:
        start_text = start_text_afternoon
        return start_text
    else:
        start_text = start_text_night
        return start_text


def days_of_week_jalali_fa():
    jalali_days_week = JalaliDate.today().strftime('%a')
    if jalali_days_week == 'Sha':
        return 'شنبه'
    elif jalali_days_week == 'Yek':
        return 'یکشنبه'
    elif jalali_days_week == 'Dos':
        return 'دوشنبه'
    elif jalali_days_week == 'Ses':
        return 'سه شنبه'
    elif jalali_days_week == 'Cha':
        return 'چهارشنبه'
    elif jalali_days_week == 'Pan':
        return 'پنجشنبه'
    elif jalali_days_week == 'Jom':
        return 'جمعه'


def main_menu(message: Message):
    text = 'Menu 👇'
    return message.reply_text(text=text, reply_markup=ReplyKeyboardMarkup(
        [
            ['زمان الان (به وقت ایران) ⏱'],
            ['تبدیل تاریخ میلادی به شمسی 🗓', 'تبدیل تاریخ شمسی به میلادی 🗓'],
            ['تبدیل تاریخ قمری به شمسی 🗓', 'تبدیل تاریخ شمسی به قمری 🗓'],
            ['✨ ارتباط با سازندۀ ربات ✨'],
        ],
        resize_keyboard=True
    ))


print('Bot is Starting.')

step = {}


@app.on_message(filters.command('start'))
def start_m(client: Client, message: Message):
    user_pocket[message.from_user.id]['step'] = 'start_level'
    print(
        f'[User_ID: {message.from_user.id}, Name: {message.from_user.first_name}, User_Name: {message.from_user.username}] starts bot.'
    )
    start_time_update()
    inline_button1 = 'سازندۀ ربات: alipython1@'
    message.reply_text(start_text, reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Opens my telegram account
                    text=inline_button1,
                    url='t.me/alipython1'
                )
            ]
        ]
    )
                       )
    main_menu(message)
    user_pocket[message.from_user.id]['step'] = 'Home_Menu'


@app.on_message(filters.text)
def message(client: Client, message: Message):
    if user_pocket[message.from_user.id]['step'] == 'Home_Menu':
        shamsi_date = JalaliDate.today().strftime('%Y/%m/%d')
        iran_time_text = 'ساعت به وقت ایران 👇'

        if message.text == 'زمان الان (به وقت ایران) ⏱':
            start_time_update()
            shamsi_days_week = days_of_week_jalali_fa()
            message.reply_text(f'{iran_time_text}\n\n⏱ {current_time_in_iran} ⏱\n{shamsi_days_week} | {shamsi_date}')

        elif message.text == 'تبدیل تاریخ شمسی به میلادی 🗓':
            message.reply_text('لطفا تاریخ شمسی خود را وارد کنید:\n\nمثال:\n1402/1/15', reply_markup=ReplyKeyboardMarkup(
                [
                    ['🔹 برگشت به منوی اصلی 🔹']
                ], resize_keyboard=True
            )
            )
            user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_miladi_level'

        elif message.text == 'تبدیل تاریخ میلادی به شمسی 🗓':
            message.reply_text('لطفا تاریخ میلادی خود را وارد کنید:\n\nمثال:\n2023-1-15',
                               reply_markup=ReplyKeyboardMarkup(
                                   [
                                       ['🔹 برگشت به منوی اصلی 🔹']
                                   ], resize_keyboard=True
                               )
                               )
            user_pocket[message.from_user.id]['step'] = 'enter_miladi_to_shamsi_level'

        elif message.text == 'تبدیل تاریخ شمسی به قمری 🗓':
            message.reply_text('لطفا تاریخ شمسی خود را وارد کنید:\n\nمثال:\n1402/1/15',
                               reply_markup=ReplyKeyboardMarkup(
                                   [
                                       ['🔹 برگشت به منوی اصلی 🔹']
                                   ], resize_keyboard=True
                               )
                               )
            user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_ghamari_level'

        elif message.text == 'تبدیل تاریخ قمری به شمسی 🗓':
            message.reply_text('لطفا تاریخ قمری خود را وارد کنید:\n\nمثال:\n1445/1/15',
                               reply_markup=ReplyKeyboardMarkup(
                                   [
                                       ['🔹 برگشت به منوی اصلی 🔹']
                                   ], resize_keyboard=True
                               )
                               )
            user_pocket[message.from_user.id]['step'] = 'enter_ghamari_to_shamsi_level'

        elif message.text == '✨ ارتباط با سازندۀ ربات ✨':
            inline_button1 = 'سازندۀ ربات: alipython1@'
            message.reply_text('علی هستم برنامه نویس ربات.\n\n🕊📩 برای سفارش ربات پیام بدید.🕊📩', reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Opens my telegram account
                            text=inline_button1,
                            url='t.me/alipython1'
                        )
                    ]
                ]
            )
                               )

        else:
            message.reply_text('⚠️ لطفا یک گزینه صحیح از داخل منو انتخاب کنید! ⚠️')

    elif user_pocket[message.from_user.id]['step'] == 'enter_shamsi_to_miladi_level':
        if message.text == '🔹 برگشت به منوی اصلی 🔹':
            inline_button1 = 'سازندۀ ربات: alipython1@'
            message.reply_text('⚡️ منوی اصلی ⚡️\n\nاز منو گزینه مورد نظر رو انتخاب کن.', reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(  # Opens my telegram account
                            text=inline_button1,
                            url='t.me/alipython1'
                        )
                    ]
                ]
            )
                               )
            main_menu(message)
            user_pocket[message.from_user.id]['step'] = 'Home_Menu'
        else:
            try:
                user_time_shamsi = message.text

                user_time_shamsi_split = user_time_shamsi.split('/')
                user_year_shamsi = user_time_shamsi_split[0]
                user_month_shamsi = user_time_shamsi_split[1]
                user_day_shamsi = user_time_shamsi_split[2]

                user_year_shamsi = int(user_year_shamsi)
                user_month_shamsi = int(user_month_shamsi)
                user_day_shamsi = int(user_day_shamsi)

                changed_shamsi_to_miladi = JalaliDate(user_year_shamsi, user_month_shamsi,
                                                      user_day_shamsi).to_gregorian().strftime('%Y/%m/%d')
                message.reply_text(f'⚡️ به تاریخ شمسی تبدیل شد. ⚡️\n\n{changed_shamsi_to_miladi}')
                main_menu(message)
                user_pocket[message.from_user.id]['step'] = 'Home_Menu'
            except:
                message.reply_text("⚠️ فرمت اشتباه وارد کردی! ⚠️\n\nفرمت درست:\n1402/1/15")
                user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_miladi_level'

    elif user_pocket[message.from_user.id]['step'] == 'enter_miladi_to_shamsi_level':
        if message.text == '🔹 برگشت به منوی اصلی 🔹':
            inline_button1 = 'سازندۀ ربات: alipython1@'
            message.reply_text('⚡️ منوی اصلی ⚡️\n\nاز منو گزینه مورد نظر رو انتخاب کن.',
                               reply_markup=InlineKeyboardMarkup(
                                   [
                                       [  # First row
                                           InlineKeyboardButton(  # Opens my telegram account
                                               text=inline_button1,
                                               url='t.me/alipython1'
                                           )
                                       ]
                                   ]
                               )
                               )
            main_menu(message)
            user_pocket[message.from_user.id]['step'] = 'Home_Menu'

        else:
            try:
                user_time_miladi = message.text

                user_time_miladi_split = user_time_miladi.split('-')
                user_year_miladi = user_time_miladi_split[0]
                user_month_miladi = user_time_miladi_split[1]
                user_day_miladi = user_time_miladi_split[2]

                user_year_miladi = int(user_year_miladi)
                user_month_miladi = int(user_month_miladi)
                user_day_miladi = int(user_day_miladi)

                changed_miladi_to_shamsi = JalaliDate.to_jalali(
                    user_year_miladi, user_month_miladi, user_day_miladi).strftime('%Y-%m-%d')
                message.reply_text(f'⚡️ به تاریخ میلادی تبدیل شد. ⚡️\n\n{changed_miladi_to_shamsi}')
                main_menu(message)
                user_pocket[message.from_user.id]['step'] = 'Home_Menu'
            except:
                message.reply_text("⚠️ فرمت اشتباه وارد کردی! ⚠️\n\nفرمت درست:\n2023-1-15")
                user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_miladi_level'

    elif user_pocket[message.from_user.id]['step'] == 'enter_shamsi_to_ghamari_level':
        if message.text == '🔹 برگشت به منوی اصلی 🔹':
            inline_button1 = 'سازندۀ ربات: alipython1@'
            message.reply_text('⚡️ منوی اصلی ⚡️\n\nاز منو گزینه مورد نظر رو انتخاب کن.',
                               reply_markup=InlineKeyboardMarkup(
                                   [
                                       [  # First row
                                           InlineKeyboardButton(  # Opens my telegram account
                                               text=inline_button1,
                                               url='t.me/alipython1'
                                           )
                                       ]
                                   ]
                               )
                               )
            main_menu(message)
            user_pocket[message.from_user.id]['step'] = 'Home_Menu'
        else:
            try:
                # Convert a Hijri date to Gregorian
                g = Hijri(1403, 2, 17).to_gregorian()

                user_time_shamsi = message.text

                user_time_shamsi_split = user_time_shamsi.split('/')
                user_year_shamsi = user_time_shamsi_split[0]
                user_month_shamsi = user_time_shamsi_split[1]
                user_day_shamsi = user_time_shamsi_split[2]

                user_year_shamsi = int(user_year_shamsi)
                user_month_shamsi = int(user_month_shamsi)
                user_day_shamsi = int(user_day_shamsi)

                changed_shamsi_to_miladi = JalaliDate(user_year_shamsi, user_month_shamsi,
                                                      user_day_shamsi).to_gregorian().strftime('%Y/%m/%d')

                changed_shamsi_to_miladi = changed_shamsi_to_miladi.split('/')
                user_year_shamsi_to_miladi = changed_shamsi_to_miladi[0]
                user_month_shamsi_to_miladi = changed_shamsi_to_miladi[1]
                user_day_shamsi_to_miladi = changed_shamsi_to_miladi[2]

                user_year_shamsi_to_miladi  = int(user_year_shamsi_to_miladi)
                user_month_shamsi_to_miladi  = int(user_month_shamsi_to_miladi)
                user_day_shamsi_to_miladi = int(user_day_shamsi_to_miladi)

                # Convert a Gregorian date to Hijri
                hijri_changed = Gregorian(
                    user_year_shamsi_to_miladi, user_month_shamsi_to_miladi, user_day_shamsi_to_miladi).to_hijri().dmyformat('/')
                hijri_changed = hijri_changed.split('/')
                hijri_changed = f'{hijri_changed[2]}/{hijri_changed[1]}/{hijri_changed[0]}'

                message.reply_text(f'⚡️ به تاریخ قمری تبدیل شد. ⚡️\n\n{hijri_changed}')
                main_menu(message)
                user_pocket[message.from_user.id]['step'] = 'Home_Menu'
            except:
                message.reply_text("⚠️ فرمت اشتباه وارد کردی! ⚠️\n\nفرمت درست:\n1402/1/15")
                user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_ghamari_level'

    elif user_pocket[message.from_user.id]['step'] == 'enter_ghamari_to_shamsi_level':
        if message.text == '🔹 برگشت به منوی اصلی 🔹':
            inline_button1 = 'سازندۀ ربات: alipython1@'
            message.reply_text('⚡️ منوی اصلی ⚡️\n\nاز منو گزینه مورد نظر رو انتخاب کن.',
                               reply_markup=InlineKeyboardMarkup(
                                   [
                                       [  # First row
                                           InlineKeyboardButton(  # Opens my telegram account
                                               text=inline_button1,
                                               url='t.me/alipython1'
                                           )
                                       ]
                                   ]
                               )
                               )
            main_menu(message)
            user_pocket[message.from_user.id]['step'] = 'Home_Menu'
        else:
            try:
                # Convert a Hijri date to Gregorian
                g = Hijri(1403, 2, 17).to_gregorian()

                user_time_ghamari = message.text

                user_time_ghamari_split = user_time_ghamari.split('/')
                user_year_ghamari = user_time_ghamari_split[0]
                user_month_ghamari = user_time_ghamari_split[1]
                user_day_ghamari = user_time_ghamari_split[2]

                user_year_ghamari = int(user_year_ghamari)
                user_month_ghamari = int(user_month_ghamari)
                user_day_ghamari = int(user_day_ghamari)

                # Convert a Hijri date to Gregorian
                g = Hijri(1403, 2, 17).to_gregorian()

                changed_ghamari_to_miladi = Hijri(
                    user_year_ghamari, user_month_ghamari, user_day_ghamari).to_gregorian().dmyformat('/')
                changed_ghamari_to_miladi = changed_ghamari_to_miladi.split('/')

                changed_miladi_to_shamsi = JalaliDate.to_jalali(
                    int(changed_ghamari_to_miladi[2]),
                    int(changed_ghamari_to_miladi[1]), int(changed_ghamari_to_miladi[0])).strftime('%Y/%m/%d')

                message.reply_text(f'⚡️ به تاریخ شمسی تبدیل شد. ⚡️\n\n{changed_miladi_to_shamsi}')
                main_menu(message)
                user_pocket[message.from_user.id]['step'] = 'Home_Menu'

            except:
                message.reply_text("⚠️ فرمت اشتباه وارد کردی! ⚠️\n\nفرمت درست:\n1445/1/15")
                user_pocket[message.from_user.id]['step'] = 'enter_shamsi_to_ghamari_level'


app.run()
