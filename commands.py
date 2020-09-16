import os
from exceptions import Exit

def cd(path):
    """Change directory

    Args:
        path (string): path for new directory
    """
    # In case path is not supplied the current directory will be displayed to the console
    if path:
        try:
            os.chdir(path)
        except:
            print(f"Cannot find path '{path}'' because it does not exist.")
    else:
        print(os.getcwd())

def dir_cmd(path):
    """List all items of a given directory

    Args:
        path (string): path for directory to be listed
    """
    # In case path is not supplied the items of the current directory will be listed
    if path:
        try:
            print(*os.listdir(path), sep='\n')
        except:
            print(f"Cannot find path '{path}'' because it does not exist.")
    else:
        print(*os.listdir(), sep='\n')

def clear_screen():
    """Clear the console"""
    os.system('cls')

def exit_shell():
    """Exits the program

    Raises:
        Exception: Indicates an exit
    """
    raise Exit()
    