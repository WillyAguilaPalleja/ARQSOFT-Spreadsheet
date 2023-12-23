bold_start = "\033[1m"
bold_end = "\033[0m"

read_commands_from_a_file_command = f"{bold_start}RF{bold_end} <text file pathname>"
create_a_new_spreadsheet_command = f"{bold_start}C{bold_end}"
edit_a_cell_command = f"{bold_start}E{bold_end} <cell coordinate> <new cell content>"
load_a_spreadsheet_command = f"{bold_start}L{bold_end} <S2V file pathname>"
save_a_spreadsheet_command = f"{bold_start}S{bold_end} <S2V file pathname>"


help_message = (
    f"\n------------------------- HELP -------------------------\n"
    f"| Read commands from a file: {read_commands_from_a_file_command}   |\n"
    f"| Create a new spreadsheet: {create_a_new_spreadsheet_command}                          |\n"
    f"| Edit a cell: {edit_a_cell_command}  |\n"
    f"| Load a spreadsheet: {load_a_spreadsheet_command}            |\n"
    f"| Save a spreadsheet: {save_a_spreadsheet_command}            |\n"
    f"--------------------------------------------------------\n"
)
