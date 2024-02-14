import os
import glob

# Get the current directory path
current_directory = os.path.dirname(__file__)

# Pattern to search for files starting with 'fn' and ending with '.py'
pattern = os.path.join(current_directory, 'fn*.py')

# Get the list of files that match the pattern
function_files = glob.glob(pattern)

# Dynamically import all functions from the files
for file in function_files:
    module_name = os.path.basename(file)[:-3]  # Remove the '.py' extension
    exec(f"from .{module_name} import *")