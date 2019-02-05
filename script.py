
from configparser import ConfigParser
from Method import *
import os
import logging
import pandas as pd


def FieldChecker(a,b):
    if b.__contains__(a):
        print(a)
        print(*FieldNumbers,sep=',')
        print('These are the field numbers which are already given')
        exit()
    else:
        b.add(a)
        return b

def RemoveSpaces(Field):
    FieldName1 = Field.replace(" ", "")
    FieldName2 = FieldName1.replace('/', '')
    FieldName3 = FieldName2.replace('//', '')
    return FieldName3

def CheckFieldNumber(topRowNumber,TotalFieldsNumber):
    if topRowNumber>TotalFieldsNumber:
        return CheckFieldNumber(int(input("Since the Field Number is greater than Total Number of Fields,please give the correct Field number:")),TotalFieldsNumber)
    else:
        return topRowNumber

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
        print('Mandatory Status for the field ' + '"'+ i+'"'+ ' is not given')
        ProperInput = input('Please reply with either ' + ' "Y"' + ' or ' + '"N":')
        return MandatoryCheck(ProperInput,i)

Header = False
Trailer = False
separator = ''
logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
parser = ConfigParser()
parser.read('properties.config')
RequiredSeparator = parser.get('Definition','separator')
if RequiredSeparator == '\\t':
    separator = '\t'
else:
    separator = RequiredSeparator
logging.info(f'Delimiter "{separator}" is given for output file')
filepath=parser.get('Definition','OutputFilePath')
if not os.path.exists(filepath):
    os.mkdir(filepath)
Header=parser.get('Definition','Header')
if Header:
    logger.info("Header is Present")
Trailer=parser.get('Definition','Trailer')
if Trailer:
    logger.info("Trailer is present")
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
DefaultHeader = False
DefaultTrailer = False
DefaultHeader = parser.getboolean('Definition', 'DefaultHeader')
DefaultTrailer = parser.getboolean('Definition', 'DefaultTrailer')

if Header and DefaultHeader:
    DefaultHeaderPath = parser.get('Definition', 'DefaultHeaderPath')
    try:
        HeaderFile = open(DefaultHeaderPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultHeaderPath "{DefaultHeaderPath}" is not proper\n Check the FilePath')
        exit()
    CSVHeaderText = HeaderFile.readline().strip()
    FileHeaderText = CSVHeaderText + '\n'

HeaderList.append(CSVHeaderText)

if Trailer and DefaultTrailer:
    DefaultTrailerPath = parser.get('Definition', 'DefaultTrailerPath')
    try:
        TrailerFile = open(DefaultTrailerPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultTrailerPath "{DefaultTrailerPath}" is not proper\n Check the FilePath')
    CSVTrailerText = TrailerFile.readline().strip()
    FileTrailerText = '\n' + CSVTrailerText

TrailerList.append(CSVTrailerText)

# Handle exception here
file = open(ReadFilePath, 'r')
Headers = file.readline().strip().split('\t')
Numbers = file.readlines()[1].strip().split('\t')

Traverse = 0

for i in Numbers:
    if str(i) == '':
        logger.error(f'Field Number for "{Headers[Traverse]}" is not mentioned')
        AskFieldNumber = (input("Please give the Field Number for " + Headers[Traverse] + ':'))
        i = AskFieldNumber

    if Numbers1.__contains__(int(i)):
        print('The Field Number ' + i + ' is present for ' + Headers[Traverse] + ' is present already')
        print('Please Add the Field Number and try again (:')
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
                print('The mandatory status for the field ' + '"' + toprow + '"' + ' is not mentioned:')
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
                ValidInput = input('The value ' + str(
                    FieldPossibleValues[toprow][
                        i]) + ' is not ended with either v or i for the field ' + toprow +
                                   '\n Do you want to Consider it as' + '"Valid"' + ' or ' + '"Invalid":')
                if ValidInput.lower() == 'Valid'.lower():
                    ValidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
                    print('Valid')
                else:
                    InvalidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
    if len(ValidtopRow) >= 1:
        TotalValidFields[topRowNumber] = ValidtopRow
        ValidCounter[topRowNumber] = len(ValidtopRow) - 1
    if len(InvalidtopRow) >= 1:
        TotalInvalidFields[topRowNumber] = InvalidtopRow
        InvalidCounter[topRowNumber] = len(InvalidtopRow) - 1




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

SSNFieldNumber = int(parser.get('Definition', 'SSNFieldNumber'))
if not FieldNumbers.__contains__(SSNFieldNumber):
    print("provided  SSN Number is not mentioned in CSV.Please Check")
    exit()
SubscriberSSNFieldNumber = int(parser.get('Definition', 'SubscriberSSNFieldNumber'))
if not FieldNumbers.__contains__(SubscriberSSNFieldNumber):
    print("provided Subscriber SSN Number is not mentioned in CSV.Please Check")
    exit()
RelationshipCodeNumber = int(parser.get('Definition', 'RelationshipCodeNumber'))
if not FieldNumbers.__contains__(RelationshipCodeNumber):
    print("provided Relationship Code Number is not present in CSV.Please check")
    exit()

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









