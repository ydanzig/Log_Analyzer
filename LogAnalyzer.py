###################################################Importing Modules###################################################
#Importing modules. If pandas/xlsxwriter is not installed a massage to the user will appear
import os
import sys
import json
import datetime
try:
    import pandas as pd
except:
    print("Please install pandas module manually")
    sys.exit()
try:
    import xlsxwriter
except:
    print("Please install xlsxwriter module manually")
    sys.exit()
###################################################Global variables####################################################
DEFAULT_KEYS = []
USER_KEYS = []
###################################################Internal Functions##################################################
# Function takes a list and lows the letters inside.
LowList = lambda L1: [x.lower() for x in L1]

# Function takes 2 lists and uniun them to a lowed letter new list.
ListCombine = lambda L1, L2: list(set(LowList(L1) + LowList(L2)))  # set removes duplicated values


# Function creates a folder if it does not exist on a given path (skipping existing folder)
def FolderCreate(FolderPath):
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath)


# Function takes the configuration json settings file and convert it to a dictionary file format
def JSON2dict(SettingFilePath):
    JsonFile = open(SettingFilePath, mode='r')
    try:
        return json.load(JsonFile)
    finally:
        JsonFile.close()

# Function takes strings from settings file and return a dictionary appearance of those strings in the log file
def StringCount(LogFilePath, VideoRealStart = False):
    # Preparing list of words to search                   #KeysList = keys/words we want to search in file
    KeysList = ListCombine(DEFAULT_KEYS, USER_KEYS)       # Combinatrion of default&user keys
    counter = {word: 0 for word in KeysList}              # Init counter - {word1:0,word2:0...wordn:0}
    LogFile = open(LogFilePath, mode="r")                 # loading our log file to a variable
    try:  # Count process
        VideoRealFound = False if VideoRealStart else True  # VideoRealFound initiation.
        for line in LogFile:
            for word in KeysList:
                if (VideoRealFound == False):
                    if ("video real" in (line.lower()).decode("ascii","ignore")):
                        VideoRealFound = True
                if (word in (line.lower()).decode("ascii","ignore")) and (VideoRealFound == True):  # word is in line. decode to ignore non ascii strings.
                    counter[word] += 1  # multiply apperance of string in one line will count like one appeance
        if VideoRealStart and not(VideoRealFound):
            print("No video real string was found in",LogFilePath.split("\\")[-1])
        return {LogFile.name.split("\\")[-1]: counter}  # return result as a dictinary of {filename: {counter dict}}
    finally:
        LogFile.close()

# Function returns dictionary type containing word apperance inside all log/text files inside a spesific folder
def FolderStringCount(LogFolderPath, VideoRealStart = False):
    DictTemp = {}  # Containder of dict results
    for file in os.listdir(LogFolderPath):  # going over the files inside LogFolderPath parameter
        if ".log" in file.lower() or ".txt" in file.lower():  # Running only over valid files
            LogFilePath = os.path.join(LogFolderPath, file)
            Result = StringCount(LogFilePath, VideoRealStart)
            DictTemp[file] = Result[file]  # collecting all results in DictTemp
    #      else:
    #           print("File: ",file," has extention that is not suppotred")
    return DictTemp  # return result as a dictinary of {file1: {counter1},file2: {counter2},..}

#Internal function to add a text box when there is no data
def EmptyTabCreate(writer,sheet_name,location,TextBox):
    workbook = writer.book
    worksheet = workbook.add_worksheet(sheet_name)
    options = {
    'width': 2*256,
    'height': 2*100,
    'x_offset': 10,
    'y_offset': 10,

    'font': {'color': 'red',
    'size': 14},
    'align': {'vertical': 'middle',
    'horizontal': 'center'
                                  },
    'gradient': {'colors': ['#DDEBCF',
    '#9CB86E',
    '#156B13']},                }
    worksheet.insert_textbox(location, TextBox, options)

