import shutil
import os
# Get the terminal size as a named tuple
terminal_size = shutil.get_terminal_size()

# Access the columns and lines (width and height) of the terminal
columns = terminal_size.columns
lines = terminal_size.lines

print(f"Terminal size: {columns} columns x {lines} lines")
