import transfer

import os
import subprocess
import shutil
import threading

import json
import asyncio
import pyz3r
import random as rd
import psutil
import urllib.request
import requests

from tkinter import filedialog as fd
from tkinter import messagebox

msupacks = []

class thread(threading.Thread):
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.daemon = True

    def run(self):
        subprocess.call(self.cmd)

def load_cfg(vars):
    try:
        with open('data/config.json', 'r') as cfgfile:
            cfg = json.load(cfgfile)
    except:
        cfg = {}
        for x in vars:
            if x != 'seed' and x != 'uri':
                if type(vars[x]) == type({}):
                    cfg[x] = {}
                    for y in vars[x]:
                        cfg[x][y] = vars[x][y].get()

                else:
                    cfg[x] = vars[x].get()

    for x in cfg:
        if type(cfg[x]) == type({}):
            for y in cfg[x]:
                vars[x][y].set(cfg[x][y])

        else:
            vars[x].set(cfg[x])

def save_cfg(vars):
    cfg = {}
    for x in vars:
        if x != 'seed' and x != 'uri':
            if type(vars[x]) == type({}):
                cfg[x] = {}
                for y in vars[x]:
                    cfg[x][y] = vars[x][y].get()

            else:
                cfg[x] = vars[x].get()


    with open('data/config.json', 'w') as cfgfile:
        json.dump(cfg, cfgfile, indent=4)

def set_path(var, entry, type):
    entry.focus()
    if type == 'file':
        path = fd.askopenfilename()
    else:
        path = fd.askdirectory()
    var.set(path)

def refresh_msu(var_msupath, input_msu, var_msu, mode, var_uri, input_fxpakfolders):
    global msupacks
    msupacks = []

    if mode.get() == 0: # Transfer
        msupath = input_fxpakfolders.get(input_fxpakfolders.curselection())
        msupacks = transfer.list_msupacks(var_uri.get(), msupath)

    else: # Copy
        if var_msupath.get():
            try:
                msupacks.extend(os.listdir(var_msupath.get()))
            except:
                msupacks.extend([])

    msupacks.sort()
    for x in msupacks:
        if '.sfc' in x:
            msupacks.pop(msupacks.index(x))

    input_msu.children['menu'].delete(0,'end')

    for x in ['Default', 'Random']:
        input_msu.children['menu'].add_command(label=x, command=lambda y=x: var_msu.set(y))

    for x in msupacks:
        input_msu.children['menu'].add_command(label=x, command=lambda y=x: var_msu.set(y))

    msupacks.append('Default')


# async def gen_seed(rom, hash, speed, color, sprite, bgm, quickswap):
#     base_rom = await pyz3r.rom.read(rom)
#     seed = await pyz3r.alttpr(hash_id=hash)
#     patched_rom = await seed.create_patched_game(base_rom, heartspeed=speed, heartcolor=color, spritename=sprite, music=bgm, quickswap=quickswap)
#
#     await pyz3r.rom.write(patched_rom, os.getcwd() + '/seed.sfc')
#     return seed.data['spoiler']

# Rewrite later
# def download(seed, rom, msu, emupath, timerpath, usbpath, trackpath, patch, emu, timer, usb, track, door, sphere, map, logic, speed, color, bgm, quickswap, glitches, msupack, sprites, output, info):
#     global msupacks
#
#     if patch.get():
#         # Patch the ROM
#         speed_val = {}
#         for x in speed:
#             speed_val[x] = speed[x].get()
#
#         color_val = {}
#         for x in color:
#             color_val[x] = color[x].get()
#
#         if glitches.get():
#             sprite = 'Link'
#         else:
#             sprites_val = {s: sprites[s]['var'].get() for s in sprites}
#             sprite = pick_setting(sprites_val, 'Link')
#
#         try:
#             settings = asyncio.run(gen_seed(rom.get(), hash(seed.get()), pick_setting(speed_val, 'normal'), pick_setting(color_val, 'red'), sprite, bgm.get(), quickswap.get()))
#         except:
#             info.config(text='An error occured while patching the ROM.')
#             return -1 ...

