
# Log Analyzer

`LogAnalyzer.py` is a Python script designed to analyze log files and export results to Excel. The script provides features for creating histograms and time plots based on the log data, offering insights for debugging and analysis.

---

## Features

- **Time Plot**: Generates a graph of the distance for all devices in an Excel file.
- **Histogram**: Creates a graph of histograms for specific strings defined in `settings.json`.
- **Case Insensitive Search**: String search in logs is not case sensitive.
- **Customizable Output**: Save Excel files to a specified directory or default locations.

---

## Requirements

The script uses built-in Python modules except for:
- `pandas`
- `xlsxwriter`

Install the required modules with:
```bash
pip install pandas xlsxwriter

## Help

------------------------------------------Help-------------------------------------------------------------
This program is used to analyze logs and export results to Excel
Time Plot - will plot in an excel file a graph of the distance for all devices
Histogram - will plot in an excel file a graph of the histograms of strings located in settings.json file
Be aware - string search inside the log file is not case sensitive

------------------------------------------Modules----------------------------------------------------------
All modules that the program is using are built in except Pandas and Xlsxwriter.
The user must Install those modules before using the program.

------------------------------------------Script Parameters------------------------------------------------
python LogAnalyzer.py <export_option> <video_real> <Input> <Output>
<export_option> is mandatory! it can be 0,1,2: 0=histogram only, 1=TimePlot only, 2=Both
<video_real> is mandatory! it can be 0 or 1: 0=analyze all log, 1=analyze only after video real
<Input> is mandatory! it can be a folder containing files or a txt/log file we want to analyze
<Output> is optional! and it's the path user wants to save excel files at
If output is empty - then files are saved in default mode:
     If <Input> is a file then excel file is exported at the same location of this file 
     If <Input> is a folder then ExcelResults sub folder is created and excel files are saved inside

------------------------------------------Script rules-----------------------------------------------------
(1) setting.json file - MUST be at the same location of LogAnalyzer.py script file
(2) <Input> and <Output> must be without spaces -  for example:
    c:\MyFiles  ----> Is a valid parameter name
    c:\My Files ----> Is not a valid parameter name
In addition to handle this issue you need to add quotation marks to your path:
    "c:\My Files" ----> Now, is a valid parameter name

------------------------------------------Examples---------------------------------------------------------
(1) python LogAnalyzer.py 2 0 c:\yoni c:\MyExcelResults
    both TimePlot and Histogram results of files inside c:\yoni are saved in c:\MyExcelResults
(2) python LogAnalyzer.py 0 1 c:\yoni
    Histogram results of files inside c:\yoni are saved in c:\yoni\ExcelResults default folder
    1 - means log is analyzed only after video real appearance

