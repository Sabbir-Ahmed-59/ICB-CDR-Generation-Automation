import pandas as pd
from datetime import datetime
import os

# Folder to save the output file
output_folder = r"E:\RPA\ICB CDR Automation\Version 3.0"  # Update this path to your desired folder

# Input file path (hardcoded)
input_file_path = r"E:\RPA\ICB CDR Automation\Version 3.0\input_data.xlsx"  # Replace with your actual Excel file path

# Original text data with header and footer
header = """Geneva: text_data_transfer_file
Format: 1
Character_set: ASCII8
File_type: RUI_file
File_subtype: RUI_subtype
File_group_number: 1
File_in_group_number: 1
Total_files_in_group: 1
Source_ID: source
Tag: -v12
"""

middle_template = """
NR;MCC;MNC;470;02
200;505030624595160;8618845110270;;;88010086069;;;;;;20191227112806;1;0;;;;;
201;1;;;FB1A;;;;;
202;359458080795110;
203;22;;;;;;;
206;20191227112806;1
300;E;Event: "MCCMNC","53","DATE-TIME.00",,,,,,,,,,,"8618845110270","8110086069",,,"1","1","E","460023467513101","359458080795110","4700227D9FB1A","8801801000038","TAPCODE","1",,,"","","HTFLE613-2756.dat","","","","",,
210;;;;;;;;;
226;
225;"ROBI"
"""

footer = """
Footer: text_data_transfer_file
AuditValue_1: 0
AuditValue_2: 0
End: text_data_transfer_file
Lines: 1
Characters: 1
Checksum:
Security_checksum:
End_of_file:
"""

# Function to update values from the Excel file
def update_values_from_excel(file_path):
    try:
        # Load both sheets - sheet1 for TAPCODE, DATE, TIME; sheet2 for fixed parameters
        df_sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')  # Contains TAPCODE, DATE, TIME
        df_sheet2 = pd.read_excel(file_path,
                                  sheet_name='Sheet2', dtype={
            'MCC': str, 'MNC': str, 'LocalCC': str, 'SatelliteCC': str, 'HomeCC': str, 'InternationalCC': str, 'TAPCODE': str
        })  # Contains MCC, MNC, LocalCC, SatelliteCC, HomeCC, InternationalCC, TAPCODE)

        # Initialize the final output with the header
        final_output = header

        # Iterate through each row in sheet1 (TAPCODE, DATE, TIME)
        for index, row in df_sheet1.iterrows():
            tapcode = str(row['TAPCODE'])

            # Fetch fixed parameters from sheet2 based on TAPCODE
            matching_row = df_sheet2[df_sheet2['TAPCODE'] == tapcode]
            if matching_row.empty:
                raise ValueError(f"No matching row found for TAPCODE: {tapcode}")

            # Get fixed parameters
            mcc = matching_row['MCC'].values[0]
            mnc = matching_row['MNC'].values[0]
            local_cc = str(matching_row['LocalCC'].values[0])
            satellite_cc = str(matching_row['SatelliteCC'].values[0])
            home_cc = str(matching_row['HomeCC'].values[0])
            international_cc = str(matching_row['InternationalCC'].values[0])

            # Format date and time
            date = row['DATE'].strftime("%Y/%m/%d")
            time = row['TIME']
            time = time if isinstance(time, str) else time.strftime("%H-%M-%S")

            # Concatenate MCC and MNC to form MCCMNC
            mccmnc = mcc + mnc

            # Replace variables in the middle template
            middle_section = middle_template.replace("MCC", mcc) \
                .replace("MNC", mnc) \
                .replace("MCCMNC", mccmnc) \
                .replace("DATE-TIME", f"{date}-{time}") \
                .replace("TAPCODE", tapcode)

            # Append this middle section to the final output
            final_output += middle_section

        # Add the footer to the final output
        final_output += footer

        # Save the final output to a file
        output_path = output_folder + r"\RUI_MSC_VMSC5253.411_20210410"
        with open(output_path, "w") as file:
            file.write(final_output)

        print(f"File saved as {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Call the function with the hardcoded input file path
update_values_from_excel(input_file_path)