def run(vars, input_fxpakfolders, default, log):
    global msupacks

    log.config(text='')
    process = [x.name() for x in psutil.process_iter()]

    if vars['seed'].get():
        hash = seed_hash(vars['seed'])
        print(f'Seed hash: {hash}')
        settings = seed_settings(hash)
        # settings = asyncio.run(seed_settings(hash))
        if settings:
            print('Found settings:')
            for x in settings['meta']:
                print('\t{:}: {:}'.format(x, settings['meta'][x]))
        else:
            print('No settings found')
        # try:
        #     settings = asyncio.run(seed_settings(hash))
        # except: # This could be used with other ROMs, e.g. AP MW ones
        #     settings = []
        # print(f'Seed hash: {hash}')
        # print('Found settings:')
        # for x in settings:
        #     print(f'\t{x}')

        # MSU Pack
        try:
            msu = vars['msu'].get()
            if msu == 'Random':
                msu = msupacks[rd.randint(0, len(msupacks)-1)]
                vars['msu'].set(msu)

            if msu == 'Default':
                if vars['mode'].get() == 0: # Transfer
                    destination_folder = input_fxpakfolders.get(input_fxpakfolders.curselection())
                else: # Copy
                    destination_folder = vars['msupath'].get()

                filename = 'seed.sfc'

            else:
                if vars['mode'].get() == 0: # Transfer
                    destination_folder = '{:}/{:}'.format(input_fxpakfolders.get(input_fxpakfolders.curselection()), msu)
                    filename = transfer.find_msu_filename(vars['uri'].get(), destination_folder)
                else: # Copy
                    destination_folder = '{:}{:}{:}'.format(vars['msupath'].get(), os.sep, msu)
                    filename = ''
                    for f in os.listdir(destination_folder)[::-1]:
                        if f[-4:] == '.msu':
                            filename = f[:-4] + '.sfc'
                            break

                if filename == '':
                    log.config(text='Could not find .msu file in the pack directory')
                    return -1

            print(f'MSU: {msu}')

            print('Transfer type: {:}'.format('Copy' if vars['mode'].get() else 'USB'))
            print(f'Destination folder: {destination_folder}')
            print(f'Filename: {filename}')

            if vars['mode'].get() == 0: # Transfer
                transfer.send_rom(vars['seed'].get(), vars['uri'].get(), f'{destination_folder}/{filename}')
            else: # Copy
                shutil.copy(vars['seed'].get(), f'{destination_folder}{os.sep}{filename}')


        except:
            log.config(text='An error occured while writing to destination folder, if using USB transfer consider turning SNES OFF/ON')

        # Boot ROM
        if vars['autostart']['boot'].get() and vars['seed'].get():
            if vars['mode'].get() == 0: # Transfer
                transfer.boot_rom(vars['uri'].get(), f'{destination_folder}/{filename}')
            elif vars['emulator'].get() != default['emulator']: # Copy
                thread_emu = thread('"{:}" "{:}"'.format(vars['emulator'].get(), f'{destination_folder}{os.sep}{filename}'))
                thread_emu.start()

    # Timer
    if vars['autostart']['timer'].get() and vars['timer'].get() != default['timer'] and not process_is_running(vars['timer'].get(), process):
        thread_timer = thread(vars['timer'].get())
        thread_timer.start()

    # Tracker
    if vars['autostart']['tracker'].get():
        if vars['tracker'].get() != default['tracker']:
            if not process_is_running(vars['tracker'].get(), process):
                thread_tracker = thread(vars['tracker'].get())
                thread_tracker.start()

        else:
            if vars['seed'].get() and settings:
                url, width, height = dunka_url(vars, log, settings['meta'])
            else:
                url, width, height = dunka_url(vars, log)

            print(f'Dunka\'s URL: {url}')

            thread_tracker = thread(f'cmd /c start msedge --app="{url}" --user-data-dir="%tmp%\rdmsprite_dunkatracker" --window-position=10,10 --window-size={width},{height}')
            thread_tracker.start()

    # SNI/QUSB2SNES
    if vars['autostart']['usbinterface'].get() and vars['usbinterface'].get() != default['usbinterface'] and not process_is_running(vars['usbinterface'].get(), process):
        thread_usbinterface = thread(vars['usbinterface'].get())
        thread_usbinterface.start()

    if vars['dunkatracker']['door'].get() == 'Crossed/Keydrop':
        keycount = 'Dungeon: total keys/dropped keys\n'
        keycount += 'Hyrule Castle: 4(+1 BK)/3(+1 BK)\n'
        keycount += 'Eastern Palace: 2/2\n'
        keycount += 'Desert Palace: 4/3\n'
        keycount += 'Tower of Hera: 1/0\n'
        keycount += 'Castle Tower: 4/2\n'
        keycount += 'Palace of Darkness: 6/0\n'
        keycount += 'Swamp Palace: 6/5\n'
        keycount += 'Skull Woods: 5/2\n'
        keycount += 'Thieves\' Town: 3/2\n'
        keycount += 'Ice Palace: 5/3\n'
        keycount += 'Misery Mire: 6/3\n'
        keycount += 'Turtle Rock: 6/2\n'
        keycount += 'Ganon\'s Tower: 8/4\n'
        messagebox.showinfo('Keydrop keys count', keycount)


