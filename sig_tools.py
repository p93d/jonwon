import requests
from xml.etree import ElementTree
from PIL import Image, ImageFont, ImageDraw




def get_char_info(ids):

    wprofs = [
        'sword',
        'club',
        'axe',
        'dagger',
        'staff',
        'longsword',
        'warhammer',
        'battleaxe',
        'spear',
        'polearm'
    ]


    cprofs = [
        'ice',
        'fire',
        'lightning',
        'wind',
        'earth',
        'wild',
        'heal',
        'focused'
    ]


    sprofs = [
        'fishing',
        'cooking',
        'glyphing',
        'transmuting',
        'suffusencing'
    ]

    chars = [
        'Fighter',
        'Barbarian',
        'Rogue',
        'Magician',
        'Guardian',
        'Samurai',
        'Paladin',
        'Monk',
        'Ninja',
        'Warlock',
        'Headhunter',
        'Alchemist'
    ]



    r = requests.get(f"https://ladderslasher.d2jsp.org/xmlChar.php?i={ids[0]}")

    tree = ElementTree.fromstring(r.content)


    char_info = {}

    for e in tree:


        if e.tag == 'wprof':

            prof_splits = e.text.split(';')
            
            for prof in prof_splits:

                x = prof.split(',')

                current_level = int(x[1])

                next_level_progress = round( int(x[2]) / (current_level + 1) / 10, 2)

                char_info[wprofs[int(x[0])]] = f"{current_level} ({next_level_progress}%)"


        elif e.tag == 'cprof':

            try:
                prof_splits = e.text.split(';')
            except:
                prof_splits = []
            
            for prof in prof_splits:

                x = prof.split(',')

                current_level = int(x[1])

                next_level_progress = '{:.2f}'.format(round(round( int(x[2]) / (current_level + 1) / 10, 2), 2)) 

                char_info[cprofs[int(x[0])]] = f"{current_level} ({next_level_progress}%)"


        elif e.tag == 'sprof':

            try:
                prof_splits = e.text.split(';')
            except:
                prof_splits = []
            
            for prof in prof_splits:

                x = prof.split(',')

                current_level = int(x[1])

                next_level_progress = round( int(x[2]) / (current_level + 1) / 10, 2)

                char_info[sprofs[int(x[0])]] = f"{current_level} ({next_level_progress}%)"


        elif e.tag == 'classid':

            if int(e.text) == -1:

                char_info['class'] = '<None>'

            else:

                char_info['class'] = chars[int(e.text)]

           

        else:
            char_info[e.tag] = e.text



    # get guild points
    r = requests.get(f"https://ladderslasher.d2jsp.org/xmlGuild.php?i={ids[2]}")

    tree = ElementTree.fromstring(r.content)

    for e in tree:

        if e.attrib['id'] == ids[1]:

            char_info['guild_points'] = e.attrib['gps']
            char_info['guild'] = ids[3]
            break

    else:
        char_info['guild_points'] = 0
        char_info['guild'] = ''
        

    if char_info['class'] == "Alchemist":

        if int(char_info['mqattempts']) == 0:

            char_info['class'] = "<None>"

    
    return char_info



    
    
    
def jonwon(ids):

    profs = get_char_info(ids)

    char_class = profs['class']

    try:
        img = Image.open(f'static/images/{char_class.lower()}.jpeg')
    except:
        img = Image.open('static/images/rogue.jpeg')

    
    draw = ImageDraw.Draw(img)

    font_one = ImageFont.truetype('static/fonts/Teko-Light.ttf', 32)
    font_two = ImageFont.truetype('static/fonts/pixelmix.ttf', 10)

    black = (35,35,35)

    line_1 = f"CLASS: {char_class.upper()}"
    line_2 = f"LEVEL: {profs['level']}"
    line_3 = f"KILLS: {int(profs['kills']):,}"
    line_4 = f"MQS: {profs['mqpasses']}/{profs['mqattempts']}"
    line_5 = f"GPS: {profs['guild_points']}"


    w, h = draw.textsize(profs['name'].upper(), font=font_one)
    draw.text((87 - w/2, 15), profs['name'].upper(), black, font=font_one)


    w, h = draw.textsize(line_1, font=font_two)
    draw.text((87 - w/2, 60), f"CLASS: {char_class.upper()}", black, font=font_two)

    w, h = draw.textsize(line_2, font=font_two)
    draw.text((87 - w/2, 72), f"LEVEL: {profs['level']}", black, font=font_two)

    w, h = draw.textsize(line_3, font=font_two)
    draw.text((87 - w/2, 84), f"KILLS: {int(profs['kills'])}", black, font=font_two)

    w, h = draw.textsize(line_4, font=font_two)
    draw.text((87 - w/2, 96), f"MQS: {profs['mqpasses']}/{profs['mqattempts']}", black, font=font_two)

    w, h = draw.textsize(line_5, font=font_two)
    draw.text((87 - w/2, 108), f"GPS: {profs['guild_points']}", black, font=font_two)
    


    img.save('static/images/jonwon.jpeg')
    
    