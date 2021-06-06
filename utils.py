from tkinter import filedialog as fd

import os
import subprocess
import shutil
import threading

import json
import asyncio
import webbrowser

import tkinter as tk
import pyz3r

import random as rd

msupacks = []

default_cfg = {'rom': '', 'msu': '', 'emupath': '', 'timerpath': '', 'usbpath': '', 'trackpath': '', 'patch': 0, 'emu': 0, 'timer': 0, 'usb': 0, 'track': 0, 'door': 0, 'sphere' : 0, 'map': 'None', 'logic': 'No Glitches', 'speed': {'off': 0, 'double': 0, 'normal': 0, 'half': 0, 'quarter': 0}, 'color': {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0}, 'bgm': 0, 'quickswap': 0, 'glitches': 0}

general_set = ['rom', 'msu', 'emupath', 'timerpath', 'usbpath', 'trackpath', 'patch', 'emu', 'timer', 'usb', 'track', 'door', 'sphere', 'map', 'logic', 'bgm', 'quickswap', 'glitches']
speed_set = ['off', 'double', 'normal', 'half', 'quarter']
color_set = ['red', 'blue', 'green', 'yellow']

class thread(threading.Thread):
    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.daemon = True

    def run(self):
        subprocess.call(self.cmd)

def set_path(txt, type):
    if type == 'file':
        path = fd.askopenfilename()
    else:
        path = fd.askdirectory()
    txt.set(path)


def refresh_msu(path, lst_msupack, var_msupack):
    global msupacks
    msupacks = []
    if path:
        try:
            msupacks.extend(os.listdir(path))
        except:
            msupacks.extend([])

    msupacks.sort()
    lst_msupack.children['menu'].delete(0,'end')

    for c in ['Default', 'Random']:
        lst_msupack.children['menu'].add_command(label=c, command=lambda x=c: var_msupack.set(x))

    for c in msupacks:
        lst_msupack.children['menu'].add_command(label=c, command=lambda x=c: var_msupack.set(x))

    msupacks.append('Default')
    var_msupack.set('Default')


def load_cfg(rom, msu, emupath, timerpath, usbpath, trackpath, patch, emu, timer, usb, track, door, sphere, map, logic, speed, color, bgm, quickswap, glitches):
    global default_cfg, general_set, speed_set, color_set

    try:
        with open('data/config.json','r') as cfgfile:
            cfg = json.load(cfgfile)
    except:
        cfg = default_cfg

    for var in general_set:
        try:
            eval(var).set(cfg[var])
        except:
            eval(var).set(default_cfg[var])

    for var in speed_set:
        try:
            speed[var].set(cfg['speed'][var])
        except:
            speed[var].set(default_cfg['speed'][var])

    for var in color_set:
        try:
            color[var].set(cfg['color'][var])
        except:
            color[var].set(default_cfg['color'][var])


def save_cfg(rom, msu, emupath, timerpath, usbpath, trackpath, patch, emu, timer, usb, track, door, sphere, map, logic, speed, color, bgm, quickswap, glitches):
    global default_cfg, general_set, speed_set, color_set

    cfg = default_cfg

    for var in general_set:
        cfg[var] = eval(var).get()

    for var in speed_set:
        cfg['speed'][var] = speed[var].get()

    for var in color_set:
        cfg['color'][var] = color[var].get()

    with open('data/config.json','w') as cfgfile:
        json.dump(cfg, cfgfile, indent=4)


