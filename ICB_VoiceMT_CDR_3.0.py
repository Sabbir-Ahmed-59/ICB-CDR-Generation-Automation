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
214;432110497127011;919831699410;;;917063163936;;;;20221025193559;1;32;;
201;1;;;4E9F;;;;;
202;869581058927490;
203;11;;;;;;;
206;20210210193559;1
300;D;Event: "MCCMNC","52","DATE-TIME.00",,,,,,,,,,,"917063163936","919831699410","32",,"0","2","D","404310497127011","869581058927490","4700227464E9F","919831029512","TAPCODE","1","3G","1","BD2G06_M29MGW1","CRE23","HTFLE824-4651.dat","","","","",,
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
        })  # Contains MCC, MNC, LocalCC, SatelliteCC, HomeCC, InternationalCC, TAPCODE)  # Contains MCC, MNC, LocalCC, SatelliteCC, HomeCC, InternationalCC, TAPCODE)

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
                .replace("MCCMNC", f"{mcc}{mnc}") \
                .replace("DATE-TIME", f"{date}-{time}") \
                .replace("TAPCODE", tapcode)

            # Append this middle section to the final output
            final_output += middle_section

        # Add the footer to the final output
        final_output += footer

        # Use os.path.join for consistent file path handling
        output_path = output_folder + r"\RUI_MSC_VMSC824.1550_20210210193934"

        # Save the file
        with open(output_path, "w") as file:
            file.write(final_output)

        print(f"File saved as {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Call the function with the hardcoded input file path
update_values_from_excel(input_file_path)
