from colorama import Fore,Style,init
init()
    # I want to save time  ok im not weird
# this will return teh desired colorama color without pasting import colorama everywhere
def clr(color):

    if color == "R":
        return Fore.RED
    elif color == "G":
        return Fore.GREEN
    else:
        return Fore.YELLOW
#this will reset the color back to normal and prevent other  output form having the color.
def resetclr():
    return Style.RESET_ALL