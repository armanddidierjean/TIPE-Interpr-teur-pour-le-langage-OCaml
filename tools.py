class colors:
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    CYELLOW = '\33[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

LOG_INFO = False

def log(*arg):
    if LOG_INFO:
        print(*arg)

SHOW_INFO = False

def show(*arg):
    if SHOW_INFO:
        print(*arg)

SHOW_WARNING = True
def warning(*arg):
    if SHOW_WARNING:
        print(colors.WARNING, *arg, colors.ENDC)

def error(*arg):
    print(colors.FAIL, *arg, colors.ENDC)