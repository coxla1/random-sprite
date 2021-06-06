import tkinter as tk
import utils
import sprites

window = tk.Tk()

# Window settings
window.title('Seed downloader')
window.resizable(width=False,height=False)
window.iconbitmap('data/icon.ico')

n = 0

## Paths
m = 0
frm_path = tk.Frame(window, bd=1)
frm_path.grid(row=n, column=0, sticky=tk.W)

# # Seed hash
# lbl_seed = tk.Label(frm_path, text='Seed hash/URL')
# lbl_seed.grid(row=m, column=0, sticky=tk.W)
#
# var_seed = tk.StringVar()
# txt_seed = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_seed)
# txt_seed.grid(row=m, column=1, sticky=tk.W)

# Seed path
lbl_seed = tk.Label(frm_path, text='Seed path')
lbl_seed.grid(row=m, column=0, sticky=tk.W)

var_seed = tk.StringVar()
txt_seed = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_seed)
txt_seed.grid(row=m, column=1, sticky=tk.W)

btn_seed = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_seed, 'file'))
btn_seed.grid(row=m, column=2, sticky=tk.W)

m += 1

# # ROM path
# lbl_rom = tk.Label(frm_path, text='ROM path')
# lbl_rom.grid(row=m, column=0, sticky=tk.W)
#
var_rom = tk.StringVar()
# txt_rom = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_rom)
# txt_rom.grid(row=m, column=1, sticky=tk.W)
#
# btn_rom = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_rom, 'file'))
# btn_rom.grid(row=m, column=2, sticky=tk.W)
#
# m += 1

# MSU folder
lbl_msu = tk.Label(frm_path, text='MSU folder')
lbl_msu.grid(row=m, column=0, sticky=tk.W)

var_msu = tk.StringVar()
txt_msu = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_msu)
txt_msu.grid(row=m, column=1, sticky=tk.W)

btn_msu = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_msu, 'dir'))
btn_msu.grid(row=m, column=2, sticky=tk.W)

m += 1

# Emulator path
lbl_emu = tk.Label(frm_path, text='Emulator path*')
lbl_emu.grid(row=m, column=0, sticky=tk.W)

var_emupath = tk.StringVar()
txt_emu = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_emupath)
txt_emu.grid(row=m, column=1, sticky=tk.W)

btn_emu = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_emupath, 'file'))
btn_emu.grid(row=m, column=2, sticky=tk.W)

m += 1

# Timer path
lbl_timer = tk.Label(frm_path, text='Timer path*')
lbl_timer.grid(row=m, column=0, sticky=tk.W)

var_timerpath = tk.StringVar()
txt_timer = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_timerpath)
txt_timer.grid(row=m, column=1, sticky=tk.W)

btn_timer = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_timerpath, 'file'))
btn_timer.grid(row=m, column=2, sticky=tk.W)

m += 1

# QUSB2SNES path
lbl_usb = tk.Label(frm_path, text='QUSB2SNES path*')
lbl_usb.grid(row=m, column=0, sticky=tk.W)

var_usbpath = tk.StringVar()
txt_usb = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_usbpath)
txt_usb.grid(row=m, column=1, sticky=tk.W)

btn_usb = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_usbpath, 'file'))
btn_usb.grid(row=m, column=2, sticky=tk.W)

m += 1

# Tracker path
lbl_tracker = tk.Label(frm_path, text='Tracker path**')
lbl_tracker.grid(row=m, column=0, sticky=tk.W)

var_trackpath = tk.StringVar()
txt_track = tk.Entry(frm_path, width=64, exportselection=0, textvariable=var_trackpath)
txt_track.grid(row=m, column=1, sticky=tk.W)

btn_track = tk.Button(frm_path, text='...', width=10, command=lambda: utils.set_path(var_trackpath, 'file'))
btn_track.grid(row=m, column=2, sticky=tk.W)

n += 1

## Checkboxes
m = 0
frm_check = tk.Frame(window, bd=1)
frm_check.grid(row=n, column=0, sticky=tk.W)

# Patch ROM
var_patch = tk.IntVar()
chk_patch = tk.Checkbutton(frm_check, text='Patch ROM',variable=var_patch, onvalue=1, offvalue=0, state='disabled')
chk_patch.grid(row=0, column=m, sticky=tk.W)

m += 1

# Emulator
var_emu = tk.IntVar()
chk_emu = tk.Checkbutton(frm_check, text='Start emulator',variable=var_emu, onvalue=1, offvalue=0)
chk_emu.grid(row=0, column=m, sticky=tk.W)

m += 1

# Timer
var_timer = tk.IntVar()
chk_timer = tk.Checkbutton(frm_check, text='Start timer',variable=var_timer, onvalue=1, offvalue=0)
chk_timer.grid(row=0, column=m, sticky=tk.W)

m += 1

