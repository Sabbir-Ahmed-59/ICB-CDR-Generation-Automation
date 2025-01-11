# ICB-CDR-Generation-Automation
This Python code creates a Graphical User Interface (GUI) for running Python scripts associated with ICB CDR generation using the tkinter module. Follow the SOP file to understand setup and installation process. Here's a summary of its functionality:

# Core Features:
The GUI has buttons for running individual scripts (GPRS_CDR, SMSMO_CDR, VoiceMO_CDR, and VoiceMT_CDR).
A "Master" button allows running all scripts sequentially.
The subprocess module is used to execute scripts and handle any errors during their execution.

# Key Functions:
run_script(script_name): Runs the specified Python script and prints an error message if execution fails.
run_all_scripts(): Executes all predefined scripts (ICB_GPRS_CDR_3.0.py, ICB_SMSMO_CDR_3.0.py, ICB_VoiceMO_CDR_3.0.py, and ICB_VoiceMT_CDR_3.0.py) in sequence.

# GUI Design:
A main window with the title "ICB CDR Generation Script."
Individual buttons for each script with clear labels.
A bold "Master" button styled in red for executing all scripts simultaneously.
The layout is simple, with buttons spaced vertically.

# Usage:
Users can click on specific buttons to run individual scripts or the master button to run all scripts in one go.
The GUI ensures user-friendly control over script execution.
