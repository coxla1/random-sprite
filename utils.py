from tkinter import filedialog as fd

import os
import shutil
import threading

import json
import asyncio
import webbrowser

import pyz3r

import random as rd

msupacks = []

class thread(threading.Thread):
    def __init__(self, path=None, url=None):
        super().__init__()
        self.path = path
        self.url = url
        self.w = 448+15
        self.h = 988+15
        self.daemon = True

    def run(self):
        if self.url is None:
            os.system('cmd /c \"' + self.path + '\"')
        else:
            os.system('cmd /c start chrome --app="{:}" --user-data-dir="%tmp%\chrome_tmp_dir_tracker" --chrome-frame --window-position=10,200 --window-size={:},{:}'.format(self.url, self.w, self.h))

def set_path(txt, type):
    if type == 'file':
        path = fd.askopenfilename()
    else:
        path = fd.askdirectory()
    txt.set(path)


def toggle_door(door, tracker):
    door.config(state='normal' if tracker.get() else 'disabled')


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


def load_cfg(rom, msu, timerpath, patch, emu, timer, track, doortrack, speed, color, bgm, quickswap, glitches):
    try:
        with open('data/config.json','r') as cfgfile:
            cfg = json.load(cfgfile)
    except:
        cfg = {'rom': '', 'msu': '', 'timerpath': '', 'patch': 0, 'emu': 0, 'timer': 0, 'track': 0, 'doortrack': 0, 'speed': {'off': 0, 'double': 0, 'normal': 0, 'half': 0, 'quarter': 0}, 'color': {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0}, 'bgm': 0, 'quickswap': 0, 'glitches': 0}

    general_set = ['rom', 'msu', 'timerpath', 'patch', 'emu', 'timer', 'track', 'doortrack', 'bgm', 'quickswap', 'glitches']

    speed_set = ['off', 'double', 'normal', 'half', 'quarter']
    color_set = ['red', 'blue', 'green', 'yellow']

    for var in general_set:
        eval(var).set(cfg[var])

    for var in speed_set:
        speed[var].set(cfg['speed'][var])

    for var in color_set:
        color[var].set(cfg['color'][var])


def save_cfg(rom, msu, timerpath, patch, emu, timer, track, doortrack, speed, color, bgm, quickswap, glitches):
    cfg = {'rom': '', 'msu': '', 'timerpath': '', 'patch': 0, 'emu': 0, 'timer': 0, 'track': 0, 'doortrack': 0, 'speed': {'off': 0, 'double': 0, 'normal': 0, 'half': 0, 'quarter': 0}, 'color': {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0}, 'bgm': 0, 'quickswap': 0, 'glitches': 0}

    general_set = ['rom', 'msu', 'timerpath', 'patch', 'emu', 'timer', 'track', 'doortrack', 'bgm', 'quickswap', 'glitches']

    speed_set = ['off', 'double', 'normal', 'half', 'quarter']
    color_set = ['red', 'blue', 'green', 'yellow']

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


def download(seed, rom, msu, timerpath, patch, emu, timer, track, doortrack, speed, color, bgm, quickswap, glitches, msupack, sprites, output, info):
    global msupacks

    if patch.get():
        # Patch the ROM
        speed_val = {}
        for x in speed:
            speed_val[x] = speed[x].get()

        color_val = {}
        for x in color:
            color_val[x] = color[x].get()

        if glitches.get():
            sprite = 'Link'
        else:
            sprites_val = {s: sprites[s]['var'].get() for s in sprites}
            sprite = pick_setting(sprites_val, 'Link')

        try:
            settings = asyncio.run(gen_seed(rom.get(), hash(seed.get()), pick_setting(speed_val, 'normal'), pick_setting(color_val, 'red'), sprite, bgm.get(), quickswap.get()))
        except:
            info.config(text='An error occured while patching the ROM.')
            return -1

        # Choose MSU Pack
        try:
            pack = msupack.get()
            if pack == 'Random':
                pack = msupacks[rd.randint(0, len(msupacks)-1)]

            if pack == 'Default':
                fdir = rom.get()[::-1]
                i = fdir.index('/')
                fdir = fdir[i+1:][::-1]
                fname = 'seed.sfc'
            else:
                fdir = msu.get() + '/' + pack
                for f in os.listdir(fdir)[::-1]:
                    if f[-4:] == '.msu':
                        fname = (f[-5::-1])[::-1] + '.sfc'
                        break

            f = fdir + '/' + fname
            shutil.move(os.getcwd() + '/seed.sfc', f)

        except:
            info.config(text='An error occured while writing to the MSU directory.')
            return -1

        # Start emulator
        if emu.get():
            t_emu = thread(path=f)
            t_emu.start()

        info.config(text='MSU Pack: ' + pack + ' // ' + 'Sprite: ' + sprite)
        output.config(state='normal', command=lambda: webbrowser.open('file://' + fdir))

    if timer.get():
        t_timer = thread(path=timerpath.get())
        t_timer.start()

    if track.get():
        if patch.get():
            url = tracker_url(settings['meta']['spoilers'], 'C' if doortrack.get() else 'N', settings['meta'])
        else:
            url = tracker_url('mystery', 'C' if doortrack.get() else 'N')
        t_tracker = thread(url=url)
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


def tracker_url(spoilers, door, meta=None):
    if spoilers == 'mystery':
        url = 'https://alttptracker.dunka.net/tracker.html?f=ONSNMAGR7R7RCNYS{:}1111NY8080&sprite=link&map=C&starting=N'.format(door)

    else:
        mode = meta['mode'][0].upper()
        entrance = 'S' if 'shuffle' in meta else 'N'
        boss = 'N' if meta['enemizer.boss_shuffle'] == 'none' else 'S'

        goal = meta['goal'][0].upper()
        if goal not in ['G','F','P']:
            if 'dungeons' in meta['goal']:
                goal = 'A'
            else:
                goal = 'O'

        tower_crystals = meta['entry_crystals_tower'][0].upper()
        if tower_crystals == 'R':
            tower = 'R'
            tower_crystals = '7'
        else:
            tower = 'C'

        ganon_crystals = meta['entry_crystals_ganon'][0].upper()
        if ganon_crystals == 'R':
            ganon = 'R'
            ganon_crystals = '7'
        else:
            ganon = 'C'

        swords = meta['weapons'][0].upper()

        dungeon = meta['dungeon_items']
        shuffledmaps = '0'
        shuffledcompasses = '0'
        shuffledsmallkeys = '0'
        shuffledbigkeys = '0'

        if dungeon == 'mc':
            shuffledmaps = '1'
            shuffledcompasses = '1'
        elif dungeon == 'mcs':
            shuffledmaps = '1'
            shuffledcompasses = '1'
            shuffledsmallkeys = '1'
        elif dungeon != 'standard':
            shuffledmaps = '1'
            shuffledcompasses = '1'
            shuffledsmallkeys = '1'
            shuffledbigkeys = '1'

        url = 'https://alttptracker.dunka.net/{:}tracker.html?f={:}{:}{:}NMA{:}{:}{:}{:}{:}{:}CNYN{:}{:}{:}{:}{:}NY8080&sprite=link&map=C&starting=N'.format('entrance' if entrance == 'S' else '', mode, entrance, boss, goal, tower, tower_crystals, ganon, ganon_crystals, swords, door, shuffledmaps, shuffledcompasses, shuffledsmallkeys, shuffledbigkeys)

    return url