# QUSB2SNES
var_usb = tk.IntVar()
chk_usb = tk.Checkbutton(frm_check, text='Start QUSB2SNES',variable=var_usb, onvalue=1, offvalue=0)
chk_usb.grid(row=0, column=m, sticky=tk.W)

m += 1

# Tracker
var_track = tk.IntVar()
chk_track = tk.Checkbutton(frm_check, text='Start tracker',variable=var_track, onvalue=1, offvalue=0)
chk_track.grid(row=0, column=m, sticky=tk.W)

n += 1

## Dunka's tracker
m = 0
frm_track = tk.Frame(window, bd=1)
frm_track.grid(row=n, column=0, sticky=tk.W)

# Door tracker
var_door = tk.IntVar()
chk_door = tk.Checkbutton(frm_track, text='Door',variable=var_door, onvalue=1, offvalue=0)
chk_door.grid(row=0, column=m, sticky=tk.W)

m += 1

# Overworld tracker
var_overworld = tk.IntVar()
chk_overworld = tk.Checkbutton(frm_track, text='Overworld',variable=var_overworld, onvalue=1, offvalue=0)
chk_overworld.grid(row=0, column=m, sticky=tk.W)

m += 1

# Sphere tracker
var_sphere = tk.IntVar()
chk_sphere = tk.Checkbutton(frm_track, text='Sphere',variable=var_sphere, onvalue=1, offvalue=0)
chk_sphere.grid(row=0, column=m, sticky=tk.W)

m += 1

# Map tracker
lbl_map = tk.Label(frm_track, text='Map/Logic')
lbl_map.grid(row=0, column=m, sticky=tk.W)

m += 1

var_map = tk.StringVar()
var_map.set('None')
lst_map = tk.OptionMenu(frm_track, var_map, *['None', 'Normal', 'Compact'])
lst_map.config(width=12)
lst_map.grid(row=0, column=m, sticky=tk.W)

m += 1

# Map logic
var_logic = tk.StringVar()
var_logic.set('None')
lst_logic = tk.OptionMenu(frm_track, var_logic, *['No Glitches', 'OWG', 'MG / No Logic'])
lst_logic.config(width=12)
lst_logic.grid(row=0, column=m, sticky=tk.W)

n += 1

## Speed / color settings
m = 0
p = 0
frm_heart = tk.Frame(window, bd=1)
frm_heart.grid(row=n, column=0, sticky=tk.W)

# Heart speed
lbl_speed = tk.Label(frm_heart, text='Heart speed:')
lbl_speed.grid(row=m, column=p, sticky=tk.W)
p += 1

var_speed = {'off' : tk.IntVar(), 'double' : tk.IntVar(), 'normal' : tk.IntVar(), 'half' : tk.IntVar(), 'quarter': tk.IntVar()}

# Speed off
lbl_speed_off = tk.Label(frm_heart, text='Off')
lbl_speed_off.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_speed_off = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_speed['off'])
spn_speed_off.grid(row=m, column=p, sticky=tk.W)
p += 1

# Speed double
lbl_speed_double = tk.Label(frm_heart, text='Double')
lbl_speed_double.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_speed_double = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_speed['double'])
spn_speed_double.grid(row=m, column=p, sticky=tk.W)
p += 1

# Speed normal
lbl_speed_normal = tk.Label(frm_heart, text='Normal')
lbl_speed_normal.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_speed_normal = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_speed['normal'])
spn_speed_normal.grid(row=m, column=p, sticky=tk.W)
p += 1

# Speed half
lbl_speed_half = tk.Label(frm_heart, text='Half')
lbl_speed_half.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_speed_half = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_speed['half'])
spn_speed_half.grid(row=m, column=p, sticky=tk.W)
p += 1

# Speed quarter
lbl_speed_quarter = tk.Label(frm_heart, text='Quarter')
lbl_speed_quarter.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_speed_quarter = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_speed['quarter'])
spn_speed_quarter.grid(row=m, column=p, sticky=tk.W)

m += 1
p = 0

# Heart color
lbl_color = tk.Label(frm_heart, text='Heart color:')
lbl_color.grid(row=m, column=p, sticky=tk.W)
p += 1

var_color = {'red' : tk.IntVar(), 'blue' : tk.IntVar(), 'green' : tk.IntVar(), 'yellow' : tk.IntVar()}

# Color red
lbl_color_red = tk.Label(frm_heart, text='Red')
lbl_color_red.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_color_red = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_color['red'])
spn_color_red.grid(row=m, column=p, sticky=tk.W)
p += 1

# Color blue
lbl_color_blue = tk.Label(frm_heart, text='Blue')
lbl_color_blue.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_color_blue = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_color['blue'])
spn_color_blue.grid(row=m, column=p, sticky=tk.W)
p += 1

# Color green
lbl_color_green = tk.Label(frm_heart, text='Green')
lbl_color_green.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_color_green = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_color['green'])
spn_color_green.grid(row=m, column=p, sticky=tk.W)
p += 1

