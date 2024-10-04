import datetime
import importlib

##### (1) Get user inputs

    ### Get date input from the user
def get_date_input():
    while True:
        date_string = input("Enter a date (ddmmyyyy): ")
        if re.match(r'^\d{8}$', date_string):
            formatted_date = f"{date_string[4:8]}-{date_string[2:4]}-{date_string[0:2]}"
            return formatted_date
        else:
            print("Invalid format. Please enter the date in ddmmyyyy format.")


##### (2) Time and date functions

    ### timestamp
def get_timestamp():
   return datetime.now().strftime('%d/%m/%y %H:%M')


##### (3) Local file operations 

    ### Deleting files in a folder
def delete_files_in_folder(folder, keyword):
    """Delete files containing the specified keyword in the folder."""
    for filename in os.listdir(folder):
        if keyword in filename:
            file_path = os.path.join(folder, filename)
            os.remove(file_path)
            tstamp = get_timestamp()
            print(f"[{tstamp}] !Deleted {file_path}", flush=True)

  
##### (4) coloured print functions 

    ### print texts in green
def printproc(*args, **kwargs):
    print("\033[92m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")

    ### print texts in red
def printwarning(*args, **kwargs):
    print("\033[93m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")

    ### print texts in blue
def printsuccess(*args, **kwargs):
    print("\033[94m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")

    ### print texts in pink
def printerror(*args, **kwargs):
    print("\033[95m", end="")
    print(*args, **kwargs)
    print("\033[0m", end="")
    


##### (5) Run Modules/Functions
def run_module(module_name):
    try:
        # Dynamically import the module using the module name
        module = importlib.import_module(module_name)
        
        # Run the module if it contains a 'main' function
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"The module '{module_name}' does not have a 'main' function.")
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")
    except Exception as e:
        print(f"An error occurred while running the module '{module_name}': {e}")