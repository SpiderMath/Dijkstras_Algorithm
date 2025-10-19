import time
import os
import sys

class Style:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

def clear_screen():
    if os.name == 'nt': # Windows being not-Unix as usual :)
        os.system('cls')
    else: # Mac and Linux
        os.system('clear')


def loading_spinner(duration: int = 3):
    spinner_chars = ['|', '/', '-', '\\']

    print("\nProcessing your request...")

    start_time = time.time()
    while (time.time() - start_time) < duration:
        for char in spinner_chars:
            sys.stdout.write(f'\r{Style.YELLOW}{char}{Style.RESET} Please wait... ')
            sys.stdout.flush()
            time.sleep(0.1)

    sys.stdout.write('\r' + ' ' * 30 + '\r')
    print(f"{Style.GREEN}🥳Operation completed!{Style.RESET}")
    time.sleep(1.5)
