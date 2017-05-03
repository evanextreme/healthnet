class bcolors:
    DEFAULT = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[36m'

def print_status(status,message):
    if status == 'GOOD':
        print(bcolors.DEFAULT + "[" + bcolors.OKGREEN + "GOOD" + bcolors.DEFAULT + "]", end=" ")
    elif status == 'FAIL':
        print(bcolors.DEFAULT + "[" + bcolors.FAIL + "FAIL" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'STATUS':
        print(bcolors.DEFAULT + "[" + bcolors.OKBLUE + "STATUS" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'USER':
        print(bcolors.DEFAULT + "[" + bcolors.OKBLUE + "USER" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'WARN':
        print(bcolors.DEFAULT + "[" + bcolors.WARNING + "WARN" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'HARDWARN':
        print(bcolors.DEFAULT + "[" + bcolors.FAIL + "WARN" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'DATA':
        print(bcolors.DEFAULT + "[" + bcolors.HEADER + "DATA" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'SERVER':
        print(bcolors.DEFAULT + "[" + bcolors.CYAN + "SERVER" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'USERFAIL':
        print(bcolors.DEFAULT + "[" + bcolors.WARNING + "USER" + bcolors.DEFAULT +"]", end=" ")
    if(message != None):
        print(message)
