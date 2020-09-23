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
        for _ in range((weights[x])):
            l.append(x)
    if len(l) == 0:
        l = list(weights.keys())
    return l[rd.randint(0,len(l))]

async def random_sprite(rom_path,hash,heart_speed,heart_color,sprite,background_music,quickswap,menu_speed,msu_choice, auto_start):
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

    if msu_choice:
        if msu_choice < 0:
            msu_choice = rd.randint(1,len(msupacks)+1)

        outpath = settings['msupath'] + '/' + msupacks[msu_choice-1]
        for f in os.listdir(outpath)[::-1]:
            if f[-4:] == '.msu':
                fname = (f[-5::-1])[::-1]
                break
        await pyz3r.rom.write(patched_rom, outpath + '/' + fname + '.sfc')
        print('File written to ' + outpath + '/' + fname + '.sfc')
        # i, j = 0, 0
        # while j < len(outpath):
        #     while j < len(outpath) and outpath[j] != '/':
        #         j += 1
        #     print('cd ' + '\"' + outpath[i:j] + '\"', os.getcwd())
        #     os.system('cd ' + '\"' + outpath[i:j] + '\"')
        #     i = j+1
        #     j += 1
        if auto_start:
            os.chdir(outpath)
            os.system(fname + '.sfc')

    else:
        await pyz3r.rom.write(patched_rom, 'seed.sfc')
        if os.name == 'nt':
            print('File written to ' + os.getcwd() + '\\seed.sfc')
        else:
            print('File written to ' + os.getcwd() + '/seed.sfc')

        if auto_start:
            os.system('seed.sfc')

if __name__ == '__main__':

    # Settings (loaded from config.yaml)

    settings = load(open('config.yaml'), Loader=Loader)
    settings['heart_speed']['off'] = settings['heart_speed'].pop(False)

    if os.name == 'nt':
        rom_path = os.getcwd() + '\\' + settings['rompath']
        msu_path = os.getcwd() + '\\' + settings['msupath']
    else:
        rom_path = os.getcwd() + '/' + settings['rompath']
        msu_path = os.getcwd() + '/' + settings['msupath']

    auto_start = int(settings['auto_start'])

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

    msu_choice = 0
    if settings['msupath']:
        print('Available MSU Packs :')
        print('-1 : Random')
        print('0 : Default')
        msupacks = os.listdir(msu_path)
        for i in range(len(msupacks)):
            print(str(i+1) + ' : ' + msupacks[i])
        msu_choice = int(input('Please choose a MSU Pack : '))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(random_sprite(rom_path,hash,heart_speed,heart_color,sprite,background_music,quickswap,menu_speed,msu_choice,auto_start))

