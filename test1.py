
from configparser import ConfigParser


def FieldChecker(a,b):
    if b.__contains__(a):
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
            if RC == '01' or RC == '1':
                employeeflag = True
            RecordFieldList = []
            for k in range(1, TotalFieldsNumber + 1):
                if k==i:
                    if employeeflag and SubscriberSSNFieldNumber==k:
                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                        FileRecord.append(appendstring)
                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                        continue
                    else:
                        appendstring = str(TotalValidFields[i][j]) + separator
                        FileRecord.append(appendstring)
                        RecordFieldList.append(str(TotalValidFields[i][j]))
                else:
                    if len(TotalValidFields[k]) >=1:
                        if employeeflag:
                            if k==SSNFieldNumber:
                                if SSNFieldNumber>SubscriberSSNFieldNumber:
                                    appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                    FileRecord.append(appendstring)
                                    RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                    ValidCounter[SSNFieldNumber] -= 1
                                    if ValidCounter[SSNFieldNumber] == -1:
                                        ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                            elif k==SubscriberSSNFieldNumber:
                                    if SSNFieldNumber > SubscriberSSNFieldNumber:
                                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                        FileRecord.append(appendstring)

                                    else:
                                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                        FileRecord.append(appendstring)
                                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                        ValidCounter[SSNFieldNumber]-=1
                                        if ValidCounter[SSNFieldNumber]==-1:
                                            ValidCounter[SSNFieldNumber]=len(TotalValidFields[SSNFieldNumber])-1

                            else:
                                if k!=SSNFieldNumber or k!=SubscriberSSNFieldNumber:
                                    Number=ValidCounter[k]
                                    appendstring=str(TotalValidFields[k][Number]) + separator
                                    RecordFieldList.append(str(TotalValidFields[k][Number]))
                                    FileRecord.append(appendstring)
                                    ValidCounter[k]=ValidCounter[k]-1
                                    if ValidCounter[k]==-1:
                                        ValidCounter[k]=len(TotalValidFields[k])-1
                        else:
                            Number = ValidCounter[k]
                            appendstring=str(TotalValidFields[k][Number]) + separator
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
                if Header:
                    global HeaderList
                    global FileHeaderText
                    CSVRecord.append(HeaderList)
                    FileRecord.append(FileHeaderText)

                employeeflag=False
                RC = TotalValidFields[RelationshipCodeNumber][ValidCounter[RelationshipCodeNumber]]
                if RC == '01' or RC == '1':
                    employeeflag = True
                RecordFieldList = []
                for k in range(1, TotalFieldsNumber + 1):
                    if k == i:
                        if employeeflag and SubscriberSSNFieldNumber == k:
                            appendstring=str(TotalInvalidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                            FileRecord.append(appendstring)
                            RecordFieldList.append(str(TotalInvalidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                            continue
                        else:
                            RecordFieldList.append(str(TotalInvalidFields[i][j]))
                            appendstring=str(TotalInvalidFields[i][j]) + separator
                            FileRecord.append(appendstring)
                    else:
                        if len(TotalValidFields[k]) >= 1:
                            if employeeflag:
                                if k == SSNFieldNumber:
                                    if SSNFieldNumber > SubscriberSSNFieldNumber:
                                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                        FileRecord.append(appendstring)
                                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                        ValidCounter[SSNFieldNumber] -= 1
                                        if ValidCounter[SSNFieldNumber] == -1:
                                            ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                                elif k == SubscriberSSNFieldNumber:
                                    if SSNFieldNumber > SubscriberSSNFieldNumber:
                                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                        FileRecord.append(appendstring)
                                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                    else:
                                        appendstring=str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]) + separator
                                        FileRecord.append(appendstring)
                                        RecordFieldList.append(str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]))
                                        ValidCounter[SSNFieldNumber] -= 1
                                        if ValidCounter[SSNFieldNumber] == -1:
                                            ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                                else:
                                    if k != SSNFieldNumber or k != SubscriberSSNFieldNumber:
                                        Number = ValidCounter[k]
                                        appendstring=str(TotalValidFields[k][Number]) + separator
                                        FileRecord.append(appendstring)
                                        RecordFieldList.append(str(TotalValidFields[k][Number]))
                                        ValidCounter[k] = ValidCounter[k] - 1
                                        if ValidCounter[k] == -1:
                                            ValidCounter[k] = len(TotalValidFields[k]) - 1
                            else:
                                Number = ValidCounter[k]
                                appendstring=str(TotalValidFields[k][Number]) + separator
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


