from random import randint
import PySimpleGUI as psg


def generate_digits() -> list:
    # Function to generate digits in code
    digits = []
    while len(digits) < 4:
        d = randint(0, 9)
        # if d not in digits:
        digits.append(d)
    return digits


def generate_inequalities(digits: list) -> list:
    # Function to generate inequalities/equalities between digits
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
    # Function to check if digits in code as list are integers
    # and returns boolean corresponding to result
    for num in lista:
        try:
            int(num)
        except ValueError:
            return False
    return True


def validity_check(original: list, user: list) -> tuple:
    # Function to check validity with original code
    # returns result as string text in popup window
    i = 0
    while i < len(user):
        if original[i] != int(user[i]):
            return True, "It's a fail!"
        i += 1
    return False, "I'm in!"


def extended_validity_check(original: list, user: list) -> tuple:
    # Function to check validity with original code
    # except that it compares user digits with original
    # appends them to three lists which are returned
    # green - user digits are correct
    # yellow - user digits exist in code but on different places
    # red - user digits don't exist in code
    i = 0
    green = []
    yellow = []
    red = []
    while i < len(user):
        digit = int(user[i])
        if digit == original[i]:
            green.append(digit)
        else:
            if digit in original:
                yellow.append(digit)
            else:
                red.append(digit)
        i += 1
    return green, yellow, red


def gui():
    ## Main funtion displays program with graphical user interface
    # variable where are attempts, inequalities available with hacking mode
    # generated digits in code, variable program running and hacking mode as booleans
    attempts = 1
    digits = generate_digits()
    ineqs = generate_inequalities(digits)
    running = True
    hacking = False
    # Main program loop
    while running:
        # Theme in my program
        psg.theme("DarkTeal12")
        # Generate graphical line for places to write user digits, if hacking mode is True
        # then there are also inequality symbols
        # if not characters "-" replace them
        digits_text = [psg.Push(background_color="sky blue")]
        for i in range(0, 4):
            digits_text.append(psg.Input("*", justification="center", font=("Arial", 18, "bold"),
                                         size=3, border_width=0, key=f"-DIGIT{i}-", disabled=True,
                                         disabled_readonly_background_color="sky blue"))
            if i < 3:
                if hacking:
                    digits_text.append(psg.Text(f"{ineqs[i]}", justification="center", background_color="sky blue",
                                                font=("Arial", 13)))
                else:
                    digits_text.append(
                        psg.Text("-", justification="center", background_color="sky blue", font=("Arial", 13)))
        digits_text.append(psg.Push(background_color="sky blue"))
        # Button size nothing special
        button_size = (4, 2)
        # Frame for out digits to click, digits from keyboard are disabled
        # features to delete user digit and move to previous side and to enter user code
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
        # Frame for inscribed user digits, inequality symbols if hacking is True
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
        # Frame which are displayed attempts if hacking mode is True, keys for exit program
        # and for activate hacking mode
        output_frame = psg.Frame("", [
            [psg.VPush()],
            [psg.Text(f"Try {attempts}/4", font=("Arial", 12), visible=hacking, key="-ATTEMPTS-")],
            [psg.Text("  X  ", text_color="red", font=("Arial", 12, "bold")), psg.Text("Exit"), psg.Text("    "),
             psg.Text("  Z  ", text_color="green", font=("Arial", 12, "bold"), visible=False if hacking else True),
             psg.Text("Hacking", visible=False if hacking else True)]
        ], size=(300, 250), )
        # Window and its layout
        layout = [
            [password_frame],
            [output_frame, digits_frame]
        ]
        window = psg.Window("Safe Hacking", layout, size=(500, 450), no_titlebar=True, return_keyboard_events=True,
                            finalize=True)
        # Disable cursor except cursor in digits frame
        window.set_cursor("none")
        digits_frame.set_cursor("arrow")

        # Window loop, the variables i and j are for easy make digits keys
        # to effective communication
        i = 0
        while True:
            # Get an event and values from graphical window
            event, values = window.read(timeout=100)
            if event == psg.WIN_CLOSED:
                break
            # Operation for keyboard key 'z' - active hacking mode and refresh window
            if event == "z" and hacking is False:
                hacking = True
                window.close()
            # Operation for keyboard key 'x' - close program
            if event == "x":
                running = False
                window.close()
            # Operation for digits button - update input boxes for user digits
            if event in [f"-{j}-" for j in range(10)]:
                window[f"-DIGIT{i}-"].update(event.replace("-", ""))
                i += 1 if i < 3 else 0
            # Operation for delete button, explained above
            if event == "-DEL-":
                window[f"-DIGIT{i}-"].update("")
                i -= 1 if i > 0 else 0
            # Operation for enter button
            if event == "-ENT-":
                # Retrieve user digits and place them to the list
                user_digits = list(values.values())
                # Retrieve user digits and place them to the list
                # Execute function user_password_check, explained above
                if user_password_check(user_digits):
                    # Check a validity of codes in hacking mode, function returns three lists
                    if hacking:
                        # Loop checks in which list digit is and change his button text color
                        for digit in [f"{i}" for i in range(10)]:
                            if window[f"-{digit}-"].ButtonColor[0] not in ["red", "yellow"]:
                                window[f"-{digit}-"].update(
                                    button_color=("#fafafa", psg.theme_button_color_background()))
                        green, yellow, red = extended_validity_check(digits, user_digits)
                        # All digits are in green list, that's means all user digits are correct
                        # window is close, return message and close program
                        if len(green) == 4:
                            window.close()
                            psg.popup("I'm in!")
                            running = False
                        # Not all digits are correct
                        else:
                            # Loops check in which list digit is and change his button text color
                            for digit in green:
                                window[f"-{digit}-"].update(button_color=("green", psg.theme_button_color_background()))
                            for digit in yellow:
                                window[f"-{digit}-"].update(
                                    button_color=("yellow", psg.theme_button_color_background()))
                            for digit in red:
                                window[f"-{digit}-"].update(button_color=("red", psg.theme_button_color_background()))
                            # Increment an attempts value and update it on the window screen
                            attempts += 1
                            window["-ATTEMPTS-"].update(f"Try {attempts}/4")
                        # Program checks if value attempts are equal to 4 and close itself previously returns failure message
                        if attempts > 4:
                            window.close()
                            psg.popup("It's a fail!")
                            running = False
                    # Check a validity of codes in non-hacking mode, function returns message displayed on
                    # the graphical popup window and close program
                    else:
                        running, output_message = validity_check(digits, user_digits)
                        if running is False:
                            window.close()
                        psg.popup(output_message)

        window.close()


# Execute program
gui()
