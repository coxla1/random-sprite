import numpy.random as rd

import os
import pyz3r
import asyncio

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def choose_setting(weights):
    l = []
    for x in weights:
        for _ in range(weights[x]):
            l.append(x)
    if len(l) == 0:
        l = list(weights.keys())
    return l[rd.randint(0,len(l))]

# Settings (loaded from config.yaml)

settings = load(open('config.yaml'), Loader=Loader)
settings['heart_speed']['off'] = settings['heart_speed'].pop(False)

if os.name == 'nt':
    rom_path = os.getcwd() + '\\' + settings['rompath']
else:
    rom_path = os.getcwd() + '/' + settings['rompath']

heart_speed = choose_setting(settings['heart_speed'])
menu_speed = choose_setting(settings['menu_speed'])
sprite = choose_setting(settings['sprite'])
heart_color = choose_setting(settings['heart_color'])
background_music = choose_setting(settings['background_music'])
quickswap = choose_setting(settings['quickswap'])

hash = input('Please paste seed URL or hash here : ')
if '/' in hash:
    tmp = hash[::-1]
    hash = tmp[:tmp.find('/')][::-1]

async def random_sprite():
    base_rom = await pyz3r.rom.read(rom_path)
    seed = await pyz3r.alttpr(hash_id=hash)

    patched_rom = await seed.create_patched_game(
        base_rom,
        heartspeed=heart_speed,
        heartcolor=heart_color,
        spritename=sprite,
        music=background_music,
        quickswap=quickswap,
        menu_speed=menu_speed
    )
    
    if not os.path.isdir('output'):
        os.mkdir('output')
    
    await pyz3r.rom.write(patched_rom, 'output/' + hash + '.sfc')

    if os.name == 'nt':
        print('File written to ' + os.getcwd() + '\\output\\' + hash + '.sfc')
    else:
        print('File written to ' + os.getcwd() + '/output/' + hash + '.sfc')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(random_sprite())
