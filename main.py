from random import randint
import PySimpleGUI as psg


def generate_digits() -> list:
    digits = []
    while len(digits) < 4:
        d = randint(0, 9)
        if d not in digits:
            digits.append(d)
    return digits


def generate_inequalities(digits: list) -> list:
    i = 1
    ineqs = []
    while i < len(digits):
        a = digits[i - 1]
        b = digits[i]
        if a < b:
            symbol = "<"
        elif a > b:
            symbol = ">"
        else:
            symbol = "="
        ineqs.append(symbol)
        i += 1
    return ineqs


def user_password_check(lista: list) -> bool:
    for num in lista:
        try:
            int(num)
        except ValueError:
            return False
    return True

def validity_check(original: list, user: list) -> str:
    if len(original) != len(user):
        return False
    i = 0
    while i < len(original):
        if original[i] != int(user[i]):
            return "Nie udało się!"
        i += 1
    return "Wchodzę!"


def gui():
    attempts = 1
    digits = generate_digits()
    ineqs = generate_inequalities(digits)
    running = True
    hacking = False
    while running:
        digits_text = [psg.Push(background_color="sky blue")]
        for i in range(0, 4):
            digits_text.append(psg.Input("*", justification="center", background_color="sky blue",
                                         font=("Arial", 18, "bold"), size=3, border_width=0, key=f"-DIGIT{i}-",
                                         disabled=False))
            if i < 3:
                if hacking:
                    digits_text.append(psg.Text(f"{ineqs[i]}", justification="center", background_color="sky blue",
                                                font=("Arial", 13)))
                else:
                    digits_text.append(
                        psg.Text("-", justification="center", background_color="sky blue", font=("Arial", 13)))
        digits_text.append(psg.Push(background_color="sky blue"))
        button_size = (4, 2)
        psg.theme("DarkTeal12")
        digits_frame = psg.Frame("", [
            [psg.VPush()],
            [psg.Push(), psg.Button("7", size=button_size, key="-7-"), psg.Button("8", size=button_size, key="-8-"),
             psg.Button("9", size=button_size, key="-9-"), psg.Push()],
            [psg.Push(), psg.Button("6", size=button_size, key="-6-"), psg.Button("5", size=button_size, key="-5-"),
             psg.Button("4", size=button_size, key="-4-"), psg.Push()],
            [psg.Push(), psg.Button("3", size=button_size, key="-3-"), psg.Button("2", size=button_size, key="-2-"),
             psg.Button("1", size=button_size, key="-1-"), psg.Push()],
            [psg.Push(), psg.Button("DEL", size=button_size, key="-DEL-"),
             psg.Button("0", size=button_size, key="-0-"),
             psg.Button("ENT", size=button_size, key="-ENT-"), psg.Push()],
            [psg.VPush()]
        ], size=(160, 200))
        password_frame = psg.Frame("", [
            [psg.Text("S E C U L O C K", font=("Arial", 22), background_color="sky blue", text_color="azure",
                      visible=False if hacking else True)],
            [psg.VPush(background_color="sky blue")],
            [psg.Text("E N T E R   C O D E", font=("Arial", 22), background_color="sky blue", text_color="azure",
                      visible=False if hacking else True)],
            [psg.VPush(background_color="sky blue")],
            [psg.VPush(background_color="sky blue")],
            digits_text
        ], size=(400, 200), background_color="sky blue")
        output_frame = psg.Frame("", [
            [psg.VPush()],
            [],
            [psg.Text("  X  ", text_color="red", font=("Arial", 12, "bold")), psg.Text("Exit"), psg.Text("    "),
             psg.Text("  Z  ", text_color="green", font=("Arial", 12, "bold"), visible=False if hacking else True),
             psg.Text("Hacking", visible=False if hacking else True)]
        ], size=(300, 250), )
        layout = [
            [password_frame],
            [output_frame, digits_frame]
        ]
        window = psg.Window("Safe Hacking", layout, size=(500, 450), no_titlebar=True, return_keyboard_events=True,
                            finalize=True)
        # Disable cursor
        window.set_cursor("none")
        digits_frame.set_cursor("arrow")

        i = 0
        while True:
            event, values = window.read(timeout=100)
            if event == psg.WIN_CLOSED:
                break
            if event == "z" and hacking == False:
                hacking = True
                window.close()
            if event == "x":
                running = False
                window.close()
            if event in [f"-{j}-" for j in range(10)]:
                window[f"-DIGIT{i}-"].update(event.replace("-", ""))
                i += 1 if i < 3 else 0
            if event == "-DEL-":
                window[f"-DIGIT{i}-"].update("")
                i -= 1 if i > 0 else 0
            if event == "-ENT-":
                user_digits = list(values.values())
                if user_password_check(user_digits):
                    if hacking:
                        pass
                    else:
                        output_message = validity_check(digits, user_digits)
                        window.close()
                        psg.popup(output_message)
                        running = False

        window.close()


gui()
