import os
import subprocess
from io import StringIO
from contextlib import redirect_stdout
from commands import exit_shell, clear_screen, cd, dir_cmd
from exceptions import UnknownCommand, NoneFound, Exit

def main():
    """The main function"""
    # Clear the screen before each execution
    os.system('cls')

    # Keep asking the user for commands
    while True:
        # Display the user's current location and ask for input
        current_directory = os.getcwd()
        command = input(f"{current_directory}>")

        # Try executing the user command, break the loop on case of a user exit (caught as an exception)
        try:
            evaluate(command)
        except Exit:
            break


def execute_command(command):
    """Execute a known command (cd, dir, exit or cls)

    Args:
        command (string): command-argument pair. E.g "cd path/to/file" or "dir"
    """
    if command.lower() == "exit":
        exit_shell()

    elif command.lower() == "cls":
        clear_screen()

    # The cd command can be written as one word when using cd.., cd\ or only cd
    elif command.lower().startswith(("cd ", "cd.", "cd\\")) or command.lower() == "cd":
        # Path starts from index 2 (after "cd")
        path = command[2:]
        cd(path.strip())

    # The dir command can be written as one word when using dir.., dir\ or only dir
    elif command.lower().startswith(("dir ", "dir.", "dir\\")) or command.lower() == "dir":
        # Path starts from index 3 (after "dir")
        path = command[3:]
        dir_cmd(path.strip())

    else:
        raise UnknownCommand()
            

def evaluate(command):
    """Evaluate a complex expression into an executable command. Used to handle piping and redirection.

    Args:
        command (string): command to be evaluated
    """

    # Remove Redundant spaces at the beggining and the end
    command = command.strip()

    # Handle piping
    if '|' in command:
        # Separate stdin and stdout
        operands = list(map(lambda op: op.strip(), command.split("|")))
        
        # Try piping the stdout of the first command as stdin for the second command
        try:
            # Capture the stdout
            stdout = StringIO()
            with redirect_stdout(stdout):
                execute_command(operands[0])

            # Pass the stdout as input
            process = subprocess.run(operands[1], shell=True, capture_output=True, text=True, input=stdout.getvalue())
            # Print the output of the second command if it's not None
            if process.returncode == 0:
                print(process.stdout)
            # Error code 1 means nothing was found in the "find" comand
            elif process.returncode == 1:
                raise NoneFound()
            # In case of an unknown command
            else:
                raise UnknownCommand()
        except Exception as err:
            print(str(err))

    # Handle redirection
    elif '>' in command:
        # Seprate the command and the file name
        operands = list(map(lambda op: op.strip(), command.split(">")))
        
        # Try redirecting the command stdout into the file specified
        try:
            with open(operands[1], 'w') as f:
                with redirect_stdout(f):
                    execute_command(operands[0])
        # In case of an unknown command
        except UnknownCommand as unknown_cmd:
            print(str(unknown_cmd))
            # Delete the redundant file that was created
            os.remove(operands[1])

    # Handle single commands
    else:
        try:
            execute_command(command)
        # In case of an unknown command
        except UnknownCommand as unknown_cmd:
            print(str(unknown_cmd))

if __name__ == "_main_":
    main()