# Color yellow
lbl_color_yellow = tk.Label(frm_heart, text='Yellow')
lbl_color_yellow.grid(row=m, column=p, sticky=tk.W)
p += 1

spn_color_yellow = tk.Spinbox(frm_heart, from_=0, to=100, width=4, textvariable=var_color['yellow'])
spn_color_yellow.grid(row=m, column=p, sticky=tk.W)

n += 1

## BGM / Quickswap / Glitched logic
m = 0
frm_game = tk.Frame(window, bd=1)
frm_game.grid(row=n, column=0, sticky=tk.W)

# BGM
var_bgm = tk.IntVar()
chk_bgm = tk.Checkbutton(frm_game, text='Background music',variable=var_bgm, onvalue=1, offvalue=0)
chk_bgm.grid(row=0, column=m, sticky=tk.W)
m += 1

# Quickswap
var_quickswap = tk.IntVar()
chk_quickswap = tk.Checkbutton(frm_game, text='Quickswap',variable=var_quickswap, onvalue=1, offvalue=0)
chk_quickswap.grid(row=0, column=m, sticky=tk.W)
m += 1

# Glitched logic
var_glitches = tk.IntVar()
chk_glitches = tk.Checkbutton(frm_game, text='Glitched logic (forces Link sprite)',variable=var_glitches, onvalue=1, offvalue=0)
chk_glitches.grid(row=0, column=m, sticky=tk.W)

n += 1

## MSU Choice
frm_msupack = tk.Frame(window, bd=1)
frm_msupack.grid(row=n, column=0, sticky=tk.W)

lbl_msupack = tk.Label(frm_msupack, text='MSU Pack')
lbl_msupack.grid(row=0, column=0, sticky=tk.W)

var_msupack = tk.StringVar()
var_msupack.set('Default')
lst_msupack = tk.OptionMenu(frm_msupack, var_msupack, *['Default', 'Random'])
lst_msupack.config(width=64)
lst_msupack.grid(row=0, column=1, sticky=tk.W)

btn_msupack = tk.Button(frm_msupack, text='Refresh', width=10, command=lambda: utils.refresh_msu(var_msu.get(), lst_msupack, var_msupack))
btn_msupack.grid(row=0, column=2, sticky=tk.W)

n += 1

## Buttons
m = 0
frm_buttons = tk.Frame(window, bd=1)
frm_buttons.grid(row=n, column=0)

# Download
# btn_download = tk.Button(frm_buttons, text='Download seed')
btn_download = tk.Button(frm_buttons, text='Run')
btn_download.grid(row=0, column=m, sticky=tk.W)

m += 1

# Output
btn_output = tk.Button(frm_buttons, text='Output directory', state='disabled')
btn_output.grid(row=0, column=m, sticky=tk.W)

m += 1

# Edit sprites
btn_edit = tk.Button(frm_buttons, text='Edit sprites list', command=lambda: sprites.window(window))
btn_edit.grid(row=0, column=m, sticky=tk.W)

m += 1

# Help
btn_help = tk.Button(frm_buttons, text='Help', command=lambda: utils.help(window))
btn_help.grid(row=0, column=m, sticky=tk.W)

n += 1

## MSU and sprite informations
lbl_info = tk.Label(window, text='')
lbl_info.grid(row=n, column=0, sticky=tk.W)

# btn_download.config(command=lambda: utils.download(var_seed, var_rom, var_msu, var_emupath, var_timerpath, var_usbpath, var_trackpath, var_patch, var_emu, var_timer, var_usb, var_track, var_door, var_sphere, var_map, var_logic, var_speed, var_color, var_bgm, var_quickswap, var_glitches, var_msupack, sprites.sprites, btn_output, lbl_info))
btn_download.config(command=lambda: utils.helper(var_seed, var_msu, var_emupath, var_timerpath, var_usbpath, var_trackpath, var_emu, var_timer, var_usb, var_track, var_door, var_overworld, var_sphere, var_map, var_logic, var_glitches, var_msupack, btn_output, lbl_info))

# Loading
utils.load_cfg(var_rom, var_msu, var_emupath, var_timerpath, var_usbpath, var_trackpath, var_patch, var_emu, var_timer, var_usb, var_track, var_door, var_sphere, var_map, var_logic, var_speed, var_color, var_bgm, var_quickswap, var_glitches)
utils.refresh_msu(var_msu.get(), lst_msupack, var_msupack)
sprites.build_dict()
sprites.load_sprites()
var_patch.set(0)

# Run
window.mainloop()

# Quitting
utils.save_cfg(var_rom, var_msu, var_emupath, var_timerpath, var_usbpath, var_trackpath, var_patch, var_emu, var_timer, var_usb, var_track, var_door, var_sphere, var_map, var_logic, var_speed, var_color, var_bgm, var_quickswap, var_glitches)
sprites.save_sprites()