def seed_hash(input_seed):
    if '.sfc' in input_seed.get(): # File provided
        # print('ici')
        # hash = input_seed.get()[-14:-4]
        f = open(input_seed.get(), 'rb')
        f.read(32704)
        hash = bytearray.fromhex(f.read(13).hex()).decode()
        f.close()
        # print(hash)
        if hash[:2] == 'VT':
            hash = str(hash[3:])
        else:
            hash = None
        # print(hash)
    else: # URL or hash
        url = input_seed.get()
        if '/' in url:
            url = url[::-1]
            hash = url[:url.find('/')][::-1]
        else:
            hash = url
    return hash

# async def seed_settings(hash):
#     seed = await pyz3r.alttpr(hash_id=hash)
#     return seed.data['spoiler']

def seed_settings(hash):
    if hash:
        url = f'https://alttpr-patch-data.s3.us-east-2.amazonaws.com/{hash}.json'
        with requests.get(url) as r:
            settings = r.json()['spoiler']
    else:
        settings = []

    return settings


# ok but useless atm
def pick_setting(weights, default=''):
    l = []
    for x in weights:
        for _ in range((weights[x])):
            l.append(x)
    if len(l) == 0:
        return default
    return l[rd.randint(0, len(l)-1)]


def dunka_url(vars, log, settings={'spoilers': 'mystery'}):
    # Determine URL format
    with urllib.request.urlopen('https://raw.githubusercontent.com/bigdunka/alttptracker/master/js/index.js') as u:
        trackerjs = u.read().decode('utf-8')

    i = len('trackerWindow = window.open(')
    j = trackerjs.index('trackerWindow')
    k = trackerjs[j:].index('\n')
    urlformat = 'f' + trackerjs[j+i:j+k]

    # Define variables
    if settings['spoilers'] == 'mystery':
        tracker = 'tracker'
        type = 'O'
        entrance = 'N'
        boss = 'S'
        enemy = 'S'
        glitches = {'No Glitches': 'N', 'OWG': 'O', 'MG/No Logic': 'M'}[vars['dunkatracker']['maplogic'].get()]
        item = 'A'
        goal = 'G'
        tower = 'R'
        towercrystals = '7'
        ganon = 'R'
        ganoncrystals = '7'
        swords = 'R'
        map = {'None': 'N', 'Normal': 'M', 'Compact': 'C'}[vars['dunkatracker']['mapdisplay'].get()]
        spoiler = 'N'
        sphere = {0: 'N', 1: 'Y'}[vars['dunkatracker']['sphere'].get()]
        mystery = 'S'
        door = {'None': 'N', 'Basic': 'B', 'Crossed/Keydrop': 'C'}[vars['dunkatracker']['door'].get()]
        shuffledmaps = '1'
        shuffledcompasses = '1'
        shuffledsmallkeys = '1'
        shuffledbigkeys = '1'
        ambrosia = 'N'
        overworld = {'None': 'N', 'Mixed/Crossed/Misc': 'O', 'Parallel': 'P', 'Full': 'F'}[vars['dunkatracker']['overworld'].get()]
        autotracking = {0: 'N', 1: 'Y'}[vars['dunkatracker']['autotracker'].get()]
        trackingport = '8080'
        sprite = 'Link'
        compact = '&map=C' if map == 'C' else ''
        startingboots = 'N'
        startingflute = 'N'
        startinghookshot = 'N'
        startingicerod = 'N'

    else:
        tracker = 'entrancetracker' if 'shuffle' in settings else 'tracker'
        type = {'open': 'O', 'standard': 'S', 'inverted': 'I', 'retro': 'R'}[settings['mode']]
        entrance = 'S' if 'shuffle' in settings else 'N'
        boss = 'N' if settings['enemizer.boss_shuffle'] == 'none' else 'S'
        enemy = 'N' if settings['enemizer.enemy_shuffle'] == 'none' else 'S'
        glitches = {'No Glitches': 'N', 'OWG': 'O', 'MG/No Logic': 'M'}[vars['dunkatracker']['maplogic'].get()]
        item = 'A'
        goal = {'ganon': 'G', 'fast_ganon': 'F', 'pedestal': 'P', 'dungeons': 'A', 'triforce-hunt': 'O'}[settings['goal']]
        tower = 'R' if settings['entry_crystals_tower'] == 'random' else 'C'
        towercrystals = '7' if settings['entry_crystals_tower'] == 'random' else settings['entry_crystals_tower']
        ganon = 'R' if settings['entry_crystals_ganon'] == 'random' else 'C'
        ganoncrystals = '7' if settings['entry_crystals_tower'] == 'random' else settings['entry_crystals_ganon']
        swords = {'randomized': 'R', 'assured': 'A', 'vanilla': 'V', 'swordless': 'S'}[settings['weapons']]
        map = {'None': 'N', 'Normal': 'M', 'Compact': 'C'}[vars['dunkatracker']['mapdisplay'].get()]
        spoiler = 'N'
        sphere = {0: 'N', 1: 'Y'}[vars['dunkatracker']['sphere'].get()]
        mystery = 'S'
        door = {'None': 'N', 'Basic': 'B', 'Crossed/Keydrop': 'C'}[vars['dunkatracker']['door'].get()]

        shuffledmaps, shuffledcompasses, shuffledsmallkeys, shuffledbigkeys = {'standard': ('0', '0', '0', '0'), 'mc': ('1', '1', '0', '0'), 'mcs': ('1', '1', '1', '0'), 'full': ('1', '1', '1', '1')}[settings['dungeon_items']]

        if 'name' in settings:
            if 'Potpourri' in settings['name']:
                shuffledmaps, shuffledcompasses, shuffledsmallkeys, shuffledbigkeys = '0', '0', '1', '1'
            log.config(text='You may have to adjust settings using the flag icon in the top-left corner')

        if settings['logic'] == 'NoLogic':
            shuffledmaps, shuffledcompasses, shuffledsmallkeys, shuffledbigkeys = '1', '1', '1', '1'

        ambrosia = 'N'
        overworld = {'None': 'N', 'Mixed/Crossed/Misc': 'O', 'Parallel': 'P', 'Full': 'F'}[vars['dunkatracker']['overworld'].get()]
        autotracking = {0: 'N', 1: 'Y'}[vars['dunkatracker']['autotracker'].get()]
        trackingport = '8080'
        sprite = 'Link'
        compact = '&map=C' if map == 'C' else ''
        startingboots = 'N'
        startingflute = 'N'
        startinghookshot = 'N'
        startingicerod = 'N'

    # This should work if Dunka adds a new variable
    flag = True
    newvar = []
    while flag:
        try:
            url = 'https://alttptracker.dunka.net/{:}'.format(eval(urlformat))
            flag = False
        except NameError as e:
            i = e[6:].index('\'')
            newvar.append(e[6:6+i])
            eval('{:} = \'N\''.format(e[6:6+i]))

    for x in newvar:
        print(f'Dunka\'s tracker new variable: {x}')
    if newvar:
        log.config(text='New variable found for Dunka\'s tracker! Please advise Coxla#2119 on Discord')

    width = 1340 if map == 'M' else 448
    height = (988 if map == 'C' else 744) if sphere == 'Y' else (692 if map == 'C' else 448)

    return url, width+15, height+15+20