import csv
import os
import pandas as pd

parser = ConfigParser()
parser.read('properties.config')
RequiredSeparator = parser.get('Definition','separator')
separator = ''
if RequiredSeparator == '\\t':
    separator = '\t'
else:
    separator = RequiredSeparator

filepath=parser.get('Definition','OutputFilePath')
if not os.path.exists(filepath):
    os.mkdir(filepath)



Header = False
Trailer = False

Header=parser.get('Definition','Header')
Trailer=parser.get('Definition','Trailer')


ReadFilePath = parser.get('Definition','RecordDeclaration')
FieldNumbers=set()
FieldPossibleValues={}
Numbers1=[]
HeaderDone=False
TrailerDone=False
RequiredFieldsList=[]
MandatoryFields={}
FieldsWithNumbers={}
ValidCounter = {}
InvalidCounter={}
TotalValidFields={}
TotalInvalidFields={}

FileTrue=True
optionFile=parser.get('Definition','OutputFileFormat')
if optionFile=='CSV':
    FileTrue=False

HeaderList=[]
TrailerList=[]
FileHeaderText="Header" + "\n"
FileTrailerText="\n" + "Trailer"
CSVHeaderText="Header"
CSVTrailerText="Trailer"
DefaultHeader=False
DefaultTrailer=False
DefaultHeader=parser.getboolean('Definition','DefaultHeader')
DefaultTrailer=parser.getboolean('Definition','DefaultTrailer')

if Header and DefaultHeader:
    DefaultHeaderPath=parser.get('Definition','DefaultHeaderPath')
    HeaderFile=open(DefaultHeaderPath,'r')
    CSVHeaderText=HeaderFile.readline().strip()
    FileHeaderText=CSVHeaderText+'\n'

HeaderList.append(CSVHeaderText)

if Trailer and DefaultTrailer:
    DefaultTrailerPath=parser.get('Definition','DefaultTrailerPath')
    TrailerFile=open(DefaultTrailerPath,'r')
    CSVTrailerText=TrailerFile.readline().strip()
    FileTrailerText='\n'+ CSVTrailerText

TrailerList.append(CSVTrailerText)

file=open(ReadFilePath,'r')
Headers=file.readline().strip().split('\t')
Numbers=file.readlines()[1].strip().split('\t')
Traverse=0
for i in Numbers:
    if str(i)=='':
        print('Field Number for ' + Headers[Traverse] +' is not mentioned')
        AskFieldNumber=(input("Please give the Field Number for " + Headers[Traverse] +':' ))
        i=AskFieldNumber

    if Numbers1.__contains__(int(i)):
        print('The Field Number ' + i + ' is present for ' + Headers[Traverse] + ' is present already')
        print('Please Add the Field Number and try again (:')
        exit(0)

    Numbers1.append(int(i))
    Traverse+=1
file.close()

TotalFieldsNumber=max(Numbers1)
for i in range(1,TotalFieldsNumber+1):
    TotalValidFields[i]=[]
    TotalInvalidFields[i]=[]



