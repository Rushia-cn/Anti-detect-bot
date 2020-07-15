import uuid
import os
import re

from PIL import Image, ImageDraw, ImageFont
from telebot import TeleBot
from telebot.types import Message

color = re.compile("#[0-9a-fA-F]{6}")

bot = TeleBot(os.environ['TOKEN'])

if not os.path.exists("storage"):
    os.mkdir("storage")


def anti(text='default',
         bg_color=(244, 193, 134),
         fnt_color=(0, 0, 0),
         margin=(20, 10),
         show_image=False
         ):
    font_size = 80
    fnt = ImageFont.truetype('Roboto-Regular.ttf', font_size)
    fnt_size = fnt.getsize(text)
    new_img = Image.new('RGB', (fnt_size[0] + margin[0] * 2, fnt_size[1] + margin[1] * 2 + fnt_size[1] // 3), bg_color)
    text = str(text)
    draw: ImageDraw = ImageDraw.Draw(new_img)

    draw.text((margin[0], margin[1]), text, font=fnt, fill=fnt_color)

    if show_image:
        new_img.show()

    file_name = f"{text}_{str(uuid.uuid4())}.jpg"
    file_path = f"storage/{file_name}.jpg"
    new_img.save(file_path)
    return file_name, file_path


@bot.message_handler(commands=["anti"])
def generate(msg: Message):
    txt = msg.text.replace("/anti", "").strip()
    if not txt:
        bot.reply_to(msg, "usage: /anti text")
        return
    if matched := color.search(txt):
        rgb = matched[0]
        name, path = anti(txt.replace(rgb, "").strip(), bg_color=rgb)
    else:
        name, path = anti(txt)
    with open(path, "rb") as f:
        bot.send_photo(msg.chat.id, f)


if '__main__' == __name__:
    """
    anti('Suisei anti detected', margin=(20, 10), show_image=True)"""
    bot.polling()