async def gen_seed(rom, hash, speed, color, sprite, bgm, quickswap):
    base_rom = await pyz3r.rom.read(rom)
    seed = await pyz3r.alttpr(hash_id=hash)
    patched_rom = await seed.create_patched_game(base_rom, heartspeed=speed, heartcolor=color, spritename=sprite, music=bgm, quickswap=quickswap)

    await pyz3r.rom.write(patched_rom, os.getcwd() + '/seed.sfc')
    return seed.data['spoiler']


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
#             return -1
#
#         # Choose MSU Pack
#         try:
#             pack = msupack.get()
#             if pack == 'Random':
#                 pack = msupacks[rd.randint(0, len(msupacks)-1)]
#
#             if pack == 'Default':
#                 fdir = rom.get()[::-1]
#                 i = fdir.index('/')
#                 fdir = fdir[i:][::-1]
#                 fname = 'seed.sfc'
#             else:
#                 fdir = msu.get() + '/' + pack
#                 for f in os.listdir(fdir)[::-1]:
#                     if f[-4:] == '.msu':
#                         fname = (f[-5::-1])[::-1] + '.sfc'
#                         break
#
#             f = fdir + '/' + fname
#             shutil.move(os.getcwd() + '/seed.sfc', f)
#
#         except:
#             info.config(text='An error occured while writing to the MSU directory.')
#             return -1
#
#         # Start emulator
#         if emu.get():
#             t_emu = thread('"{:}" "{:}"'.format(emupath.get(), f))
#             t_emu.start()
#
#         info.config(text='MSU Pack: ' + pack + ' // ' + 'Sprite: ' + sprite)
#         output.config(state='normal', command=lambda: webbrowser.open('file://' + fdir))
#
#     # Start timer
#     if timer.get():
#         print('time')
#         t_timer = thread(timerpath.get())
#         t_timer.start()
#
#     # Start QUSB2SNES
#     if usb.get():
#         print('usb')
#         t_usb = thread(usbpath.get())
#         t_usb.start()
#
#     # Start tracker
#     if track.get():
#         if trackpath.get():
#             t_tracker = thread(trackpath.get())
#             t_tracker.start()
#         else:
#             if patch.get():
#                 url, w, h = tracker_url(settings['meta']['spoilers'], door.get(), sphere.get(), map.get(), logic.get(), settings['meta'])
#             else:
#                 url, w, h = tracker_url('mystery', door.get(), sphere.get(), map.get(), logic.get())
#             t_tracker = thread('cmd /c start chrome --app="{:}" --user-data-dir="%tmp%\chrome_tmp_dir_tracker" --chrome-frame --window-position=10,10 --window-size={:},{:}'.format(url, w+15, h+15))
#             t_tracker.start()


async def seed_settings(hash):
    seed = await pyz3r.alttpr(hash_id=hash)
    return seed.data['spoiler']


def helper(seed, msu, emupath, timerpath, usbpath, trackpath, emu, timer, usb, track, door, sphere, map, logic, glitches, msupack, output, info):
    global msupacks

    if seed.get():
        hash = seed.get()[-14:-4]
        try:
            settings = asyncio.run(seed_settings(hash))
        except:
            settings = []

        # Choose MSU Pack
        try:
            pack = msupack.get()
            if pack == 'Random':
                pack = msupacks[rd.randint(0, len(msupacks)-1)]

            if pack == 'Default':
                fdir = msu.get()
                fname = 'seed.sfc'
            else:
                fdir = msu.get() + '/' + pack
                for f in os.listdir(fdir)[::-1]:
                    if f[-4:] == '.msu':
                        fname = (f[-5::-1])[::-1] + '.sfc'
                        break

            f = fdir + '/' + fname
            shutil.copy(seed.get(), f)

        except:
            info.config(text='An error occured while writing to the MSU directory.')
            return -1

        # Start emulator
        if emu.get():
            t_emu = thread('"{:}" "{:}"'.format(emupath.get(), f))
            t_emu.start()

        info.config(text='MSU Pack: ' + pack)
        output.config(state='normal', command=lambda: webbrowser.open('file://' + fdir))

    # Start timer
    if timer.get():
        print('time')
        t_timer = thread(timerpath.get())
        t_timer.start()

    # Start QUSB2SNES
    if usb.get():
        print('usb')
        t_usb = thread(usbpath.get())
        t_usb.start()

    # Start tracker
    if track.get():
        if trackpath.get():
            t_tracker = thread(trackpath.get())
            t_tracker.start()
        else:
            if seed.get() and settings:
                url, w, h = tracker_url(door.get(), sphere.get(), map.get(), logic.get(), settings['meta'])
            else:
                url, w, h = tracker_url(door.get(), sphere.get(), map.get(), logic.get())
            t_tracker = thread('cmd /c start chrome --app="{:}" --user-data-dir="%tmp%\chrome_tmp_dir_tracker" --chrome-frame --window-position=10,10 --window-size={:},{:}'.format(url, w+15, h+15))
            t_tracker.start()


