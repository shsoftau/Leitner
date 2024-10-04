import click
import sys
import subprocess
import os
import platform

from common_def_functions import *
from click_shell import shell
from config import *

# region - Shell & module functions
@shell(prompt=click.style("Leitner System> ", fg="bright_green"), intro=f"""\nWelcome to the Leitner SR system Type 'help' to see all available commands.
   """)

def Leitner():
    pass

# region - General Commands
@Leitner.command()
def help():
    """Display help message."""
    click.echo("""
    Here are the available commands:
    
    --- MAIN MENU ------------------------------------------------------------------------ 
    
    --- DATA AUDIT -----------------------------------------------------------------------
    
    --- SYSTEM MAINTENANCE ---------------------------------------------------------------    
    system --database : audit the database tables 
                          
    --- GENERAL COMMANDS -----------------------------------------------------------------
    help   : Display this help message
    cls    : Clear the terminal messages
    quit   : Exit the shell
    """)

@Leitner.command()
def cls():
    """Clear the terminal messages."""
    click.clear()

@Leitner.command()
def quit():
    """Exit the shell."""
    click.echo("Successfully logged out from football-api shell.")
    os._exit(0)


# region - SYSTEM Maintenance Commands
# region - SYSTEM Maintenance Commands
@Leitner.command()
@click.option('--database', is_flag=True, help="Audit Database Tables")
@click.option('--tbc', is_flag=True, help="Function Not Mapped Yet")
def system(database, tbc):
    """System Maintenance Functions"""
    if not any([database, tbc]):
        click.echo("Please specify an option: --database, --tbc")
        return
    if database:
        run_module('duckdb_audit_tables.py')
    if tbc:
        print("Function Not Mapped Yet")
    
# endregion


# region - Main loop
if __name__ == "__main__":
    Leitner()
# endregion
