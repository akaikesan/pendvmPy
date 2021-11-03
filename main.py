import sys
from machine import load_imem, step_processor
from pendvm import m
from commands import command

VERSION = 0.1

interactive = False
OPTION_DEBUG = "--debug"
OPTION_HELP  = "--help"

def main():

    args = sys.argv
    global progname
    progname = args[0]
    inp = parse_command_line(args)
    load_imem(inp)
    

    if (interactive):
        print("pendvm ",VERSION)
        loop()
        return
    else:
        result = step_processor(-1)
    
    return


# return input file path
def parse_command_line(args):
    if args[1] == "--debug":
        global interactive
        interactive = True

        return args[2]

    elif args[1] == OPTION_HELP:
        usage()
        sys.exit()

    else:
        return args[1]


def loop():
    buffer = ""
    oldbuffer = ""
    while(True):
        print("(pendvm)", end='')
        buffer = input()
        buffer.strip()

        if buffer == "":
            buffer = oldbuffer
        else:
            oldbuffer = buffer

        fields = buffer.split()
        func = None
        for c in command:
            if c.name == fields[0]:
                func = c.func
                break
            else:
                continue
        if func != None:
            func(fields)
        else:
            print("Invalid command. Type \"help\" for help.\n")

def usage():
    print("USAGE: pendvm <PRP-PAL-file>\n");
    print("OPTIONS:\n");
    print(" --radix r -- output using specified radix, which should be 10 or 16\n");
    print(" --debug -- use interactive debugging mode\n");
    print(" --version -- show detailed version information\n");
    print(" --help -- this message\n");
    sys.exit()

if __name__ == "__main__":
    main()