#Function export an excel file containing time plot results for every file in a different tab.
#Link input can be a folder of a single file
def TimePlotExcelExport(Link, SavingPath, VideoRealStart = False):
    filename = datetime.datetime.now().strftime("TimePlotFolderResults_from_%d-%m-%Y@%H-%M-%S.xlsx") #filename with time stamp
    fullpath = os.path.join(SavingPath,filename)         #full saving path with time stamp
    writer = pd.ExcelWriter(fullpath)                    #Create a Pandas Excel writer using XlsxWriter as the engine.
    FileList = []
    if os.path.isfile(Link):
        FileList.append(Link.split("\\")[-1])
    else:
        FileList = os.listdir(Link)                      #FileList has a list name of single file or files inside given folder
    for file in FileList:
        if ".log" in file.lower() or ".txt" in file.lower(): #Running only over valid files
            sheet_name = file[:31]                           #Sheet name is filename
            LogFilePath = Link if (os.path.isfile(Link)) else os.path.join(Link,file)
            if not(TimePlot(LogFilePath, VideoRealStart).empty):             #Adding tabs only if TimePlot function return is not empty
                df = TimePlot(LogFilePath, VideoRealStart)
                df.to_excel(writer, sheet_name=sheet_name)   #Convert the dataframe to an XlsxWriter Excel object.
                # Access the XlsxWriter workbook and worksheet objects from the dataframe.
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                # Create a chart object.
                chart = workbook.add_chart({'type': 'line'})
                # Add a series to the chart.
                # [sheetname, first_row, first_col, last_row, last_col]
                row_end, col_end = df.shape[0], df.shape[1]
                #adding statistics to excel tab
                stat = df.describe()
                stat.index.name = "Statistic Info"          #Adding title to desctibe info
                stat.to_excel(writer, sheet_name=sheet_name, startcol=col_end+2)
                # Configure the series of the chart from the dataframe data.
                for col_num in range(1, col_end + 1):
                    chart.add_series({
                        'name':       [sheet_name, 0, col_num],
                        'categories': [sheet_name, 1, 0, row_end, 0],
                        'values':     [sheet_name, 1, col_num, row_end, col_num],
                        'marker':     {'type': 'circle', 'size': 6},
                        #'line':       {'none': True},       #Hidding graph line
                        'line':       {'width' : 0.25, 'transparency': 25},
                    })
                #Configure the chart axes.
                interval_units = 13 if (row_end > 13) else 1
                chart.set_x_axis({'name': 'Time','interval_unit': interval_units,'num_font': {'rotation': -45}})
                chart.set_y_axis({'name': 'Distance[m]'})
                #Plotting total time in chart title
                start_time = datetime.datetime.strptime(df.index[0], '%H:%M:%S')
                end_time = datetime.datetime.strptime(df.index[len(df.index)-1], '%H:%M:%S')
                if (end_time > start_time):
                    delta = (end_time - start_time)
                elif (end_time < start_time):
                    delta = (end_time - start_time) + datetime.timedelta(days=1)
                else:
                    delta = ""                     #Only one value
                chart.set_title({'name':"".join(["Total Time: ",str(delta)])})
                chart.show_blanks_as('span')                   #Blanks cells are showen as a span... nice!! :)
                # Insert the chart into the worksheet.
                worksheet.insert_chart('I1', chart)
            else:
                #When no "set distance" found in file - Create an empty tab with a message to the user
                message = "No set distance results - Excel tab is empty"
                EmptyTabCreate(writer,sheet_name,location = 'B2',TextBox = message)
    writer.save()    # Close the Pandas Excel writer and output the Excel file.
    print("Export completed at ", fullpath)

