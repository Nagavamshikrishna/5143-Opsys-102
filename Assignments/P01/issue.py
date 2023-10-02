"""
This file is starting file of our shell. It will have following features
 - using getch capture input and handle certain keys when they are pushed.
 - flgas and params handle
 - Piping handle 
 - Output redirection handle 
 - maintain history of command 
"""

import sys
from time import sleep
import re
from  getch_helper import Getch
from command_helper import CommandHelper
from history import add_to_history
from whoami import prompt
import os

#todo
#resize and check the output and make resize
#import module path ask ??

command_history=[] # To collect command 
getch = Getch()   # create instance of our getch class


def print_cmd(cmd):
    """ This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    terminal_width, _ = os.get_terminal_size()
    prompt_str = prompt()
    
    # Calculate the maximum width available for the command
    max_cmd_width = terminal_width - len(prompt_str) - 2  # Reserve 2 characters for padding
    
    # Check if the command is longer than the available width
    if len(cmd) > max_cmd_width:
        # Adjust the prompt width to accommodate the long command
        prompt_str = prompt_str[:max_cmd_width - len(cmd) - 3] + "...$:"  # Truncate and add ellipsis
    
    padding = " " * (terminal_width - len(prompt_str) - len(cmd) - 1)
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt_str + cmd)
    sys.stdout.flush()


#check cat a.txt b.txt >c.txt
# check cat b.txt >n.txt> m.txt : not support 
def save_output_to_file(output, output_file):
    ''' This method will save content (output) on the required files 

    - **Params:**
      - output: content
      - output_file: file_name
    
    - **Returns:**
      - (None
    '''
    print("\r")
    try:
        # Save the captured output to the specified file
        file_name=output_file.strip()
        #file_name = os.path.basename(output_file) if  "/"in output_file else output_file

        # Check if the file_name starts with a '>' followed by any character other than a hyphen

        if re.match(r'^>[^-]', file_name):
          mode = 'a'  
          file_name=file_name.rsplit(">", 1)[-1].strip() # Extract the actual file name by splitting at the last '>'

        else :
           mode='w'

        with open(file_name, mode) as file:
              file.write(output)
    except Exception as e:
        print(f"Error: {e}")


# input redirection : as discussion with professor .. no need to do 
# wc -l tu.txt     wc -l <tu.txt
# grep test  tu.txt grep test  <tu.txt




if __name__ == '__main__':

    ch = CommandHelper()

    cmd_text = ""        # empty cmd variable

    print_cmd(cmd_text)     # print to terminal
    
    while True:       # loop forever

        char = getch()   # read a character (but don't print)

        if char == '\x03' or cmd_text == 'exit': # ctrl-c
            raise SystemExit(" Bye.")
        
        elif char == '\x7f':    # back space pressed
           # print(" "+cmd_text)    
                    
            cmd_text = cmd_text[:-1]
            print("\b \b", end='')  # Move the cursor back and erase the character
            print_cmd(cmd_text)
        
        
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd_text += u"\u2191"
                print_cmd(cmd_text)
                sleep(0.3)
                #cmd = cmd[:-1]
                
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd_text += u"\u2193"
                print_cmd(cmd_text)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            if direction in 'C':            # right arrow pressed    
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd_text += u"\u2192"
                print_cmd(cmd_text)
                sleep(0.3)
                #cmd = cmd[:-1]

            if direction in 'D':            # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd_text += u"\u2190"
                print_cmd(cmd_text)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            print_cmd(cmd_text)                  # print the command (again)

        elif char in '\r':                  # return pressed 
            
            left_value, redirect_value = cmd_text.split('>', 1) if '>' in cmd_text else (cmd_text, '') #max pslit will be 1 that two parts 
            commands=left_value.split("|")
            captured_output=""
            if len(commands)>1 and commands[0].split()[0].strip()=="ls": # handle formated print of ls
                captured_output="ls"
            for comnnad in commands:
                # Split the command using spaces outside of quotes
                parts = re.findall(r'[^"\s\']+|"[^"]*"|\'[^\']*\'', comnnad)
                # The first part is the command itself
                cmd = parts[0].strip() if parts else ""
                
                #ch.add_to_history(command)  # Add executed command to history
                                

                # collect parameters and flags
                params = [part.strip() for part in parts[1:] if not part.startswith('-')]
                flags = [part.lstrip("-").strip() for part in parts[1:] if re.match(r'^-[^\-]', part)]
                helps = [part.lstrip("-").strip() for part in parts[1:] if re.match(r'^--[^-]', part)]
                
                add_to_history(comnnad, flags)
           

            # if command exists in our shell
                if ch.exists(cmd):
                    if helps:
                       captured_output= ch.invoke(cmd=cmd, params=params,flags=''.join(flags),input=captured_output,help=''.join(helps))
                    else:
                        captured_output= ch.invoke(cmd=cmd, params=params,flags=''.join(flags),input=captured_output)

                else:
                    print("\r")
                    print("Error: command %s doesn't exist." % (cmd))   


            if redirect_value:
                save_output_to_file(captured_output,redirect_value)  
            else:
                print("\r")
                print(captured_output)                  
            
            sleep(1)    
            cmd_text = ""                        # reset command to nothing (since we just executed it)

            print_cmd(cmd_text)   
                           # now print empty cmd prompt
        elif char == ':':
            char = getch()  # Read the next character
            if char.isdigit():
                history_index = int(char)
                while char.isdigit():
                    char = getch()
                    if char.isdigit():
                        history_index = history_index * 10 + int(char)
                    else:
                        break
                if history_index >= 0 and history_index <= len(command_history):
                    selected_command = command_history[history_index - 1]
                    print_cmd(selected_command)
                    cmd_text = selected_command
                else:
                    print("Invalid history index.")
            else:
                print("Invalid history command format.")
        else:
            cmd_text += char  # add typed character to our "cmd"
            print_cmd(cmd_text)                  # print the cmd out