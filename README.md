
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
```

---

## Help

### Overview
This program is used to analyze logs and export results to Excel.

- **Time Plot**: Plots in an Excel file a graph of the distance for all devices.
- **Histogram**: Plots in an Excel file histograms of strings located in `settings.json`.
- **Case Sensitivity**: String search inside the log file is not case sensitive.

---

### Script Parameters

Run the script using the following syntax:
```bash
python LogAnalyzer.py <export_option> <video_real> <Input> <Output>
```

- `<export_option>` (Mandatory):
  - `0`: Histogram only.
  - `1`: Time plot only.
  - `2`: Both histogram and time plot.
- `<video_real>` (Mandatory):
  - `0`: Analyze the entire log file.
  - `1`: Analyze only after "video real" appears in the log.
- `<Input>` (Mandatory): Path to a folder containing files or a specific `.txt`/`.log` file to analyze.
- `<Output>` (Optional): Path to save the Excel files.
  - **Default Output Locations**:
    - If `<Input>` is a file: Excel file is saved in the same location as the input file.
    - If `<Input>` is a folder: An `ExcelResults` subfolder is created, and files are saved there.

---

### Script Rules

1. The `settings.json` file **must** be in the same directory as the `LogAnalyzer.py` script.
2. Paths for `<Input>` and `<Output>` must not contain spaces. For example:
   - `c:\MyFiles` is valid.
   - `c:\My Files` is not valid.
3. To handle spaces, enclose the path in quotation marks:
   - `"c:\My Files"` is valid.

---

### Examples

1. Save both time plot and histogram results of files inside `c:\yoni` to `c:\MyExcelResults`:
   ```bash
   python LogAnalyzer.py 2 0 c:\yoni c:\MyExcelResults
   ```
2. Save histogram results of files inside `c:\yoni` to the default folder (`c:\yoni\ExcelResults`), analyzing only after "video real":
   ```bash
   python LogAnalyzer.py 0 1 c:\yoni
   ```

---

## Notes

- Ensure `settings.json` is properly configured to match the log analysis requirements.
- Outputs are generated in `.xlsx` format and require a compatible Excel viewer.