#Function takes the dictinary type STRING COUNT results and export them to excel.
#Function can show full table or only the foundings (FoundOnly flag)
def StringHistogramExport(DictResults, SavingPath, FoundOnly = True):
    df = pd.DataFrame.from_dict(DictResults)              #converting the dict to data frame type
    if FoundOnly:
        df = df.loc[(df!=0).any(axis=1)]     #Removing all rows that are fulled with zero results
    filename = datetime.datetime.now().strftime("StringCountResults_from_%d-%m-%Y@%H-%M-%S.xlsx") #filename with time stamp
    fullpath = os.path.join(SavingPath,filename)                                      #full saving path with time stamp
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter') # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Results'
    if not(df.empty):                                      # Adding tabs only if histogram has results
        df.to_excel(writer, sheet_name=sheet_name) # Convert the dataframe to an XlsxWriter Excel object.
        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]
        # Create a chart object.
        chart = workbook.add_chart({'type': 'column'})
        # Add a series to the chart.
        # [sheetname, first_row, first_col, last_row, last_col]
        row_end, col_end = df.shape[0], df.shape[1]
        # Configure the series of the chart from the dataframe data.
        for col_num in range(1, col_end + 1):
            chart.add_series({
                'name':       [sheet_name, 0, col_num],
                'categories': [sheet_name, 1, 0, row_end, 0],
                'values':     [sheet_name, 1, col_num, row_end, col_num],
                'data_labels': {'value': True},       #Adding data labels.
            })
        chart.set_x_axis({'major_gridlines': {'visible': True}})
        chart.set_table({'show_keys':  True})                #Adding data table in the buttom of graph.
        chart.set_legend({'none': True})                     #No need for legend - show_keys=True.
        #chart.set_style(5)                                  #Changing table style
        # Insert the chart into the worksheet.
        worksheet.insert_chart('I1', chart)
    else:
        #When no histogram results were found in file - Create an empty tab with a message to the user
        files_checked = ", ".join(df.columns.tolist())
        message = "".join(["No histogram results were found in files ",files_checked," Excel tab is empty"])
        EmptyTabCreate(writer,sheet_name,location = 'B2',TextBox = message)
    writer.save()   # Close the Pandas Excel writer and output the Excel file.
    print("Export completed at ", fullpath)

#Function returns a dataframe containing distance values for each ANA inside log.
def TimePlot(LogFilePath,   VideoRealStart = False):
    # internal functions to "cut" time,Ana1-4 and Distance information
    Time = lambda Line: Line[Line.find("\t") + 1:Line.find("\t") + 9]  # Cutting time function
    Ana = lambda Line: Line[Line.find("ANA"):Line.find("ANA") + 5]  # Cutting ANA 1/ANA 2/ANA 3/ANA 4
    Distance = lambda Line: Line[Line.find("distance") + 9:Line.find("[m]")]  # Cutting the distance in [m]
    LogFile = open(LogFilePath, mode="r")  # Loading log file to a variable

    df = pd.DataFrame()  # Creating the dataframe
    df.index.name = "Time"
    VideoRealFound = False if VideoRealStart else True                        # VideoRealFound initiation.
    try:
        for line in LogFile:
            if (VideoRealFound == False):
                if ("video real" in (line.lower()).decode("ascii","ignore")):
                    VideoRealFound = True
            if ("set distance" in line.lower()) and (VideoRealFound == True):
                df.at[Time(line), Ana(line)] = float(Distance(line))  # Updating every row
        if VideoRealStart and not(VideoRealFound):
            print("No video real string was found in",LogFilePath.split("\\")[-1])
        return (df)
    finally:
        LogFile.close()

# Function return user keys and default keys from json file
def GetKeys(SettingFilePath):
    SettingFilePath = os.path.join(SettingFilePath)
    JsonFile = JSON2dict(SettingFilePath)  # Loading keys from json file.
    return (JsonFile['DefaultKeys'], JsonFile['UserKeys'])  # List of default keys

