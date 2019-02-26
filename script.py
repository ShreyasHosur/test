
from configparser import ConfigParser
import os
import logging
import csv
import pandas as pd

parser = ConfigParser()
parser.read('properties.config')
logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]-->%(message)s')
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def CsvConvert(Record,filename):
    global HeaderDone
    if Header and not HeaderDone:
        Record1 = Record.copy()
        HeaderDone=True
        Headfilename=filepath+'//Header'
        if not os.path.exists(Headfilename):
            os.mkdir(Headfilename)
        Record1.pop(0)
        HeadFilenamecsv=Headfilename+'//NoHeader.csv'
        with open(HeadFilenamecsv, 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=separator)
            writer.writerows(Record1)
        csvFile.close()

    global TrailerDone
    if Trailer and not TrailerDone:
        Record1 = Record.copy()
        TrailerDone=True
        TrailerfileName=filepath+'//Trailer'
        if not os.path.exists(TrailerfileName):
            os.mkdir(TrailerfileName)
        TrailerFilenamecsv=TrailerfileName + '//NoTrailer.csv'
        Record1.pop(-1)
        with open(TrailerFilenamecsv, 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=separator)
            writer.writerows(Record1)
        csvFile.close()

    filename1=filename+'.csv'
    with open(filename1, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=separator)
        writer.writerows(Record)
    csvFile.close()

def FileConvert(FileRecord,filename):
    global HeaderDone
    if Header and not HeaderDone:
        Record1 = FileRecord.copy()
        Headfilename=filepath+'//Header'
        HeaderDone=True
        if not os.path.exists(Headfilename):
            os.mkdir(Headfilename)
        HeadFilename1 = Headfilename + '//NoHeader'
        Record1.pop(0)
        writefile = open(HeadFilename1, 'w+')
        for subrecord in Record1:
            writefile.write(str(subrecord))
        writefile.close()

    global TrailerDone
    if Trailer and not TrailerDone:
        Record1=FileRecord.copy()
        TrailerDone = True
        TrailerfileName = filepath + '//Trailer'
        if not os.path.exists(TrailerfileName):
            os.mkdir(TrailerfileName)
        TrailerfileName1 = TrailerfileName + '//NoTrailer'
        Record1.pop(-1)
        writefile = open(TrailerfileName1, 'w+')
        for subrecord in Record1:
            writefile.write(str(subrecord))
        writefile.close()


    writefile=open(filename,'w+')
    for subrecord in FileRecord:
        writefile.write(str(subrecord))
    writefile.close()


def FieldChecker(a,b):
    if b.__contains__(a):
        print(a)
        logger.error(f'{FieldNumbers}\nThese are the field numbers which are already given')
        exit()
    else:
        b.add(a)
        return b

def MethodCall(option):
    dummy=[]
    if option==1:
        RequiredFields=input("Please give the Field Numbers in comma separated(1,2,3) for the required Positive Field and give '0' for all Fields:")
        RequiredFieldsList = RequiredFields.split(',')
        if len(RequiredFieldsList)==1 and RequiredFieldsList[0]=='0':
            PositiveRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields, ValidCounter,InvalidCounter, False, dummy)
        else:
            PositiveRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,True, RequiredFieldsList)
        return True
    elif option==2:
        dummy=[]
        RequiredFields = input("Please give the Field Numbers in comma separated(1,2,3) for the required Negative Field((Only For Mandatory Fields will be done):")
        RequiredFieldsList = RequiredFields.split(',')
        if len(RequiredFieldsList) == 1 and RequiredFieldsList[0] == '0':
            NegativeMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields,
                                     ValidCounter, InvalidCounter, False, dummy)
        else:
            NegativeMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields,ValidCounter, InvalidCounter, True, RequiredFieldsList)
        return True
    elif option==3:
        dummy=[]
        RequiredFields = input("Please give the Field Numbers in comma separated(1,2,3) for the required Blank Field(Only For Mandatory Fields will be done):")
        RequiredFieldsList = RequiredFields.split(',')
        if len(RequiredFieldsList) == 1 and RequiredFieldsList[0] == '0':
            BlankRecord(Header, Trailer, MandatoryFields, TotalValidFields, False, dummy)
        else:
            BlankRecord(Header,Trailer,MandatoryFields,TotalValidFields,True,RequiredFieldsList)
        return True
    elif option==4:
        RequiredFieldsList=[]
        PositiveRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,False,RequiredFieldsList)
        BlankRecord(Header,Trailer,MandatoryFields,TotalValidFields,False,RequiredFieldsList)
        NegativeMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields,ValidCounter, InvalidCounter, False, RequiredFieldsList)
        InvalidNonMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields, ValidCounter,InvalidCounter, False, RequiredFieldsList)
        return True
    else:
        print("You have given the Wrong Option, please give proper Integer Number (:")
        return False

