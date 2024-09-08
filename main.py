import os
import subprocess
import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from scenarioData import get_data
from simulation import run_simulation


def format_excel_file(file_path):
    # Load the workbook and select the active sheet
    wb = load_workbook(file_path)
    ws = wb.active

    # Apply styles to the header (first row)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_alignment = Alignment(horizontal="right", vertical="center")

    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # Set the width of the first column to 45
    ws.column_dimensions['A'].width = 45

    ws['A1'].alignment = Alignment(horizontal="left", vertical="center")

    # Set the width of all other columns to 11 and apply number format #,###
    for col in range(2, ws.max_column + 1):
        col_letter = get_column_letter(col)  # Convert column number to column letter

        # Set the width of the column
        ws.column_dimensions[col_letter].width = 11

        # Apply the number format #,### to all cells in this column (starting from row 2)
        for row in range(2, ws.max_row + 1):
            cell = ws[f"{col_letter}{row}"]  # Access the specific cell
            cell.number_format = '#,###'


    # Make specific rows bold
    bold_rows = [2, 7, 12, 17, 22, 32, ]
    bold_font = Font(bold=True)
    for row in bold_rows:
        for cell in ws[row]:
            cell.font = bold_font

    total_rows = [26, 39]
    for row in total_rows:
        for cell in ws[row]:
            cell.font = header_font
            cell.fill = header_fill

    last_row = ws.max_row + 1
    ws[f'A{last_row}'] = 'Accumulated Gross Profit'
    ws[f'B{last_row}'] = ws[f'B{last_row - 1}'].value
    ws[f'B{last_row}'].number_format = '#,###'
    for col in range(3, ws.max_column + 1):
        col_letter = get_column_letter(col)
        prev_letter = get_column_letter(col - 1)
        ws[f'{col_letter}{last_row}'] = f'={prev_letter}{last_row} + {col_letter}{last_row-1}'
        ws[f'{col_letter}{last_row}'].number_format = '#,###'

    # Save the formatted Excel file
    wb.save(file_path)

def test():
    # Check if 'test.xlsx' exists in the repository and delete
    if os.path.exists('test.xlsx'):
        # Remove the file from the Git repository and stage the change
        subprocess.run(['git', 'rm', 'test.xlsx'], check=True)
        print('Deleted test.xlsx from the repository')

        # Commit the deletion
        commit_message = 'Remove existing test.xlsx before generating a new one'
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        # Push the deletion to the remote repository
        subprocess.run(['git', 'push'], check=True)

    # Get simulation data and run simulation
    data_dict = get_data()
    print(data_dict['scenarioName'])

    results = run_simulation(data_dict)

    df = pd.DataFrame(results, columns=[
        'month', 'customers', 'new customers', 'referred customers', 'lead customers',
        'existing customers', 'Risk assessment pakages sold', 'Risk assessment pakages sold to new customers',
        'Risk assessment pakages sold to referred customers', 'Risk assessment pakages sold to lead customers',
        'Risk assessment pakages sold to existing customers', 'SOC pakages sold',
        'SOC pakages sold to new customers', 'SOC pakages sold to referred customers',
        'SOC pakages sold to lead customers', 'SOC pakages sold to existing customers', 'Insurance packages sold',
        'Insurance packages sold to new customers', 'Insurance packages sold to referred customers',
        'Insurance packages sold to lead customers', 'Insurance packages sold to existing customers',
        'All packages sold', 'Income from risk assessment packages', 'Income from SOC packages', 'Income from insurance packages',
        'Total income', 'Admin staff', 'Tele staff', 'Sales staff', 'Cyber staff', 'Logistics staff',
        'Total staff', 'Labor cost', 'Risk assessment packages cost', 'SOC packages cost', 'Marketing cost',
        'General overhead', 'Legal & Accounting cost', 'Total cost', 'Gross profit',
    ])

    df = df.T
    df = df.reset_index()
    df.to_excel('test.xlsx', index=False, header=False)

    # Format Excl file
    format_excel_file('test.xlsx')

    # Save new excel file with simulation results
    # Add the Excel file to the Git staging area
    subprocess.run(['git', 'add', 'test.xlsx'], check=True)

    # Commit the Excel file with a message
    commit_message = 'Add Excel file generated by GitHub Actions workflow'
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

    # Push the changes back to the repository
    subprocess.run(['git', 'push'], check=True)

    # time.sleep(30)


if __name__ == '__main__':
    test()



