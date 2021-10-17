import tkinter as tk
import utils
import transfer
# import sprites

# TODO : debug print picked options when this will be back
# TODO : fix (?) check process tracker : I can't because that would mean checking if msedge is running, which might be the case
# TODO : sprites

window = tk.Tk()

# Window settings
window.title('ALTTPR Helper')
window.resizable(width=False,height=False)
window.iconbitmap('data/icon.ico')

n = 0

LBL_WIDTH = 14
ENTRY_WIDTH = 64
BTN_WIDTH = 12
SPIN_WIDTH = 5

frm_dict = {}
lbl_dict = {}
input_dict = {}
btn_dict = {}
var_dict = {}
default_dict = {}

## Main settings
m = 0
frm_dict['main'] = tk.LabelFrame(window, text='Main', bd=2)
frm_dict['main'].grid(row=n, sticky=tk.W+tk.E)


# Seed path / URL (soon)
lbl_dict['seed'] = tk.Label(frm_dict['main'], text='Seed path', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['seed'].grid(row=m, column=0)

var_dict['seed'] = tk.StringVar()
input_dict['seed'] = tk.Entry(frm_dict['main'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['seed'])
input_dict['seed'].grid(row=m, column=1)

btn_dict['seed'] = tk.Button(frm_dict['main'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['seed'], input_dict['seed'], 'file'))
btn_dict['seed'].grid(row=m, column=2)

m += 1

# JP1.0 path
lbl_dict['rom'] = tk.Label(frm_dict['main'], text='JP1.0 ROM path', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['rom'].grid(row=m, column=0)

var_dict['rom'] = tk.StringVar()
input_dict['rom'] = tk.Entry(frm_dict['main'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['rom'])
input_dict['rom'].grid(row=m, column=1)

btn_dict['rom'] = tk.Button(frm_dict['main'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['rom'], input_dict['rom'], 'file'))
btn_dict['rom'].grid(row=m, column=2)

m += 1

# Mode
lbl_dict['mode'] = tk.Label(frm_dict['main'], text='Mode', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['mode'].grid(row=m, column=0)

frm_dict['mode'] = tk.Frame(frm_dict['main'], bd=2)
frm_dict['mode'].grid(row=m, column=1, sticky=tk.W)

var_dict['mode'] = tk.IntVar()
input_dict['mode'] = [None, None]
input_dict['mode'][0] = tk.Radiobutton(frm_dict['mode'], text='Transfer via USB', variable=var_dict['mode'], value=0, command=lambda: utils.switch_frame(frm_dict['transfer'].winfo_children(), frm_dict['copy'].winfo_children()))
input_dict['mode'][0].grid(row=0, column=0)
input_dict['mode'][1] = tk.Radiobutton(frm_dict['mode'], text='Copy file', variable=var_dict['mode'], value=1, command=lambda: utils.switch_frame(frm_dict['copy'].winfo_children(), frm_dict['transfer'].winfo_children()))
input_dict['mode'][1].grid(row=0, column=1)

n += 1

## Transfer via USB
m = 0
frm_dict['transfer'] = tk.LabelFrame(window, text='Transfer via USB', bd=2)
frm_dict['transfer'].grid(row=n, sticky=tk.W+tk.E)

# SNI
btn_dict['detect'] = tk.Button(frm_dict['transfer'], text='Detect FXPak', width=LBL_WIDTH)
btn_dict['detect'].grid(row=m, column=0)

lbl_dict['detect'] = tk.Label(frm_dict['transfer'], text='', anchor=tk.W)
lbl_dict['detect'].grid(row=m, column=1, sticky=tk.W)

m += 1

# MSU List
var_dict['uri'] = tk.StringVar()
lbl_dict['fxpakfolders'] = tk.Label(frm_dict['transfer'], text='MSU folder', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['fxpakfolders'].grid(row=m, column=0)

input_dict['fxpakfolders'] = tk.Listbox(frm_dict['transfer'], width=ENTRY_WIDTH+BTN_WIDTH, height=4)
input_dict['fxpakfolders'].grid(row=m, column=1, sticky=tk.W)

n += 1

## Copy file
m = 0
frm_dict['copy'] = tk.LabelFrame(window, text='Copy file', bd=2)
frm_dict['copy'].grid(row=n, sticky=tk.W+tk.E)

# Emulator
lbl_dict['emulator'] = tk.Label(frm_dict['copy'], text='Emulator', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['emulator'].grid(row=m, column=0)

var_dict['emulator'] = tk.StringVar()
input_dict['emulator'] = tk.Entry(frm_dict['copy'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['emulator'])
input_dict['emulator'].grid(row=m, column=1)
default_dict['emulator'] = 'Optional'

btn_dict['emulator'] = tk.Button(frm_dict['copy'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['emulator'], input_dict['emulator'], 'file'))
btn_dict['emulator'].grid(row=m, column=2)
m += 1

# MSU
lbl_dict['msupath'] = tk.Label(frm_dict['copy'], text='MSU folder', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['msupath'].grid(row=m, column=0)

var_dict['msupath'] = tk.StringVar()
input_dict['msupath'] = tk.Entry(frm_dict['copy'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['msupath'])
input_dict['msupath'].grid(row=m, column=1)
default_dict['msupath'] = 'Seed will be written there if default music used'

btn_dict['msupath'] = tk.Button(frm_dict['copy'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['msupath'], input_dict['msupath'], 'dir'))
btn_dict['msupath'].grid(row=m, column=2)

n += 1

## Misc
m = 0
frm_dict['misc'] = tk.LabelFrame(window, text='Misc', bd=2)
frm_dict['misc'].grid(row=n, sticky=tk.W+tk.E)

# Timer
lbl_dict['timer'] = tk.Label(frm_dict['misc'], text='Timer', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['timer'].grid(row=m, column=0)

var_dict['timer'] = tk.StringVar()
input_dict['timer'] = tk.Entry(frm_dict['misc'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['timer'])
input_dict['timer'].grid(row=m, column=1)
default_dict['timer'] = 'Optional'

btn_dict['timer'] = tk.Button(frm_dict['misc'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['timer'], input_dict['timer'], 'file'))
btn_dict['timer'].grid(row=m, column=2)

m += 1

# Tracker
lbl_dict['tracker'] = tk.Label(frm_dict['misc'], text='Tracker', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['tracker'].grid(row=m, column=0)

var_dict['tracker'] = tk.StringVar()
input_dict['tracker'] = tk.Entry(frm_dict['misc'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['tracker'])
input_dict['tracker'].grid(row=m, column=1)
default_dict['tracker'] = 'Optional, will start Dunka\'s tracker if empty'

btn_dict['tracker'] = tk.Button(frm_dict['misc'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['tracker'], input_dict['tracker'], 'file'))
btn_dict['tracker'].grid(row=m, column=2)

m += 1

# SNI/QUSB2SNES
lbl_dict['usbinterface'] = tk.Label(frm_dict['misc'], text='SNI/QUSB2SNES', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['usbinterface'].grid(row=m, column=0)

var_dict['usbinterface'] = tk.StringVar()
input_dict['usbinterface'] = tk.Entry(frm_dict['misc'], width=ENTRY_WIDTH, exportselection=0, textvariable=var_dict['usbinterface'])
input_dict['usbinterface'].grid(row=m, column=1)
default_dict['usbinterface'] = 'SNI required if FXPak/SD2SNES, otherwise optional'

btn_dict['usbinterface'] = tk.Button(frm_dict['misc'], text='...', width=BTN_WIDTH, command=lambda: utils.set_path(var_dict['usbinterface'], input_dict['usbinterface'], 'file'))
btn_dict['usbinterface'].grid(row=m, column=2)

n += 1

## Autostart
m = 0
frm_dict['autostart'] = tk.LabelFrame(window, text='Autostart', bd=2)
frm_dict['autostart'].grid(row=n, sticky=tk.W+tk.E)

input_dict['autostart'] = {}
var_dict['autostart'] = {}

# Emulator

var_dict['autostart']['boot'] = tk.IntVar()
input_dict['autostart']['boot'] = tk.Checkbutton(frm_dict['autostart'], text='Boot ROM', variable=var_dict['autostart']['boot'], onvalue=1, offvalue=0)
input_dict['autostart']['boot'].grid(row=0, column=m)

m += 1

# Timer
var_dict['autostart']['timer'] = tk.IntVar()
input_dict['autostart']['timer'] = tk.Checkbutton(frm_dict['autostart'], text='Timer', variable=var_dict['autostart']['timer'], onvalue=1, offvalue=0)
input_dict['autostart']['timer'].grid(row=0, column=m)

m += 1

# Tracker
var_dict['autostart']['tracker'] = tk.IntVar()
input_dict['autostart']['tracker'] = tk.Checkbutton(frm_dict['autostart'], text='Tracker', variable=var_dict['autostart']['tracker'], onvalue=1, offvalue=0)
input_dict['autostart']['tracker'].grid(row=0, column=m)

m += 1

# QUSB2SNES
var_dict['autostart']['usbinterface'] = tk.IntVar()
input_dict['autostart']['usbinterface'] = tk.Checkbutton(frm_dict['autostart'], text='SNI/QUSB2SNES', variable=var_dict['autostart']['usbinterface'], onvalue=1, offvalue=0)
input_dict['autostart']['usbinterface'].grid(row=0, column=m)

n += 1

## Dunka's tracker
m = 0
frm_dict['dunkatracker'] = tk.LabelFrame(window, text='Dunka\'s tracker display options', bd=2)
frm_dict['dunkatracker'].grid(row=n, sticky=tk.W+tk.E)

input_dict['dunkatracker'] = {}
var_dict['dunkatracker'] = {}

frm_dict['dunkarow1'] = tk.Frame(frm_dict['dunkatracker'], bd=2)
frm_dict['dunkarow1'].grid(row=0, sticky=tk.W)

# Door tracker
lbl_dict['door'] = tk.Label(frm_dict['dunkarow1'], text='Door Rando', width=LBL_WIDTH)
lbl_dict['door'].grid(row=0, column=m)

m += 1

var_dict['dunkatracker']['door'] = tk.StringVar()
var_dict['dunkatracker']['door'].set('None')
input_dict['dunkatracker']['door'] = tk.OptionMenu(frm_dict['dunkarow1'], var_dict['dunkatracker']['door'], *['None', 'Basic', 'Crossed/Keydrop'])
input_dict['dunkatracker']['door'].config(width=BTN_WIDTH+2)
input_dict['dunkatracker']['door'].grid(row=0, column=m)

m += 1

# Overworld tracker
lbl_dict['overworld'] = tk.Label(frm_dict['dunkarow1'], text='Overworld Rando', width=LBL_WIDTH)
lbl_dict['overworld'].grid(row=0, column=m)

m += 1

var_dict['dunkatracker']['overworld'] = tk.StringVar()
var_dict['dunkatracker']['overworld'].set('None')
input_dict['dunkatracker']['overworld'] = tk.OptionMenu(frm_dict['dunkarow1'], var_dict['dunkatracker']['overworld'], *['None', 'Mixed/Crossed/Misc', 'Parallel', 'Full'])
input_dict['dunkatracker']['overworld'].config(width=BTN_WIDTH+6)
input_dict['dunkatracker']['overworld'].grid(row=0, column=m)

m += 1

# Sphere tracker
var_dict['dunkatracker']['sphere'] = tk.IntVar()
input_dict['dunkatracker']['sphere'] = tk.Checkbutton(frm_dict['dunkarow1'], text='Sphere', variable=var_dict['dunkatracker']['sphere'], onvalue=1, offvalue=0)
input_dict['dunkatracker']['sphere'].grid(row=0, column=m)

m = 0
frm_dict['dunkarow2'] = tk.Frame(frm_dict['dunkatracker'], bd=2)
frm_dict['dunkarow2'].grid(row=1, sticky=tk.W)

# Map tracker
lbl_dict['mapdisplay'] = tk.Label(frm_dict['dunkarow2'], text='Map display', width=LBL_WIDTH)
lbl_dict['mapdisplay'].grid(row=0, column=m)

m += 1

var_dict['dunkatracker']['mapdisplay'] = tk.StringVar()
var_dict['dunkatracker']['mapdisplay'].set('None')
input_dict['dunkatracker']['mapdisplay'] = tk.OptionMenu(frm_dict['dunkarow2'], var_dict['dunkatracker']['mapdisplay'], *['None', 'Normal', 'Compact'])
input_dict['dunkatracker']['mapdisplay'].config(width=BTN_WIDTH+2)
input_dict['dunkatracker']['mapdisplay'].grid(row=0, column=m)

m += 1

# Map logic
lbl_dict['maplogic'] = tk.Label(frm_dict['dunkarow2'], text='Map logic', width=LBL_WIDTH)
lbl_dict['maplogic'].grid(row=0, column=m)

m += 1

var_dict['dunkatracker']['maplogic'] = tk.StringVar()
var_dict['dunkatracker']['maplogic'].set('No Glitches')
input_dict['dunkatracker']['maplogic'] = tk.OptionMenu(frm_dict['dunkarow2'], var_dict['dunkatracker']['maplogic'], *['No Glitches', 'OWG', 'MG/No Logic'])
input_dict['dunkatracker']['maplogic'].config(width=BTN_WIDTH+6)
input_dict['dunkatracker']['maplogic'].grid(row=0, column=m)

m += 1

# Autotracker
var_dict['dunkatracker']['autotracker'] = tk.IntVar()
input_dict['dunkatracker']['autotracker'] = tk.Checkbutton(frm_dict['dunkarow2'], text='Autotracker', variable=var_dict['dunkatracker']['autotracker'], onvalue=1, offvalue=0)
input_dict['dunkatracker']['autotracker'].grid(row=0, column=m)

m = 0
frm_dict['dunkarow3'] = tk.Frame(frm_dict['dunkatracker'], bd=2)
frm_dict['dunkarow3'].grid(row=2, sticky=tk.W)

# Shopsanity
var_dict['dunkatracker']['shopsanity'] = tk.IntVar()
input_dict['dunkatracker']['shopsanity'] = tk.Checkbutton(frm_dict['dunkarow3'], text='Shopsanity', variable=var_dict['dunkatracker']['shopsanity'], onvalue=1, offvalue=0)
input_dict['dunkatracker']['shopsanity'].grid(row=0, column=m)

n += 1

## Postgen options
m = 0
p = 0

frm_dict['postgen'] = tk.LabelFrame(window, text='Post-gen options', bd=2)
frm_dict['postgen'].grid(row=n, sticky=tk.W+tk.E)

frm_dict['heart'] = tk.Frame(frm_dict['postgen'], bd=2)
frm_dict['heart'].grid(row=0, sticky=tk.W)

# Heart speed
lbl_dict['heartspeed'] = {}

lbl_dict['heartspeed']['main'] = tk.Label(frm_dict['heart'], text='Heart speed', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['heartspeed']['main'].grid(row=m, column=p)
p += 1

var_dict['heartspeed'] = {'off' : tk.IntVar(), 'double' : tk.IntVar(), 'normal' : tk.IntVar(), 'half' : tk.IntVar(), 'quarter': tk.IntVar()}

# Speed off
lbl_dict['heartspeed']['off'] = tk.Label(frm_dict['heart'], text='Off', width=SPIN_WIDTH+1)
lbl_dict['heartspeed']['off'].grid(row=m, column=p)
p += 1

input_dict['heartspeed'] = {}

input_dict['heartspeed']['off'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartspeed']['off'])
input_dict['heartspeed']['off'].grid(row=m, column=p)
p += 1

# Speed double
lbl_dict['heartspeed']['double'] = tk.Label(frm_dict['heart'], text='Double', width=SPIN_WIDTH+1)
lbl_dict['heartspeed']['double'].grid(row=m, column=p)
p += 1

input_dict['heartspeed']['double'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartspeed']['double'])
input_dict['heartspeed']['double'].grid(row=m, column=p)
p += 1

# Speed normal
lbl_dict['heartspeed']['normal'] = tk.Label(frm_dict['heart'], text='Normal', width=SPIN_WIDTH+1)
lbl_dict['heartspeed']['normal'].grid(row=m, column=p)
p += 1

input_dict['heartspeed']['normal'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartspeed']['normal'])
input_dict['heartspeed']['normal'].grid(row=m, column=p)
p += 1

# Speed half
lbl_dict['heartspeed']['half'] = tk.Label(frm_dict['heart'], text='Half', width=SPIN_WIDTH+1)
lbl_dict['heartspeed']['half'].grid(row=m, column=p)
p += 1

input_dict['heartspeed']['half'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartspeed']['half'])
input_dict['heartspeed']['half'].grid(row=m, column=p)
p += 1

# Speed quarter
lbl_dict['heartspeed']['quarter'] = tk.Label(frm_dict['heart'], text='Quarter', width=SPIN_WIDTH+1)
lbl_dict['heartspeed']['quarter'].grid(row=m, column=p)
p += 1

input_dict['heartspeed']['quarter'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartspeed']['quarter'])
input_dict['heartspeed']['quarter'].grid(row=m, column=p)

m += 1
p = 0

# Heart color
lbl_dict['heartcolor'] = {}
lbl_dict['heartcolor']['main'] = tk.Label(frm_dict['heart'], text='Heart color', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['heartcolor']['main'].grid(row=m, column=p)
p += 1

input_dict['heartcolor'] = {}

var_dict['heartcolor'] = {'red' : tk.IntVar(), 'blue' : tk.IntVar(), 'green' : tk.IntVar(), 'yellow' : tk.IntVar()}

# Color red
lbl_dict['heartcolor']['red'] = tk.Label(frm_dict['heart'], text='Red', width=SPIN_WIDTH+1)
lbl_dict['heartcolor']['red'].grid(row=m, column=p)
p += 1

input_dict['heartcolor']['red'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartcolor']['red'])
input_dict['heartcolor']['red'].grid(row=m, column=p)
p += 1

# Color blue
lbl_dict['heartcolor']['blue'] = tk.Label(frm_dict['heart'], text='Blue', width=SPIN_WIDTH+1)
lbl_dict['heartcolor']['blue'].grid(row=m, column=p)
p += 1

input_dict['heartcolor']['blue'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartcolor']['blue'])
input_dict['heartcolor']['blue'].grid(row=m, column=p)
p += 1

# Color green
lbl_dict['heartcolor']['green'] = tk.Label(frm_dict['heart'], text='Green', width=SPIN_WIDTH+1)
lbl_dict['heartcolor']['green'].grid(row=m, column=p)
p += 1

input_dict['heartcolor']['green'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartcolor']['green'])
input_dict['heartcolor']['green'].grid(row=m, column=p)
p += 1

# Color yellow
lbl_dict['heartcolor']['yellow'] = tk.Label(frm_dict['heart'], text='Yellow', width=SPIN_WIDTH+1)
lbl_dict['heartcolor']['yellow'].grid(row=m, column=p)
p += 1

input_dict['heartcolor']['yellow'] = tk.Spinbox(frm_dict['heart'], from_=0, to=100, width=SPIN_WIDTH, textvariable=var_dict['heartcolor']['yellow'])
input_dict['heartcolor']['yellow'].grid(row=m, column=p)

m = 0

frm_dict['gameoptions'] = tk.Frame(frm_dict['postgen'], bd=2)
frm_dict['gameoptions'].grid(row=1, sticky=tk.W+tk.E)

# BGM
var_dict['backgroundmusic'] = tk.IntVar()
input_dict['backgroundmusic'] = tk.Checkbutton(frm_dict['gameoptions'], text='Background music',variable=var_dict['backgroundmusic'], onvalue=1, offvalue=0)
input_dict['backgroundmusic'].grid(row=0, column=m)
m += 1

# Quickswap
var_dict['quickswap'] = tk.IntVar()
input_dict['quickswap'] = tk.Checkbutton(frm_dict['gameoptions'], text='Quickswap',variable=var_dict['quickswap'], onvalue=1, offvalue=0)
input_dict['quickswap'].grid(row=0, column=m)

m = 0

frm_dict['sprites'] = tk.Frame(frm_dict['postgen'], bd=2)
frm_dict['sprites'].grid(row=1, sticky=tk.W)


# Edit sprites
btn_dict['editsprites'] = tk.Button(frm_dict['sprites'], text='Sprites list', width=BTN_WIDTH)
btn_dict['editsprites'].grid(row=0, column=m)
m += 1

# Update sprites
btn_dict['updatesprites'] = tk.Button(frm_dict['sprites'], text='Update sprites', width=BTN_WIDTH)
btn_dict['updatesprites'].grid(row=0, column=m)
m += 1

# Glitched logic
var_dict['linksprite'] = tk.IntVar()
input_dict['linksprite'] = tk.Checkbutton(frm_dict['sprites'], text='Force Link sprite (e.g. glitched logic)',variable=var_dict['linksprite'], onvalue=1, offvalue=0)
input_dict['linksprite'].grid(row=0, column=m)

n += 1

## MSU, run and log
frm_dict['msu'] = tk.Frame(window, bd=2)
frm_dict['msu'].grid(row=n, sticky=tk.W+tk.E)

lbl_dict['msu'] = tk.Label(frm_dict['msu'], text='MSU Pack', width=LBL_WIDTH, anchor=tk.W)
lbl_dict['msu'].grid(row=0, column=0)

var_dict['msu'] = tk.StringVar()
var_dict['msu'].set('Default')
input_dict['msu'] = tk.OptionMenu(frm_dict['msu'], var_dict['msu'], *['Default', 'Random'])
input_dict['msu'].config(width=ENTRY_WIDTH-8)
input_dict['msu'].grid(row=0, column=1)

btn_dict['msu'] = tk.Button(frm_dict['msu'], text='Refresh', width=BTN_WIDTH, command=lambda: utils.refresh_msu(var_dict['msupath'], input_dict['msu'], var_dict['msu'], var_dict['mode'], var_dict['uri'], input_dict['fxpakfolders']))
btn_dict['msu'].grid(row=0, column=2)

n += 1

btn_dict['run'] = tk.Button(window, text='RUN')
btn_dict['run'].grid(row=n)

n += 1

lbl_dict['log'] = tk.Label(window, text='', anchor=tk.W, width=80)
lbl_dict['log'].grid(row=n, sticky=tk.W)

## Loading
utils.load_cfg(var_dict)

lbl_dict['rom'].config(state='disabled')
input_dict['rom'].config(state='disabled')
btn_dict['rom'].config(state='disabled')
for child in frm_dict['heart'].winfo_children():
    child.configure(state='disabled')
for child in frm_dict['gameoptions'].winfo_children():
    child.configure(state='disabled')
for child in frm_dict['sprites'].winfo_children():
    child.configure(state='disabled')

for x in default_dict:
    utils.set_default_text(input_dict[x], default_dict[x])

if var_dict['mode'].get() == 0:
    utils.switch_frame(frm_dict['transfer'].winfo_children(), frm_dict['copy'].winfo_children())
else:
    utils.switch_frame(frm_dict['copy'].winfo_children(), frm_dict['transfer'].winfo_children())

btn_dict['run'].config(command=lambda: utils.run(var_dict, input_dict['fxpakfolders'], default_dict, lbl_dict['log']))
btn_dict['detect'].config(command=lambda: transfer.detect_fxpak(var_dict['usbinterface'], input_dict['fxpakfolders'], var_dict['uri'], lbl_dict['detect']))

# sprites.build_dict()
# sprites.load_sprites()
# var_patch.set(0)

window.mainloop()

## Quitting
utils.save_cfg(var_dict)
# sprites.save_sprites()