#Help Function
def help():
    print("------------------------------------------Help-------------------------------------------------------------")
    print("This program is used to analyze logs and export results to Excel")
    print("Time Plot - will plot in an excel file a graph of the distance for all devices")
    print("Histogram - will plot in an excel file a graph of the histograms of strings located in settings.json file")
    print("Be aware - string search inside the log file is not case sensitive")
    print("")
    print("------------------------------------------Modules----------------------------------------------------------")
    print("All modules that the program is using are built in except Pandas and Xlsxwriter.")
    print("The user must Install those modules before using the program.")
    print("------------------------------------------Script Parameters------------------------------------------------")
    print("python LogAnalyzer.py <export_option> <video_real> <Input> <Output>")
    print("<export_option> is mandatory! it can be 0,1,2: 0=histogram only, 1=TimePlot only, 2=Both")
    print("<video_real> is mandatory! it can be 0 or 1: 0=analyze all log, 1=analyze only after video real")
    print("<Input> is mandatory! it can be a folder containing files or a txt/log file we want to analyze")
    print("<Output> is optional! and it's the path user want's to save excel files at")
    print("If output is empty - then files are saved in default mode:")
    print("     If <Input> is a file then excel file is exported at the same location of this file ")
    print("     If <Input> is a folder then ExcelResults sub folder is created and excel files are saved inside")
    print("")
    print("------------------------------------------Script rules-----------------------------------------------------")
    print("(1) setting.json file - MUST be at the same location of LogAnalyzer.py script file")
    print("(2) <Input> and <Output> must be without spaces -  for example:" )
    print("    c:\MyFiles  ----> Is a valid parameter name")
    print("    c:\My Files ----> Is not a valid parameter name")
    print("In addition to handle this issue you need to add quotation marks to your path:")
    print("    \"c:\My Files\" ----> Now, is a valid parameter name")
    print("")
    print("------------------------------------------Examples---------------------------------------------------------")
    print("(1) python LogAnalyzer.py 2 0 c:\yoni c:\MyExcelResults")
    print("    both TimePlot and Histogram results of files inside c:\yoni are saved in c:\MyExcelResults")
    print("(2) python LogAnalyzer.py 0 1 c:\yoni")
    print("    Histogram results of files inside c:\yoni are saved in c:\yoni\ExcelResults default folder")
    print("    1 - means log is analyzed only after video real appearance")
########################################################Main function##################################################
def main():
    # Lodaing user keys and default keys from settings.json file
    Script_Path = os.path.dirname(os.path.abspath(__file__))  # running script path
    SettingFile = os.path.join(Script_Path, "settings.json")  # json link
    if not (os.path.isfile(SettingFile)):
        help()
        sys.exit()
    global DEFAULT_KEYS, USER_KEYS
    DEFAULT_KEYS, USER_KEYS = GetKeys(SettingFile)
    #############################################User Parameters handle section#########################################
    # Export user option argument to boolean variable
    export_option = sys.argv[1]  # Export option = 0-StringCount ,1- TimePlot, 2-Both
    if export_option == "0":
        TimePlotEnable, StringCountEnable = False, True  # Only StringCount is enabled
    elif export_option == "1":
        TimePlotEnable, StringCountEnable = True, False  # Only TimePlot is enabled
    elif export_option == "2":
        TimePlotEnable, StringCountEnable = True, True  # TimePlot and StringCount are enabled
    elif export_option == 'help':
        help()
        sys.exit()
    else:
        help()
        sys.exit()

    #VideoRealStart parameter handeling
    VideoRealParam = sys.argv[2]
    if VideoRealParam == "0":
        VideoRealStart = False
    elif VideoRealParam == "1":
        VideoRealStart = True
    else:
        help()
        sys.exit()

    #Input parameter handeling
    link = os.path.abspath(sys.argv[3])                 # Second Argument: input - file/folder, to be analyze
    #Output parameter handeling
    if len(sys.argv) == 5:                              # User declare his own export folder
        UserExportFolder = sys.argv[4]                  # Export folder is as user declaration
        FolderCreate(UserExportFolder)                  # creating the folder, for future file export, if not existed
    elif len(sys.argv) == 4:                            # User did not declare an export folder
        UserExportFolder = "default"

    # input file validation
    if (os.path.isfile(link) and (not (".log" in link.lower()) and not (".txt" in link.lower()))):
        help()
        sys.exit()

    # Saving path handeling section
    SavingPath = UserExportFolder  # We assume path is a user declaration
    if os.path.isfile(link):  # File is the input
        if UserExportFolder == "default":
            SavingPath = os.path.dirname(link)
    else:  # Folder is the Input
        if (UserExportFolder == "default"):
            FolderCreate(os.path.join(link, "ExcelResults"))
            SavingPath = os.path.join(link, "ExcelResults")

#Excel Exporting section
    if StringCountEnable:  # StringCountEnable = True
        print("Exporting Histogram...")
        if os.path.isfile(link):  # File is the input
            DictResults = StringCount(link, VideoRealStart)
        else:                     # Folder is the input
            DictResults = FolderStringCount(link, VideoRealStart)
        StringHistogramExport(DictResults, SavingPath=SavingPath)
    if TimePlotEnable:           # TimePlotEnable = True
        print("Exporting TimePlot...")
        TimePlotExcelExport(link, SavingPath, VideoRealStart)

if __name__ == "__main__":
    main()