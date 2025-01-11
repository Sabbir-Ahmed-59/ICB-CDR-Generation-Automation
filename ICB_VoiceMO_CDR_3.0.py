import pandas as pd
from datetime import datetime, timedelta

# Folder to save the output file
output_folder = r"E:\RPA\ICB CDR Automation\Version 3.0"  # Update this path to your desired folder

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
200;426010624595160;918750280064;;;919999373074;;;;;;20240502112643;1;63;;;;;
201;1;;;719E;;;;;
202;358674081811950;
203;11;;;;;;;
206;20191227112643;1
300;D;Event: "MCCMNC","51","DATE-TIME.00",,,,,,,,,,,"88018750280064","CountryCode999373074","63",,"0","2","D","231060624595160","358674081811950","470021B70719E","8801801000038","TAPCODE","1","2G","1","DRE10","D31G06_M40MGW2","HTFLE613-2756.dat","23","1","","8801801000604",,
210;1;23;;;;;;;
226;
225;1001
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

# Function to update values based on Excel input and create a single output file
def update_values_from_excel(file_path):
    # Read the Excel file
    sheet1_df = pd.read_excel(file_path, sheet_name='Sheet1')  # Main values from Sheet1
    sheet2_df = pd.read_excel(file_path, sheet_name='Sheet2', dtype={
            'MCC': str, 'MNC': str, 'LocalCC': str, 'SatelliteCC': str, 'HomeCC': str, 'InternationalCC': str, 'TAPCODE': str
        })  # Contains MCC, MNC, LocalCC, SatelliteCC, HomeCC, InternationalCC, TAPCODE)

    # Initialize the final output with the header
    final_output = header

    # Iterate through each row of Sheet1 DataFrame
    for index, row in sheet1_df.iterrows():
        tapcode = str(row['TAPCODE'])
        date = row['DATE'].strftime("%Y/%m/%d")  # Format as DD/MM/YYYY
        base_time = row['TIME']  # Base time in HH-MM-SS format
        base_time = datetime.strptime(base_time, "%H-%M-%S") if isinstance(base_time, str) else base_time

        # Find the corresponding TAPCODE parameters from Sheet2
        corresponding_params = sheet2_df[sheet2_df['TAPCODE'] == tapcode]

        if not corresponding_params.empty:
            # Extract relevant parameters from the matched row in Sheet2
            mcc = str(corresponding_params['MCC'].values[0])
            mnc = str(corresponding_params['MNC'].values[0])
            local_cc = str(corresponding_params['LocalCC'].values[0])
            satellite_cc = str(corresponding_params['SatelliteCC'].values[0])
            home_cc = str(corresponding_params['HomeCC'].values[0])
            international_cc = str(corresponding_params['InternationalCC'].values[0])

            # List of country codes from Sheet2 corresponding to TAPCODE
            country_codes = [local_cc, satellite_cc, home_cc, international_cc]

            # Generate unique times for each of the 4 paragraphs within the row
            for para_num, country_code in enumerate(country_codes):
                # Increment time by para_num minutes to ensure unique times for each paragraph in the row
                unique_time = base_time + timedelta(minutes=para_num)
                time_str = unique_time.strftime("%H-%M-%S")

                # Replace variables in the middle template with row-specific values
                middle_section = middle_template.replace("MCC", mcc) \
                    .replace("MNC", mnc) \
                    .replace("MCCMNC", f"{mcc}{mnc}") \
                    .replace("DATE-TIME", f"{date}-{time_str}") \
                    .replace("CountryCode", country_code) \
                    .replace("TAPCODE", tapcode)

                # Append the modified middle section to the final output
                final_output += middle_section

    # Add the footer to the final output
    final_output += footer

    # Save the final output to a file
    output_path = r"E:\RPA\ICB CDR Automation\Version 3.0\RUI_MSC_VMSC51612.3532_20210410"
    with open(output_path, "w") as file:
        file.write(final_output)

    print(f"File saved as {output_path}")

# Main function to trigger file processing without GUI file selection
if __name__ == "__main__":
    # Hardcoded input Excel file path
    excel_file_path = r"E:\RPA\ICB CDR Automation\Version 3.0\input_data.xlsx"  # Update this path

    # Process the input Excel file and generate the output
    update_values_from_excel(excel_file_path)
