class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\33[33m'
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

SHOW_WARNING = False

def warning(*arg):
    if SHOW_WARNING:
        print(colors.WARNING, *arg, colors.ENDC)

def error(*arg):
    errorsManager.extend(arg)
    print(colors.FAIL, *arg, colors.ENDC, sep='\n')

# Errors are pushed to the pile so they can be listed by the tests command
class ErrorsManager():
    def __init__(self):
        self.errorsPile = []
    def empty(self):
        self.errorsPile = []
    def extend(self, list):
        self.errorsPile.extend(list)
    def get(self):
        return self.errorsPile
    
    def warning(self, arg):
        if SHOW_WARNING:
            print(colors.WARNING, arg, colors.ENDC)
    
    def error(self, arg):
        errorsManager.extend(arg)
        print(colors.FAIL, arg, colors.ENDC)

    def SyntaxError(self, message):
        self.error(message)
    
    def MemoryError(self, message):
        self.error(message)
    
    def TypeError(self, message):
        self.error(message)
    
    def TypeWarning(self, message):
        self.warning(message)

    def Exception(self, message):
        self.error(message)
    
errorsManager = ErrorsManager()