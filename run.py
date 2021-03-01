import os
import random
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter
import csv


def recommend_font_size(text):
    size = 90*MULTIPLIER
    l = len(text)

    resize_heuristic = 0.9
    resize_actual = 0.985
    while l > 1:
        l = l * resize_heuristic
        size = size * resize_actual

    return int(size)


def select_background_image():
    prefix = "input/people/"
    options = os.listdir(prefix)
    return prefix + random.choice(options)


# def select_icon():
#     prefix = "icons/"
#     options = os.listdir(prefix)
#     return prefix + random.choice(options)


def select_font():
    prefix = "fonts/"
    options = os.listdir(prefix)
    return prefix + random.choice(options)


def wrap_text(text, w=30):
    new_text = ""
    new_sentence = ""
    for word in text.split(" "):
        delim = " " if new_sentence != "" else ""
        new_sentence = new_sentence + delim + word
        if len(new_sentence) > w:
            new_text += "\n" + new_sentence
            new_sentence = ""
    new_text += "\n" + new_sentence
    return new_text


def write_image(text, output_filename, background_img):
    # setup
    text = wrap_text(text)
    img = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

    # background
    back = Image.open(background_img, 'r')

    back = back.filter(ImageFilter.SMOOTH_MORE)

    applier = ImageEnhance.Color(back)
    back = applier.enhance(0.20)

    img_w, img_h = back.size
    bg_w, bg_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    img.paste(back, offset)

    # paste icon

    # im = Image.open(ICON)

    # (width, height) = (im.width // 8, im.height // 8)
    # im_resized = im.resize((width, height))
    # img.paste(im_resized, (50, 50))

    # paste logo

    logo = Image.open("pclogo.png")
    (width, height) = (logo.width // 4*MULTIPLIER, logo.height // 4*MULTIPLIER)
    logo_resized = logo.resize((width, height))
    img.paste(logo_resized, (IMAGE_WIDTH-width-60, IMAGE_HEIGHT-height-60))

    # text
    font = ImageFont.truetype(FONT, FONT_SIZE)
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    x = img_w / 2
    y = img_h / 2
    textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)
    text_w, text_h = textsize
    x -= text_w / 2
    y -= text_h / 2
    draw.multiline_text(align="center", xy=(x, y), text=text,
                        fill=COLOR, font=font, spacing=SPACING)

    # rectangle
    draw.rectangle((30, IMAGE_HEIGHT-30, IMAGE_WIDTH-30, 30),
                   fill=None, outline="#CE1126", width=6*MULTIPLIER)

    # output
    img.save(output_filename)
    return output_filename


# text
text = ' “Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to lose. You are already naked. There is no reason not to follow your heart.” – Steve Jobs '
output_filename = "output/{}.png".format(int(time.time()))

# config
MULTIPLIER = 2
FONT = select_font()
# ICON = select_icon()
FONT_SIZE = recommend_font_size(text)
print(FONT_SIZE)
IF = ImageFont.truetype(FONT, FONT_SIZE)
IMAGE_WIDTH = 940*MULTIPLIER
IMAGE_HEIGHT = 788*MULTIPLIER
COLOR = (255, 255, 255)
SPACING = 6*MULTIPLIER


# print(write_image(text, output_filename, background_img=select_background_image()))


path = "quotes.csv"
file = open(path, newline="")
reader = csv.reader(file)

data = [row for row in reader]

counter = 0
for n in data:
    text = '"' + data[counter][0] + '"' + " - " + data[counter][1]
    counter = counter + 1
    output_filename = "output/{}-{}.png".format(counter, int(time.time()))
    FONT = select_font()
    ONT_SIZE = recommend_font_size(text)
    print(FONT_SIZE)
    IF = ImageFont.truetype(FONT, FONT_SIZE)
    print(write_image(text, output_filename,
                      background_img=select_background_image()))
