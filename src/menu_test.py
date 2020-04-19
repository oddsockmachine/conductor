from interfaces.oled_sw import OLED

oled = OLED(0)

oled.create_menu(list('abcdefghijklm'))
oled.set_encoder_assignment("encoder")


run = True

while run:
    print(oled.get_text())
    ch = input()
    if ch == 'd':
        oled.menu_scroll('down')
    elif ch == 'u':
        oled.menu_scroll('up')
    elif ch == 'i':
        print(oled.get_menu_item())
    elif ch == 'x':
        run = False