def hash(url):
    if '/' in url:
        tmp = url[::-1]
        h = tmp[:tmp.find('/')][::-1]
    else:
        h = url
    return h


def pick_setting(weights, default=''):
    l = []
    for x in weights:
        for _ in range((weights[x])):
            l.append(x)
    if len(l) == 0:
        return default
    return l[rd.randint(0, len(l)-1)]


def tracker_url(door, sphere, map, logic, meta={'spoilers': 'mystery'}):
    door_url = 'C' if door else 'N'
    overworld = 'F' if door else 'N'
    sphere_url = 'Y' if sphere else 'N'
    map_url = 'M' if map == 'Normal' else 'C' if map == 'Compact' else 'N'
    logic_url = 'O' if logic == 'OWG' else 'M' if logic == 'MG / No Logic' else 'N'

    width = 1340 if map_url == 'M' else 448
    if sphere_url == 'Y':
        height = 988 if map_url == 'C' else 764
    else:
        height = 692 if map_url == 'C' else 468

    if meta['spoilers'] == 'mystery':
        trackername = 'tracker'
        type = 'O'
        entrance = 'N'
        boss = 'S'
        enemy = 'S'
        item = 'A'

        goal = 'G'

        tower = 'R'
        towercrystals = '7'
        ganon = 'R'
        ganoncrystals = '7'

        swords = 'R'
        spoiler = 'N'
        mystery = 'S'

        dungeon = '1111'

    else:
        trackername = 'entrancetracker' if 'shuffle' in meta else 'tracker'
        type = meta['mode'][0].upper()
        entrance = 'S' if 'shuffle' in meta else 'N'
        boss = 'N' if meta['enemizer.boss_shuffle'] == 'none' else 'S'
        enemy = 'N' if meta['enemizer.enemy_shuffle'] == 'none' else 'S'
        item = 'A'

        goal = meta['goal'][0].upper()
        if goal not in ['G','F','P']:
            if 'dungeons' in meta['goal']:
                goal = 'A'
            else:
                goal = 'O'

        towercrystals = meta['entry_crystals_tower'][0].upper()
        if towercrystals == 'R':
            tower = 'R'
            towercrystals = '7'
        else:
            tower = 'C'

        ganoncrystals = meta['entry_crystals_ganon'][0].upper()
        if ganoncrystals == 'R':
            ganon = 'R'
            ganoncrystals = '7'
        else:
            ganon = 'C'

        swords = meta['weapons'][0].upper()
        spoiler = 'N'
        mystery = 'N'

        if len(meta['dungeon_items']) > 4: # Standard shuffle
            dungeon = '0000'
        else:
            dungeon = len(meta['dungeon_items'])*'1' + (4-len(meta['dungeon_items']))*'0'

        if 'name' in meta:
            if 'Potpourri' in meta['name']:
                dungeon = '0011'

    ambrosia = 'N'
    autotracking = 'Y'
    trackingport = '8080'
    sprite = 'Link'
    compact = '&map=C' if map_url == 'C' else ''

    url = 'https://alttptracker.dunka.net/{:}.html?f={:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}{:}&sprite={:}{:}&starting=NNNN'.format(trackername, type, entrance, boss, enemy, logic_url, item, goal, tower, towercrystals, ganon, ganoncrystals, swords, map_url, spoiler, sphere_url, mystery, door_url, dungeon, ambrosia, overworld, autotracking, trackingport, sprite, compact)

    return (url, width, height)

def help(master):

    window = tk.Toplevel(master)
    window.title('Help')
    window.resizable(width=False,height=False)
    window.iconbitmap('data/icon.ico')

    txt_help = 'If you choose to use the default MSU Pack, your seed will be written to the MSU folder.\n\nPaths marked with a * or ** are optional\n\nIf tracker path is left empty, start tracker will then launch Dunka\'s one (requires Chrome).\n\nThe second line of checkboxes refers to Dunka\'s tracker options.\n\nIf all weights are set to zero, setting will be picked at random.\n\nAll configurations are saved when closing the program.'

    frm_help = tk.Frame(window, border=1)
    frm_help.grid(row=0, column=0, sticky=tk.W)

    lbl_help = tk.Label(frm_help, text=txt_help)
    lbl_help.grid(row=0, column=0, sticky=tk.W)