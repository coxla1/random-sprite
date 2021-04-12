import tkinter as tk
import ast

from PIL import Image, ImageTk
import urllib.request
import io
import json

sprites = {}
lbl_sprite = {}

def build_dict():
    global sprites
    sprites = {s['name']: {'author': s['author'], 'xmin': s['xmin'], 'xmax': s['xmax'], 'var': tk.IntVar()} for s in ast.literal_eval(open('data/sprites.txt', 'r').read())}


def download():
    v = open('data/version.txt', 'r').read()
    url = 'https://alttpr.s3.us-east-2.amazonaws.com/sprites.' + v + '.png'
    with urllib.request.urlopen(url) as u:
        stream = io.BytesIO(u.read())
    Image.open(stream).save('data/sprites.png')


def hover(event, var, leave=0):
    global sprites
    global lbl_sprite

    if leave:
        var.set('')
    else:
        x = event.widget
        s = [y for y in lbl_sprite if lbl_sprite[y] == x][0]
        var.set(s + ' ' + sprites[s]['author'])


def window(master):
    global sprites
    global lbl_sprite

    window = tk.Toplevel(master)
    window.title('Edit sprites weights')
    window.resizable(width=False,height=False)
    window.iconbitmap('data/icon.ico')

    frm_sprites = tk.Frame(window, border=1)
    frm_sprites.grid(row=0, column=0, sticky=tk.W)

    frm_info = tk.Frame(window, border=1)
    frm_info.grid(row=1, column=0, sticky=tk.W)

    var_info = tk.StringVar()
    lbl_info = tk.Label(frm_info, text ='', textvariable=var_info)
    lbl_info.grid(row=0, column=0, sticky=tk.W)

    try:
        f = Image.open('data/sprites.png')
    except:
        download()
        f = Image.open('data/sprites.png')

    x, y = 16, 24
    scale = 1

    m = 0
    q = 15
    r = 0
    lbl_sprite = {}
    for s in sprites:
        sprt = f.crop((sprites[s]['xmin'],0,sprites[s]['xmax']-1,y-1))
        sprt = sprt.resize((int(scale*x),int(scale*y)), resample=Image.NEAREST)
        sprt = ImageTk.PhotoImage(sprt)

        lbl_sprite[s] = tk.Label(frm_sprites, image=sprt)
        lbl_sprite[s].image = sprt

        lbl_sprite[s].bind('<Enter>', lambda evt: hover(evt, var_info))
        lbl_sprite[s].bind('<Leave>', lambda evt: hover(evt, var_info, leave=1))

        lbl_sprite[s].grid(row=m, column=r, sticky=tk.W)
        r += 1

        spn_sprite = tk.Spinbox(frm_sprites, from_=0, to=100, width=4, textvariable=sprites[s]['var'])
        spn_sprite.grid(row=m, column=r, sticky=tk.W)
        r = (r+1)%(2*q)
        if r == 0:
            m += 1

def load_sprites():
    global sprites
    try:
        with open('data/list.json','r') as cfgfile:
            weights = json.load(cfgfile)
    except:
        weights = {s: 0 for s in sprites}

    for s in sprites:
        sprites[s]['var'].set(weights[s])


def save_sprites():
    global sprites

    weights = {s: sprites[s]['var'].get() for s in sprites}
    with open('data/list.json','w') as cfgfile:
        json.dump(weights, cfgfile, indent=4)
