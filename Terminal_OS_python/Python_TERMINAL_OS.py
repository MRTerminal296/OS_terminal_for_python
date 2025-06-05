import curses
import time
import random
import sys




def blinking_text(stdscr, text, y, x, times=5, delay=0.4, color_pair=0):
    for _ in range(times):
        stdscr.addstr(y, x, text, curses.color_pair(color_pair) | curses.A_BLINK)
        stdscr.refresh()
        time.sleep(delay)
        stdscr.addstr(y, x, ' ' * len(text))
        stdscr.refresh()
        time.sleep(delay)

def loading_bar(stdscr, y, x, length=30, delay=0.05, color_pair=0):
    h, w = stdscr.getmaxyx()

    bar_str = '[' + (' ' * length) + ']'
    if x + len(bar_str) >= w or y >= h:
        x = max(0, w // 2 - (length // 2) - 1)
        y = min(h - 1, y)

    stdscr.addstr(y, x, '[' + (' ' * length) + ']', curses.color_pair(color_pair))
    stdscr.refresh()
    for i in range(length):
        stdscr.addstr(y, x + 1 + i, '=', curses.color_pair(color_pair))
        stdscr.refresh()
        time.sleep(delay)
    finish_msg = "Initialization complete. Welcome!"
    stdscr.addstr(y + 4, max(0, (w - len(finish_msg)) // 2), finish_msg, curses.color_pair(2))
    stdscr.refresh()
    time.sleep(1.5)
    stdscr.clear()



def beep():
    # Try to beep - cross platform fallback
    try:
        print('\a', end='', flush=True)
    except:
        pass
def typewriter(stdscr, text, y, x, delay=0.05, color_pair=0):
    h, w = stdscr.getmaxyx()
    for i, ch in enumerate(text):
        if x + i >= w - 1:  # Prevent going out of width
            break
        if y >= h - 1:      # Prevent going out of height (just in case)
            break
        stdscr.addstr(y, x + i, ch, curses.color_pair(color_pair))
        stdscr.refresh()
        time.sleep(delay)

def boot_animation(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = "Booting TERMINAL OS v1.03..."
    y = h // 2
    x = max(0, (w - len(msg)) // 2)
    typewriter(stdscr, msg, y, x, delay=0.07, color_pair=1)
    time.sleep(0.5)
    loading_bar(stdscr, y + 2, max(0, (w // 2) - 15), 30, delay=0.03, color_pair=3)
    time.sleep(1)  # Let user see full bar
    stdscr.clear()  # ✅ Clear screen to continue
    stdscr.refresh()

def boot_menu(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    options = ["Normal Boot", "Safe Mode", "Diagnostics", "Secret Easter Egg"]
    current_idx = 0

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        title = "== TERMINAL OS v3.0 BOOT MENU =="
        stdscr.addstr(1, (w - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)

        for idx, option in enumerate(options):
            x = (w - len(option)) // 2
            y = h // 2 - len(options) // 2 + idx
            if idx == current_idx:
                stdscr.addstr(y, x, option, curses.color_pair(2) | curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, option, curses.color_pair(1))

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
        elif key == curses.KEY_DOWN and current_idx < len(options) - 1:
            current_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return current_idx

def secret_easter_egg(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    message = "?? Boom! You found the secret Easter Egg! ??"
    for i in range(5):
        stdscr.clear()
        color = curses.color_pair(random.choice([1,2,3]))
        stdscr.addstr(h//2, (w - len(message))//2, message, color | curses.A_BLINK | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.4)
    stdscr.addstr(h//2 + 2, (w - 25)//2, "Press any key to go back...", curses.color_pair(1))
    stdscr.getch()

def safe_mode(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = "Safe Mode activated. Limited functions available."
    stdscr.addstr(h//2, (w - len(msg))//2, msg, curses.color_pair(3))
    stdscr.addstr(h//2 + 2, (w - 26)//2, "Press any key to return to menu.")
    stdscr.refresh()
    stdscr.getch()

def diagnostics(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    messages = [
        "Running diagnostics...",
        "CPU: OK",
        "Memory: OK",
        "Disk: OK",
        "Network: OK",
        "All systems functional."
    ]
    y = h//2 - len(messages)//2
    x = (w - max(len(m) for m in messages))//2
    for msg in messages:
        stdscr.addstr(y, x, msg, curses.color_pair(2))
        stdscr.refresh()
        time.sleep(0.8)
        y += 1
    stdscr.addstr(y+1, (w - 24)//2, "Press any key to return to menu.")
    stdscr.getch()

def main_os_loop(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        title = "===TERMINAL OS v3.0 MAIN INTERFACE==="
        stdscr.addstr(1, (w - len(title))//2, title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, 5, "1. Writer")
        stdscr.addstr(4, 5, "2. Calculator")
        stdscr.addstr(5, 5, "3. Game Center")
        stdscr.addstr(6, 5, "4. Shutdown")
        stdscr.addstr(8, 5, "Select an option: ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('1'):
            writer(stdscr)
        elif key == ord('2'):
            calculator(stdscr)
        elif key == ord('3'):
            game_center(stdscr)
        elif key == ord('4'):
            shutdown_message(stdscr)
            break

def writer(stdscr):
    stdscr.clear()
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "📝 Writer - Type your text below. ESC to exit.", curses.color_pair(1) | curses.A_BOLD)
    text_lines = []
    y = 2
    x = 0
    while True:
        stdscr.move(y, x)
        stdscr.refresh()
        c = stdscr.get_wch()
        if c == '\x1b':  # ESC to exit
            break
        elif c == '\n':
            text_lines.append('')
            y += 1
            x = 0
        elif c == curses.KEY_BACKSPACE or c == '\b' or c == '\x7f':
            if x > 0:
                x -= 1
                stdscr.move(y, x)
                stdscr.delch()
                text_lines[-1] = text_lines[-1][:-1]
            elif y > 2:
                y -= 1
                x = len(text_lines[-2])
                text_lines.pop()
        else:
            if len(text_lines) == 0:
                text_lines.append('')
            text_lines[-1] += c
            stdscr.addstr(y, x, c)
            x += 1

def calculator(stdscr):
    stdscr.clear()
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "🧮 Calculator - Enter expression, ESC to exit.", curses.color_pair(1) | curses.A_BOLD)
    expr = ""
    y = 2
    x = 0
    while True:
        stdscr.move(y, x)
        stdscr.clrtoeol()
        stdscr.addstr(y, 0, expr)
        stdscr.refresh()
        c = stdscr.get_wch()
        if c == '\x1b':  # ESC
            break
        elif c == '\n':
            try:
                result = str(eval(expr, {"__builtins__": {}}, {}))
            except Exception as e:
                result = "Error"
            stdscr.addstr(y+1, 0, "Result: " + result + " " * (w - len(result) - 8))
            expr = ""
            y += 2
            x = 0
        elif c == curses.KEY_BACKSPACE or c == '\b' or c == '\x7f':
            expr = expr[:-1]
            x = max(0, x -1)
        else:
            expr += c
            x += 1

def game_center(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.addstr(2, 5, "🎮 Game Center")
    stdscr.addstr(4, 5, "1. Snake Game 🐍")
    stdscr.addstr(5, 5, "2. Back to Main Menu")
    stdscr.addstr(7, 5, "Choose option: ")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            snake_game(stdscr)
            break
        elif key == ord('2'):
            break

def snake_game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    for y in range(box[0][0], box[1][0]):
        stdscr.addstr(y, box[0][1], '|', curses.color_pair(3))
        stdscr.addstr(y, box[1][1], '|', curses.color_pair(3))
    for x in range(box[0][1], box[1][1]):
        stdscr.addstr(box[0][0], x, '-', curses.color_pair(3))
        stdscr.addstr(box[1][0], x, '-', curses.color_pair(3))

    snk = [[10,10], [10,9], [10,8]]
    food = [random.randint(5, sh-5), random.randint(5, sw-5)]
    stdscr.addstr(food[0], food[1], "O", curses.color_pair(4))
    key = curses.KEY_RIGHT

    while True:
        next_key = stdscr.getch()
        key = key if next_key == -1 else next_key
        head = snk[0]
        if key == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif key == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif key == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif key == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        else:
            continue
        snk.insert(0, new_head)
        if new_head == food:
            food = [random.randint(5, sh-5), random.randint(5, sw-5)]
            stdscr.addstr(food[0], food[1], "O", curses.color_pair(4))
        else:
            tail = snk.pop()
            stdscr.addstr(tail[0], tail[1], " ")
        if (new_head[0] in [box[0][0], box[1][0]] or
            new_head[1] in [box[0][1], box[1][1]] or
            new_head in snk[1:]):
            stdscr.addstr(sh//2, sw//2 - 5, "GAME OVER", curses.color_pair(3) | curses.A_BOLD)
            stdscr.nodelay(0)
            stdscr.getch()
            break
        stdscr.addstr(new_head[0], new_head[1], "#", curses.color_pair(4) | curses.A_BOLD)

def shutdown_message(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    msg = "Shutting down Terminal OS... Goodbye! 👋"
    for i in range(len(msg)):
        stdscr.addstr(h//2, (w - len(msg))//2 + i, msg[i], curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.05)
    time.sleep(1)

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.curs_set(0)

    boot_animation(stdscr)

    while True:
        choice = boot_menu(stdscr)
        if choice == 0:  # Normal Boot
            main_os_loop(stdscr)
        elif choice == 1:  # Safe Mode
            safe_mode(stdscr)
        elif choice == 2:  # Diagnostics
            diagnostics(stdscr)
        elif choice == 3:  # Easter Egg
            secret_easter_egg(stdscr)
        else:
            break

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nTerminal OS interrupted by user. Goodbye!")