# old
# def tracker_url(door, overworld, sphere, map, logic, meta={'spoilers': 'mystery'}):
#     door_url = 'C' if door else 'N'
#     overworld_url = 'F' if overworld else 'N'
#     sphere_url = 'Y' if sphere else 'N'
#     map_url = 'M' if map == 'Normal' else 'C' if map == 'Compact' else 'N'
#     logic_url = 'O' if logic == 'OWG' else 'M' if logic == 'MG / No Logic' else 'N'
#
#     width = 1340 if map_url == 'M' else 448
#     if sphere_url == 'Y':
#         height = 988 if map_url == 'C' else 764
#     else:
#         height = 692 if map_url == 'C' else 468
#
#     if meta['spoilers'] == 'mystery':
#         trackername = 'tracker'
#         type = 'O'
#         entrance = 'N'
#         boss = 'S'
#         enemy = 'S'
#         item = 'A'
#
#         goal = 'G'
#
#         tower = 'R'
#         towercrystals = '7'
#         ganon = 'R'
#         ganoncrystals = '7'
#
#         swords = 'R'
#         spoiler = 'N'
#         mystery = 'S'
#
#         dungeon = '1111'
#
#     else:
#         trackername = 'entrancetracker' if 'shuffle' in meta else 'tracker'
#         type = meta['mode'][0].upper()
#         entrance = 'S' if 'shuffle' in meta else 'N'
#         boss = 'N' if meta['enemizer.boss_shuffle'] == 'none' else 'S'
#         enemy = 'N' if meta['enemizer.enemy_shuffle'] == 'none' else 'S'
#         item = 'A'
#
#         goal = meta['goal'][0].upper()
#         if goal not in ['G','F','P']:
#             if 'dungeons' in meta['goal']:
#                 goal = 'A'
#             else:
#                 goal = 'O'
#
#         towercrystals = meta['entry_crystals_tower'][0].upper()
#         if towercrystals == 'R':
#             tower = 'R'
#             towercrystals = '7'
#         else:
#             tower = 'C'
#
#         ganoncrystals = meta['entry_crystals_ganon'][0].upper()
#         if ganoncrystals == 'R':
#             ganon = 'R'
#             ganoncrystals = '7'
#         else:
#             ganon = 'C'
#
#         swords = meta['weapons'][0].upper()
#         spoiler = 'N'
#         mystery = 'N'
#
#         if len(meta['dungeon_items']) > 4: # Standard shuffle
#             dungeon = '0000'
#         else:
#             dungeon = len(meta['dungeon_items'])*'1' + (4-len(meta['dungeon_items']))*'0'
#
#         if 'name' in meta:
#             if 'Potpourri' in meta['name']:
#                 dungeon = '0011'
#
#         if meta['logic'] == 'NoLogic':
#             dungeon = '1111'
#
#     ambrosia = 'N'
#     autotracking = 'Y'
#     trackingport = '8080'
#     sprite = 'Link'
#     compact = '&map=C' if map_url == 'C' else ''
#
#     url = 'https://alttptracker.dunka.net/{:}.html?f={:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}0{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}&sprite={:}{:}&starting=NNNN'.format(trackername, type, entrance, boss, enemy, logic_url, item, goal, tower, towercrystals, ganon, ganoncrystals, swords, map_url, spoiler, sphere_url, mystery, door_url, dungeon, ambrosia, overworld_url, autotracking, trackingport, sprite, compact)
#     print(url)
#
#     return (url, width, height)

def process_is_running(exe_path, process_list):
    process_name = exe_path[::-1]
    try:
        i = process_name.index('/')
        process_name = process_name[:i][::-1]
    except:
        process_name = ''

    return process_name in process_list

def switch_frame(enable_children, disable_children):
    for child in enable_children:
        child.configure(state='normal')
    for child in disable_children:
        child.configure(state='disabled')

def on_entry_click(entry):
    if entry.cget('fg') == 'grey':
       entry.delete(0, 'end')
       entry.insert(0, '')
       entry.config(fg = 'black')

def on_focusout(entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg = 'grey')

def set_default_text(entry, text):
    entry.bind('<FocusIn>', lambda event: on_entry_click(entry))
    entry.bind('<FocusOut>', lambda event: on_focusout(entry, text))
    if entry.get() == '':
        entry.insert(0, text)
    if entry.get() == text:
        entry.config(fg = 'grey')