df=pd.read_csv(ReadFilePath,sep='\t',dtype=str)
for toprow in Headers:
    ColumnList=df[toprow].values.tolist()
    RealColumnList=[]
    mandatory =True
    Field=True
    for i in ColumnList:
        if str(i)=='nan':
            if mandatory:
                print('The mandatory status for the field ' + '"'+toprow+'"' + ' is not mentioned:')
                InputMandatory=input('Enter the Status with '  + '"Y" or ' + '"N":')
                IsMandatoryField=MandatoryCheck(InputMandatory,i)
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
            IsMandatoryField=MandatoryCheck(i,toprow)
            try:
                topRowNumber=int(ColumnList[list(ColumnList).index(i)+1])
            except ValueError:
                topRowNumber=int(input('Please Give the Field Number for ' + toprow+ ' :'))
            FieldNumbers=FieldChecker(topRowNumber,FieldNumbers)
            if IsMandatoryField:
                MandatoryFields[toprow]=topRowNumber
            FieldsWithNumbers[toprow]=topRowNumber
            mandatory=False
        elif Field:
            Field=False
            continue
        else:
            RealColumnList.append(i)
    FieldPossibleValues[toprow]=RealColumnList
    ValidtopRow=[]
    InvalidtopRow=[]
    if len(FieldPossibleValues)>=1:
        for i in range(0,len(FieldPossibleValues[toprow])):
            if str(FieldPossibleValues[toprow][i]).strip()[-1] == 'v' or str(FieldPossibleValues[toprow][i]).strip()[-1]=='V':
                ValidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
            elif str(FieldPossibleValues[toprow][i]).strip()[-1] == 'i' or str(FieldPossibleValues[toprow][i]).strip()[-1]=='I':
                InvalidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
            else:
                ValidInput=input('The value '+ str(FieldPossibleValues[toprow][i]) + ' is not ended with either v or i for the field '+ toprow +
                '\n Do you want to Consider it as' + '"Valid"'+ ' or ' + '"Invalid":')
                if ValidInput.lower()=='Valid'.lower():
                    ValidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
                    print('Valid')
                else:
                    InvalidtopRow.append(str(FieldPossibleValues[toprow][i])[:-1])
    if len(ValidtopRow) >=1:
        TotalValidFields[topRowNumber]=ValidtopRow
        ValidCounter[topRowNumber]=len(ValidtopRow)-1
    if len(InvalidtopRow)>=1:
        TotalInvalidFields[topRowNumber]=InvalidtopRow
        InvalidCounter[topRowNumber]=len(InvalidtopRow)-1



print("These are the Fields for your ETL:\n")
print("{:>36} {:>10} {:>10}".format('FieldName','FieldNumbers','MandatoryStatus'))
for k in sorted(FieldNumbers):
    value=MandatoryFields.__contains__(GetFieldName(k))
    if value:
        status='True'
    else:
        status='False'
    print("{:>36}{:>10} {:>10}".format(GetFieldName(k),FieldsWithNumbers[GetFieldName(k)],status))

importantfields=[]

SSNFieldNumber=int(parser.get('Definition','SSNFieldNumber'))
if not FieldNumbers.__contains__(SSNFieldNumber):
    print("provided  SSN Number is not mentioned in CSV.Please Check")
    exit()
importantfields.append(SSNFieldNumber)
SubscriberSSNFieldNumber=int(parser.get('Definition','SubscriberSSNFieldNumber'))
if not FieldNumbers.__contains__(SubscriberSSNFieldNumber):
    print("provided Subscriber SSN Number is not mentioned in CSV.Please Check")
    exit()
importantfields.append(SubscriberSSNFieldNumber)
RelationshipCodeNumber= int(parser.get('Definition','RelationshipCodeNumber'))
if not FieldNumbers.__contains__(RelationshipCodeNumber):
    print("provided Relationship Code Number is not present in CSV.Please check")
    exit()
importantfields.append(RelationshipCodeNumber)


print("Select the appropriate Following Number (1,2,3,4) according to your requirement:\n")
print("{:1} {:30}".format('1.','only Positive Records'))
print("{:1} {:30}".format('2.','only Invalid/Negative Records'))
print("{:1} {:30}".format('3.','only Blank Records'))
print("{:1} {:30}".format('4.','All of the Above'))

Callstatus=False
while Callstatus==False:
    option = int(input('Enter the option here:'))
    Callstatus = MethodCall(option)