def RemoveSpaces(Field):
    FieldName1 = Field.replace(" ", "")
    FieldName2 = FieldName1.replace('/', '')
    FieldName3 = FieldName2.replace('//', '')
    return FieldName3


def GetFieldName(FieldNumber):
    for Field,FN in FieldsWithNumbers.items():
        if FN==FieldNumber:
            return Field
    return "dummy"

def checkInput(a):
    if a == 'Y' or a == 'y':
        return True
    elif a == 'N' or a == 'n':
        return False
    else:
        ProperInput = input('Please reply with either ' + ' "Y"' + ' or ' + '"N":')
        return checkInput(ProperInput)

def MandatoryCheck(a,i='nan'):
    if a == 'Y' or a == 'y':
        return True
    elif a == 'N' or a == 'n':
        return False
    else:
        logger.warning(f'Mandatory Status for the field "{i}" is not given')
        ProperInput = input('Please reply with either ' + ' "Y"' + ' or ' + '"N":')
        return MandatoryCheck(ProperInput,i)

def BlankRecord(Header, Trailer,MandatoryFields,TotalValidFields,RequiredFieldFlag,RequiredFieldList):

    for i in  MandatoryFields:
        CSVRecord = []
        FileRecord = []
        Count = 1
        if RequiredFieldFlag:
            RequiredFieldNumber=str(FieldsWithNumbers[i])
            if not RequiredFieldList.__contains__(RequiredFieldNumber):
                continue
        ClearedFieldName=RemoveSpaces(i)
        fileDirectory=filepath + '//' + str(ClearedFieldName)
        if not os.path.exists(fileDirectory):
            os.mkdir(fileDirectory)
        fileDirectory1=fileDirectory+'//BlankRecords'
        if not os.path.exists(fileDirectory1):
            os.mkdir(fileDirectory1)
        filename1=fileDirectory1+'//'+ str(Count)
        Count=Count+1
        if Header:
            global HeaderList
            global FileHeaderText
            CSVRecord.append(HeaderList)
            FileRecord.append(FileHeaderText)

        RecordFieldList = []
        for j in range(1,TotalFieldsNumber+1):
            if j==int(MandatoryFields[i]) or len(TotalValidFields[j])==0:
                RecordFieldList.append(' ')
                FileRecord.append(separator)
            else:
                appendstring=str(TotalValidFields[j][0]) + separator
                FileRecord.append(appendstring)
                RecordFieldList.append(str(TotalValidFields[j][0]))
        CSVRecord.append(RecordFieldList)

        if Trailer:
            global TrailerList
            global FileTrailerText
            CSVRecord.append(TrailerList)
            FileRecord.append(FileTrailerText)
        if FileTrue:
            FileConvert(FileRecord, filename1)
        else:
            CsvConvert(CSVRecord, filename1)

def InvalidNonMandatoryRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,RequiredFieldFlag,RequiredFieldsList):
    for i in TotalInvalidFields:
        if GetFieldName(i) not in MandatoryFields.keys():
            if RequiredFieldFlag:
                if not RequiredFieldsList.__contains__(str(i)):
                    continue
            for j in range(0,len(TotalInvalidFields[i])):
                CSVRecord = []
                FileRecord = []
                FieldName=GetFieldName(i)
                ClearedFieldName=RemoveSpaces(FieldName)
                fileDirectory=filepath+'//'+ClearedFieldName
                if not os.path.exists(fileDirectory):
                    os.mkdir(fileDirectory)
                fileDirectory1=fileDirectory+'//InvalidRecords'
                if not os.path.exists(fileDirectory1):
                    os.mkdir(fileDirectory1)
                filename1 = fileDirectory1 + '//' + str(j + 1)
                toprint=''
                if Header:
                    global HeaderList
                    global FileHeaderText
                    CSVRecord.append(HeaderList)
                    FileRecord.append(FileHeaderText)
                employeeflag=False
                RC = TotalValidFields[RelationshipCodeNumber][ValidCounter[RelationshipCodeNumber]]
                global EmployeeFieldValue
                if RC == EmployeeFieldValue:
                    employeeflag = True
                RecordFieldList = []
                for k in range(1, TotalFieldsNumber + 1):
                    if len(TotalValidFields[k]) >= 1:
                        if employeeflag:
                            if k == SSNFieldNumber:
                                if SSNFieldNumber > SubscriberSSNFieldNumber:
                                    appendstring = str(
                                        TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                    FileRecord.append(appendstring)
                                    RecordFieldList.append(
                                        str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                    ValidCounter[SSNFieldNumber] -= 1
                                    if ValidCounter[SSNFieldNumber] == -1:
                                        ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                            elif k == SubscriberSSNFieldNumber:
                                if SSNFieldNumber > SubscriberSSNFieldNumber:
                                    appendstring = str(
                                        TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                    FileRecord.append(appendstring)
                                    RecordFieldList.append(
                                        str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                else:
                                    appendstring = str(
                                        TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                    FileRecord.append(appendstring)
                                    RecordFieldList.append(
                                        str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                    ValidCounter[SSNFieldNumber] -= 1
                                    if ValidCounter[SSNFieldNumber] == -1:
                                        ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                            else:
                                if k != SSNFieldNumber or k != SubscriberSSNFieldNumber:
                                    Number = ValidCounter[k]
                                    appendstring = str(TotalValidFields[k][Number]) + separator
                                    FileRecord.append(appendstring)
                                    RecordFieldList.append(str(TotalValidFields[k][Number]))
                                    ValidCounter[k] = ValidCounter[k] - 1
                                    if ValidCounter[k] == -1:
                                        ValidCounter[k] = len(TotalValidFields[k]) - 1
                        else:
                            Number = ValidCounter[k]
                            appendstring = str(TotalValidFields[k][Number]) + separator
                            FileRecord.append(appendstring)
                            RecordFieldList.append(str(TotalValidFields[k][Number]))
                            ValidCounter[k] = ValidCounter[k] - 1
                            if ValidCounter[k] == -1:
                                ValidCounter[k] = len(TotalValidFields[k]) - 1

                    else:
                        RecordFieldList.append(' ')
                        FileRecord.append(separator)
                CSVRecord.append(RecordFieldList)
                if Trailer:
                    global TrailerList
                    global FileTrailerText
                    CSVRecord.append(TrailerList)
                    FileRecord.append(FileTrailerText)
                if FileTrue:
                    FileConvert(FileRecord, filename1)
                else:
                    CsvConvert(CSVRecord, filename1)

def PositiveRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,RequiredFieldFlag,RequiredFieldsList):
    for i in TotalValidFields:
        if RequiredFieldFlag:
            if not RequiredFieldsList.__contains__(str(i)):
                continue
        for j in range(0,len(TotalValidFields[i])):
            CSVRecord = []
            FileRecord = []
            FieldName=GetFieldName(i)
            ClearedFieldName=RemoveSpaces(FieldName)
            fileDirectory = filepath + '//'+ClearedFieldName
            if not os.path.exists(fileDirectory):
                os.mkdir(fileDirectory)
            fileDirectory1=fileDirectory+'//ValidRecords'
            if not os.path.exists(fileDirectory1):
                os.mkdir(fileDirectory1)

            filename1= fileDirectory1 + '//' + str(j+1)
            if Header:
                global HeaderList
                global FileHeaderText
                CSVRecord.append(HeaderList)
                FileRecord.append(FileHeaderText)
            employeeflag=False
            RC = TotalValidFields[RelationshipCodeNumber][ValidCounter[RelationshipCodeNumber]]
            global EmployeeFieldValue
            if RC == EmployeeFieldValue:
                employeeflag = True
            RecordFieldList = []
            for k in range(1, TotalFieldsNumber + 1):
                if len(TotalValidFields[k]) >= 1:
                    if employeeflag:
                        if k == SSNFieldNumber:
                            if SSNFieldNumber > SubscriberSSNFieldNumber:
                                appendstring = str(
                                    TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                FileRecord.append(appendstring)
                                RecordFieldList.append(
                                    str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                ValidCounter[SSNFieldNumber] -= 1
                                if ValidCounter[SSNFieldNumber] == -1:
                                    ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                        elif k == SubscriberSSNFieldNumber:
                            if SSNFieldNumber > SubscriberSSNFieldNumber:
                                appendstring = str(
                                    TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                RecordFieldList.append(
                                    str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                FileRecord.append(appendstring)

                            else:
                                appendstring = str(
                                    TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                FileRecord.append(appendstring)
                                RecordFieldList.append(
                                    str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                ValidCounter[SSNFieldNumber] -= 1
                                if ValidCounter[SSNFieldNumber] == -1:
                                    ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                        else:
                            if k != SSNFieldNumber or k != SubscriberSSNFieldNumber:
                                Number = ValidCounter[k]
                                appendstring = str(TotalValidFields[k][Number]) + separator
                                RecordFieldList.append(str(TotalValidFields[k][Number]))
                                FileRecord.append(appendstring)
                                ValidCounter[k] = ValidCounter[k] - 1
                                if ValidCounter[k] == -1:
                                    ValidCounter[k] = len(TotalValidFields[k]) - 1
                    else:
                        Number = ValidCounter[k]
                        appendstring = str(TotalValidFields[k][Number]) + separator
                        FileRecord.append(appendstring)
                        RecordFieldList.append(str(TotalValidFields[k][Number]))
                        ValidCounter[k] = ValidCounter[k] - 1
                        if ValidCounter[k] == -1:
                            ValidCounter[k] = len(TotalValidFields[k]) - 1

                else:
                    RecordFieldList.append(' ')
                    FileRecord.append(separator)

            CSVRecord.append(RecordFieldList)
            if Trailer:
                global TrailerList
                global FileTrailerText
                CSVRecord.append(TrailerList)
                FileRecord.append(FileTrailerText)
            if FileTrue:
                FileConvert(FileRecord, filename1)
            else:
                CsvConvert(CSVRecord, filename1)

def NegativeMandatoryRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,RequiredFieldFlag,RequiredFieldsList):
    for field in MandatoryFields:
        if RequiredFieldFlag:
            RequiredFieldNumber = str(FieldsWithNumbers[field])
            if not RequiredFieldsList.__contains__(RequiredFieldNumber):
                continue
        ClearedFieldName=RemoveSpaces(field)
        fileDirectory = filepath + '//'+str(ClearedFieldName)
        if not os.path.exists(fileDirectory):
            os.mkdir(fileDirectory)
        fileDirectory1 = fileDirectory + '//InvalidRecords'
        if not os.path.exists(fileDirectory1):
            os.mkdir(fileDirectory1)
        MandatoryFieldNumber=MandatoryFields[field]
        InvalidValuesLength=len(TotalInvalidFields[MandatoryFieldNumber])

        for count in range(0,InvalidValuesLength):
            CSVRecord = []
            FileRecord=[]
            filename1 = fileDirectory1 +  '//' +str(count+1)
            if Header:
                global HeaderList
                global FileHeaderText
                CSVRecord.append(HeaderList)
                FileRecord.append(FileHeaderText)
            RecordFieldList = []
            for j in range(1,TotalFieldsNumber+1):
                if j==MandatoryFieldNumber:
                    appendstring=str(TotalInvalidFields[j][count])+separator
                    RecordFieldList.append(str(TotalInvalidFields[j][count]))
                    FileRecord.append(appendstring)
                    count=count+1
                elif len(TotalValidFields[j])==0:
                    RecordFieldList.append(' ')
                    FileRecord.append(separator)
                else:
                    appendstring=str(TotalValidFields[j][0])+separator
                    FileRecord.append(appendstring)
                    RecordFieldList.append(str(TotalValidFields[j][0]))
            CSVRecord.append(RecordFieldList)
            if Trailer:
                global TrailerList
                global FileTrailerText
                CSVRecord.append(TrailerList)
                FileRecord.append(FileTrailerText)
            if FileTrue:
                FileConvert(FileRecord, filename1)
            else:
                CsvConvert(CSVRecord, filename1)



Header = False
Trailer = False
separator = ''
RequiredSeparator = parser.get('Definition','separator')
if RequiredSeparator == '\\t':
    separator = '\t'
else:
    separator = RequiredSeparator
logger.info(f'Delimiter "{separator}" is given for output file')
filepath=parser.get('Definition','OutputFilePath')

try:
    if not os.path.exists(filepath):
        os.mkdir(filepath)
except FileNotFoundError:
    logger.error(f'Output filePath {filepath} is Improper.Please Check')
    exit()

Header=parser.getboolean('Definition','Header')
if Header:
    logger.info('"Header" is Present')
else:
    logger.info('"Header" is not Present')
Trailer=parser.getboolean('Definition','Trailer')
if Trailer:
    logger.info('"Trailer" is present')
else:
    logger.info('"Trailer" is not Present')

ReadFilePath = parser.get('Definition', 'RecordDeclaration')

FieldNumbers = set()
FieldPossibleValues = {}
Numbers1 = []
HeaderDone = False
TrailerDone = False
RequiredFieldsList = []
MandatoryFields = {}
FieldsWithNumbers = {}
ValidCounter = {}
InvalidCounter = {}
TotalValidFields = {}
TotalInvalidFields = {}

FileTrue = True
HeaderList = []
TrailerList = []
optionFile = parser.get('Definition', 'OutputFileFormat')
if optionFile == 'CSV':
    FileTrue = False
    logger.info('Output File Format is CSV')
else:
    logger.info('Output File Format is Text')
FileHeaderText = "Header" + "\n"
FileTrailerText = "\n" + "Trailer"
CSVHeaderText = "Header"
CSVTrailerText = "Trailer"
SeparateHeader = False
SeparateTrailer = False
SeparateHeader = parser.getboolean('Definition', 'SeparateHeader')
SeparateTrailer = parser.getboolean('Definition', 'SeparateTrailer')

if Header and SeparateHeader:
    DefaultHeaderPath = parser.get('Definition', 'DefaultHeaderPath')
    try:
        HeaderFile = open(DefaultHeaderPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultHeaderPath "{DefaultHeaderPath}" is not proper\n Check the FilePath')
        exit()
    CSVHeaderText = HeaderFile.readline().strip()
    FileHeaderText = CSVHeaderText + '\n'

HeaderList.append(CSVHeaderText)

if Trailer and SeparateTrailer:
    DefaultTrailerPath = parser.get('Definition', 'DefaultTrailerPath')
    try:
        TrailerFile = open(DefaultTrailerPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultTrailerPath "{DefaultTrailerPath}" is not proper\n Check the FilePath')
        exit()
    CSVTrailerText = TrailerFile.readline().strip()
    FileTrailerText = '\n' + CSVTrailerText

TrailerList.append(CSVTrailerText)

EmployeeFieldValue=str(parser.get('Definition','EmployeeFieldValue'))
logger.info(f'Employee Field Value is {EmployeeFieldValue}')

try:
    file = open(ReadFilePath, 'r')
except FileNotFoundError:
    logger.error(f'RecordDeclaration File Path {ReadFilePath} is improper.Please Check')
    exit()
Headers = file.readline().strip().split('\t')
Numbers = file.readlines()[1].split('\t')

Traverse = 0

for i in Numbers:
    if str(i)=='':
        logger.warning(f'The Field Number for {Headers[Traverse]} is not mentioned')
        AskFieldNumber = (input("Please give the Field Number for " + Headers[Traverse] + ':'))
        i = AskFieldNumber

    if Numbers1.__contains__(int(i)):
        logger.warning(f'The Field Number {i} is present for  {Headers[Traverse]} is present already')
        logger.error('Please Add the Field Number and try again (:')
        exit(0)

    Numbers1.append(int(i))
    Traverse += 1
file.close()



TotalFieldsNumber = max(Numbers1)
for i in range(1, TotalFieldsNumber + 1):
    TotalValidFields[i] = []
    TotalInvalidFields[i] = []


df = pd.read_csv(ReadFilePath, sep='\t', dtype=str)
for toprow in Headers:
    ColumnList = df[toprow].values.tolist()
    RealColumnList = []
    mandatory = True
    Field = True
    for i in ColumnList:
        if str(i) == 'nan':
            if mandatory:
                logger.warning(f'The mandatory status for the field "{toprow}" is not mentioned:')
                InputMandatory = input('Enter the Status with ' + '"Y" or ' + '"N":')
                IsMandatoryField = MandatoryCheck(InputMandatory, i)
                try:
                    topRowNumber = int(ColumnList[1])
                except ValueError:
                    topRowNumber = int(input('Please Give the Field Number for ' + toprow + ' :'))
                FieldNumbers = FieldChecker(topRowNumber, FieldNumbers)
                if IsMandatoryField:
                    MandatoryFields[toprow] = topRowNumber
                FieldsWithNumbers[toprow] = topRowNumber
                mandatory = False
            else:
                continue
        elif mandatory:
            IsMandatoryField = MandatoryCheck(i, toprow)
            try:
                topRowNumber = int(ColumnList[list(ColumnList).index(i) + 1])
            except ValueError:
                topRowNumber = int(input('Please Give the Field Number for ' + toprow + ' :'))
            FieldNumbers = FieldChecker(topRowNumber, FieldNumbers)
            if IsMandatoryField:
                MandatoryFields[toprow] = topRowNumber
            FieldsWithNumbers[toprow] = topRowNumber
            mandatory = False
        elif Field:
            Field = False
            continue
        else:
            RealColumnList.append(i)
    FieldPossibleValues[toprow] = RealColumnList
    ValidtopRow = []
    InvalidtopRow = []
    if len(FieldPossibleValues) >= 1:
        for i in range(0, len(FieldPossibleValues[toprow])):
            if str(FieldPossibleValues[toprow][i]).strip()[-1] == 'v' or \
                    str(FieldPossibleValues[toprow][i]).strip()[-1] == 'V':
                ValidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
            elif str(FieldPossibleValues[toprow][i]).strip()[-1] == 'i' or \
                    str(FieldPossibleValues[toprow][i]).strip()[-1] == 'I':
                InvalidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
            else:
                logger.warning(f'The value "{str(FieldPossibleValues[toprow][i])}" is not ended with either v or i for the field "{toprow}"')
                ValidInput = input('Do you want to Consider it as' + '"Valid"' + ' or ' + '"Invalid":')
                if ValidInput.lower() == 'Valid'.lower():
                    ValidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
                    logger.info("Considered as Valid Input")
                else:
                    InvalidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
                    logger.info("Considered as Invalid Input")
    if len(ValidtopRow) >= 1:
        TotalValidFields[topRowNumber] = ValidtopRow
        ValidCounter[topRowNumber] = len(ValidtopRow) - 1
    if len(InvalidtopRow) >= 1:
        TotalInvalidFields[topRowNumber] = InvalidtopRow
        InvalidCounter[topRowNumber] = len(InvalidtopRow) - 1

SSNFieldNumber = int(parser.get('Definition', 'SSNFieldNumber'))
if not FieldNumbers.__contains__(SSNFieldNumber):
    logger.error('provided  SSN Number is not mentioned in CSV.Please Check')
    exit()
logger.info(f'SSNFieldNumber is {SSNFieldNumber}')
SubscriberSSNFieldNumber = int(parser.get('Definition', 'SubscriberSSNFieldNumber'))
if not FieldNumbers.__contains__(SubscriberSSNFieldNumber):
    logger.error('provided Subscriber SSN Number is not mentioned in CSV.Please Check')
    exit()
logger.info(f'SubscriberSSNFieldNumber is {SubscriberSSNFieldNumber}')
RelationshipCodeNumber = int(parser.get('Definition', 'RelationshipCodeNumber'))
if not FieldNumbers.__contains__(RelationshipCodeNumber):
    logger.error('provided Relationship Code Number is not present in CSV.Please check')
    exit()
logger.info(f'RelationshipCodeNumber is {RelationshipCodeNumber}')

RequiredSSNNumber=0
for i in TotalValidFields:
    if i!=SSNFieldNumber:
        RequiredSSNNumber+=len(TotalValidFields[i])

if(RequiredSSNNumber > len(TotalValidFields[SSNFieldNumber])):
    logger.warning(f'Since the Valid Fields are in "{RequiredSSNNumber}",but you have given unique SSNs of {len(TotalValidFields[SSNFieldNumber])}')
    print('In order to avoid the overiding of basic info to existing upin,Please give valid SSNs')


 # Add Logs for this
print("These are the Fields for your ETL:\n")
print("{:>36} {:>10} {:>10}".format('FieldName', 'FieldNumbers', 'MandatoryStatus'))
for k in sorted(FieldNumbers):
    value = MandatoryFields.__contains__(GetFieldName(k))
    if value:
        status = 'True'
    else:
        status = 'False'
    print("{:>36}{:>10} {:>10}".format(GetFieldName(k), FieldsWithNumbers[GetFieldName(k)], status))


if __name__=='__main__':

    print("Select the appropriate Following Number (1,2,3,4) according to your requirement:\n")
    print("{:1} {:30}".format('1.', 'only Positive Records'))
    print("{:1} {:30}".format('2.', 'only Invalid/Negative Records'))
    print("{:1} {:30}".format('3.', 'only Blank Records'))
    print("{:1} {:30}".format('4.', 'All of the Above'))

    Callstatus = False
    while Callstatus == False:
        option = int(input('Enter the option here:'))
        Callstatus = MethodCall(option)
    print("Test data is Generated at the Specified Path",filepath)









