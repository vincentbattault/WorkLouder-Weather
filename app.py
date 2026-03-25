import wlsdk as wl
import lvgl as lv
import gc

wlabel = lv.label(lv_root)
wlabel.set_text("")
wlabel.set_style_text_font(wl.ui.FONT.SMALL, 0)
wlabel.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
wlabel.set_width(170)
wlabel.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
wlabel.set_pos(0, 8)

t = lv.label(lv_root)
t.set_text("--")
t.set_style_text_font(wl.ui.FONT.BIG, 0)
t.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
t.set_width(170)
t.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
t.set_pos(0, 70)

box = lv.obj(lv_root)
box.set_size(150, 80)
box.set_pos(10, 230)
box.set_style_bg_color(lv.color_hex(0x111111), 0)
box.set_style_bg_opa(255, 0)
box.set_style_radius(8, 0)
box.set_style_border_width(0, 0)
box.set_style_pad_all(12, 0)
box.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

dot = lv.obj(box)
dot.set_size(10, 10)
dot.set_style_radius(5, 0)
dot.set_style_bg_color(lv.color_hex(0x39FF14), 0)
dot.set_style_bg_opa(255, 0)
dot.set_style_border_width(0, 0)
dot.set_pos(118, 4)

info = lv.label(box)
info.set_text("...")
info.set_style_text_font(wl.ui.FONT.SMALL, 0)
info.set_style_text_color(lv.color_hex(0x828282), 0)
info.set_pos(0, 20)

ville = lv.label(box)
ville.set_text("...")
ville.set_style_text_font(wl.ui.FONT.SMALL, 0)
ville.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
ville.set_pos(0, 0)

hilo = lv.label(lv_root)
hilo.set_text("")
hilo.set_style_text_font(wl.ui.FONT.SMALL, 0)
hilo.set_style_text_color(lv.color_hex(0xFFFFFF), 0)
hilo.set_width(170)
hilo.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
hilo.set_pos(0, 110)

gc.collect()

def on_data(ctx, p):
    if p and p.get("found"):
        t.set_text(str(int(p.get("temp", 0))))
        wlabel.set_text(str(p.get("label", "")))
        lo = str(int(p.get("temp_min", 0)))
        hi = str(int(p.get("temp_max", 0)))
        hilo.set_text("min. " + lo + "°  /  max. " + hi + "°")
        city = str(p.get("city", ""))
        w = str(int(p.get("wind", 0)))
        h = str(p.get("humidity", 0))
        ville.set_text(city)
        info.set_text(w + " km/h   \n" + h + "%")
        c = int(p.get("code", 0))
        if c <= 1:
            g1, g2 = 0xFFDD00, 0xFF5A00
        elif c <= 3:
            g1, g2 = 0x011D39, 0xFFFFFF
        elif c <= 67:
            g1, g2 = 0x005199, 0xCDCDCD
        elif c <= 86:
            g1, g2 = 0x6EBEFF, 0xFFFFFF
        else:
            g1, g2 = 0xE570FF, 0x939EFF
        lv_root.set_style_bg_color(lv.color_hex(g1), 0)
        lv_root.set_style_bg_grad_color(lv.color_hex(g2), 0)
    wl.rpc.send_response(ctx, p)
    gc.collect()

wl.rpc.register("weather.data", on_data)
lv_root.set_style_bg_color(lv.color_hex(0xFF8C00), 0)
lv_root.set_style_bg_grad_color(lv.color_hex(0xE65100), 0)
lv_root.set_style_bg_grad_dir(lv.GRAD_DIR.VER, 0)
lv_root.set_style_bg_opa(255, 0)

def start():
    wl.rpc.send_notify("weather.fetch", "")
