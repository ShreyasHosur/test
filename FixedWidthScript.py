import pandas as pd
import logging
import os
from configparser import ConfigParser

parser = ConfigParser()
parser.read('FixedWidthProperties.config')
logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]-->%(message)s')
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def MandatoryCheck(a,i='nan'):
    if a == 'Y' or a == 'y':
        return True
    elif a == 'N' or a == 'n':
        return False
    else:
        logger.warning(f'Mandatory Status for the field "{i}" is not given')
        ProperInput = input('Please reply with either ' + ' "Y"' + ' or ' + '"N":')
        return MandatoryCheck(ProperInput,i)

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
        RequiredFields = input("Please give the Field Numbers in comma separated(1,2,3) for the required Negative Field((Only For Mandatory Fields will be done) and give '0' for all Fields::")
        RequiredFieldsList = RequiredFields.split(',')
        if len(RequiredFieldsList) == 1 and RequiredFieldsList[0] == '0':
            NegativeMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields,
                                     ValidCounter, InvalidCounter, False, dummy)
        else:
            NegativeMandatoryRecords(Header, Trailer, MandatoryFields, TotalValidFields, TotalInvalidFields,ValidCounter, InvalidCounter, True, RequiredFieldsList)
        return True
    elif option==3:
        dummy=[]
        RequiredFields = input("Please give the Field Numbers in comma separated(1,2,3) for the required Blank Field(Only For Mandatory Fields will be done) and give '0' for all Fields::")
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

def InvalidNonMandatoryRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,RequiredFieldFlag,RequiredFieldsList):
    for i in TotalInvalidFields:
        if GetFieldName(i) not in MandatoryFields.keys():
            if RequiredFieldFlag:
                if not RequiredFieldsList.__contains__(str(i)):
                    continue
            for j in range(0,len(TotalInvalidFields[i])):
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
                    global HeaderText
                    toprint+= HeaderText
                employeeflag=False
                RC = TotalValidFields[RelationshipCodeNumber][ValidCounter[RelationshipCodeNumber]]
                global EmployeeFieldValue
                if RC == EmployeeFieldValue:
                    employeeflag = True
                for k in sorted(StartList):
                    padding=' '
                    if k in PaddingFields:
                        padding='0'
                    length = 0
                    spaces = ''
                    if sorted(StartList).index(k) != 0:
                        previousEnd = sorted(StartList)[sorted(StartList).index(k) - 1]
                        if k - int(EndingPosition[previousEnd]) == 1:
                            length = int(EndingPosition[k]) - int(k) + 1
                        else:
                            length2 = k - int(EndingPosition[previousEnd])
                            spaces = ' ' * (length2 - 1)
                            length = int(EndingPosition[k]) - int(k) + 1
                    else:
                        length = int(EndingPosition[k]) - int(k) + 1
                    if k in ValidFieldNumbers:
                        if employeeflag:
                            if k == SSNFieldNumber:
                                if SSNFieldNumber > SubscriberSSNFieldNumber:
                                    toprint+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                    ValidCounter[SSNFieldNumber] -= 1
                                    if ValidCounter[SSNFieldNumber] == -1:
                                        ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                            elif k == SubscriberSSNFieldNumber:
                                if SSNFieldNumber > SubscriberSSNFieldNumber:
                                    toprint+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                else:
                                    toprint+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                    ValidCounter[SSNFieldNumber] -= 1
                                    if ValidCounter[SSNFieldNumber] == -1:
                                        ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                            else:
                                if k != SSNFieldNumber or k != SubscriberSSNFieldNumber:
                                    Number = ValidCounter[k]
                                    toprint+=spaces+str(TotalValidFields[k][Number]).ljust(length,padding)[:length]
                                    ValidCounter[k] = ValidCounter[k] - 1
                                    if ValidCounter[k] == -1:
                                        ValidCounter[k] = len(TotalValidFields[k]) - 1
                        else:
                            Number = ValidCounter[k]
                            toprint+=spaces+str(TotalValidFields[k][Number]).ljust(length,padding)[:length]
                            ValidCounter[k] = ValidCounter[k] - 1
                            if ValidCounter[k] == -1:
                                ValidCounter[k] = len(TotalValidFields[k]) - 1

                    else:
                        spaces2=' '*length
                        toprint+=spaces+spaces2
                if Trailer:
                    global TrailerText
                    toprint+= TrailerText
                file = open(filename1, 'w')
                file.write(toprint)
                file.close()



def PositiveRecords(Header,Trailer,MandatoryFields,TotalValidFields,TotalInvalidFields,ValidCounter,InvalidCounter,RequiredFieldFlag,RequiredFieldsList):
    for i in TotalValidFields:
        if RequiredFieldFlag:
            if not RequiredFieldsList.__contains__(str(i)):
                continue
        for j in range(0,len(TotalValidFields[i])):
            FieldName=GetFieldName(i)
            ClearedFieldName=RemoveSpaces(FieldName)
            fileDirectory = filepath + '//'+ClearedFieldName
            if not os.path.exists(fileDirectory):
                os.mkdir(fileDirectory)
            fileDirectory1=fileDirectory+'//ValidRecords'
            if not os.path.exists(fileDirectory1):
                os.mkdir(fileDirectory1)
            filename1= fileDirectory1 + '//' + str(j+1)
            toprint1 = ''
            toprint2 = ''
            toprint3 = ''
            if Header:
                global HeaderText
                toprint1+= HeaderText
            employeeflag=False
            RC = TotalValidFields[RelationshipCodeNumber][ValidCounter[RelationshipCodeNumber]]
            global EmployeeFieldValue
            if RC == EmployeeFieldValue:
                employeeflag = True
            for k in sorted(StartList):
                padding=' '
                if str(k) in PaddingFields:
                    padding='0'
                length=0
                spaces=''
                if sorted(StartList).index(k)!=0:
                    previousEnd = sorted(StartList)[sorted(StartList).index(k) - 1]
                    if k - int(EndingPosition[previousEnd]) == 1:
                        length = int(EndingPosition[k]) - int(k) + 1
                    else:
                        length2 = k - int(EndingPosition[previousEnd])
                        spaces = ' ' * (length2 - 1)
                        length=int(EndingPosition[k]) - int(k) + 1
                else:
                    length = int(EndingPosition[k]) - int(k) + 1

                if k in ValidFieldNumbers:
                    if employeeflag:
                        if k==SSNFieldNumber:
                            if SSNFieldNumber>SubscriberSSNFieldNumber:
                                toprint2+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                ValidCounter[SSNFieldNumber] -= 1
                                if ValidCounter[SSNFieldNumber] == -1:
                                    ValidCounter[SSNFieldNumber] = len(TotalValidFields[SSNFieldNumber]) - 1

                        elif k==SubscriberSSNFieldNumber:
                                if SSNFieldNumber > SubscriberSSNFieldNumber:
                                    toprint2+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                else:
                                    toprint2+=spaces+str(TotalValidFields[SSNFieldNumber][ValidCounter[SSNFieldNumber]]).ljust(length,padding)[:length]
                                    ValidCounter[SSNFieldNumber]-=1
                                    if ValidCounter[SSNFieldNumber]==-1:
                                        ValidCounter[SSNFieldNumber]=len(TotalValidFields[SSNFieldNumber])-1

                        else:
                            if k!=SSNFieldNumber or k!=SubscriberSSNFieldNumber:
                                Number=ValidCounter[k]
                                toprint2+=spaces+str(TotalValidFields[k][Number]).ljust(length,padding)[:length]
                                ValidCounter[k]=ValidCounter[k]-1
                                if ValidCounter[k]==-1:
                                    ValidCounter[k]=len(TotalValidFields[k])-1
                    else:
                        Number = ValidCounter[k]
                        toprint2+=spaces+str(TotalValidFields[k][Number]).ljust(length,padding)[:length]
                        ValidCounter[k] = ValidCounter[k] - 1
                        if ValidCounter[k] == -1:
                            ValidCounter[k] = len(TotalValidFields[k]) - 1

                else:
                    spaces2=' '*length
                    toprint2+=spaces+spaces2
            if Trailer:
                global TrailerText
                toprint3+= TrailerText
            global HeaderDone
            global TrailerDone
            if Header and not HeaderDone:
                HeaderDone=True
                Headerlessprint=toprint2+toprint3
                filepath2=filepath+'/Header'
                if not os.path.exists(filepath2):
                    os.mkdir(filepath2)
                filename2=filepath2+'/Headerless'
                file=open(filename2,'w')
                file.write(Headerlessprint)
                file.close()
            if Trailer and not TrailerDone:
                TrailerlessPrint=toprint1+toprint2
                filepath3=filepath+'/Trailer'
                if not os.path.exists(filepath3):
                    os.mkdir(filepath3)
                filename3=filepath3+'/Trailerless'
                file=open(filename3,'w')
                file.write(TrailerlessPrint)
                file.close()
                TrailerDone=True
            toprint=toprint1+toprint2+toprint3
            file=open(filename1,'w')
            file.write(toprint)
            file.close()

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
        if MandatoryFieldNumber in InvalidFieldNumbers:
            InvalidValuesLength=len(TotalInvalidFields[MandatoryFieldNumber])
        else:
            InvalidValuesLength=0
        for count in range(0,InvalidValuesLength):
            toprint=''
            filename1 = fileDirectory1 +  '//' +str(count+1)
            if Header:
                global HeaderText
                toprint+= HeaderText
            for j in sorted(StartList):
                padding=' '
                if str(j) in PaddingFields:
                    padding='0'
                length = 0
                spaces = ''
                if sorted(StartList).index(j) != 0:
                    previousEnd = sorted(StartList)[sorted(StartList).index(j) - 1]
                    if j - int(EndingPosition[previousEnd]) == 1:
                        length = int(EndingPosition[j]) - int(j) + 1
                    else:
                        length2 = j - int(EndingPosition[previousEnd])
                        spaces = ' ' * (length2 - 1)
                        length = int(EndingPosition[j]) - int(j) + 1
                else:
                    length = int(EndingPosition[j]) - int(j) + 1
                if j==MandatoryFieldNumber:
                    toprint+=spaces+str(TotalInvalidFields[j][count]).ljust(length,padding)[:length]
                else:
                    if j in ValidFieldNumbers:
                        toprint+=spaces+str(TotalValidFields[j][0]).ljust(length,padding)[:length]
                    else:
                        spaces2=' '*length
                        toprint+=spaces+spaces2
            if Trailer:
                global TrailerText
                toprint += TrailerText
            file=open(filename1,'w')
            file.write(toprint)
            file.close()



def BlankRecord(Header, Trailer,MandatoryFields,TotalValidFields,RequiredFieldFlag,RequiredFieldList):

    for k in  MandatoryFields:
        Count = 1
        if RequiredFieldFlag:
            RequiredFieldNumber=str(FieldsWithNumbers[i])
            if not RequiredFieldList.__contains__(RequiredFieldNumber):
                continue
        ClearedFieldName=RemoveSpaces(k)
        fileDirectory=filepath + '//' + str(ClearedFieldName)
        if not os.path.exists(fileDirectory):
            os.mkdir(fileDirectory)
        fileDirectory1=fileDirectory+'//BlankRecords'
        if not os.path.exists(fileDirectory1):
            os.mkdir(fileDirectory1)
        filename1=fileDirectory1+'//'+ str(Count)
        Count=Count+1
        toprint=''
        if Header:
            global HeaderText
            toprint+=HeaderText
        for i in sorted(StartList):
            padding=' '
            if str(i) in PaddingFields:
                padding='0'
            length = 0
            spaces = ''
            if sorted(StartList).index(i) != 0:
                previousEnd = sorted(StartList)[sorted(StartList).index(i) - 1]
                if i - int(EndingPosition[previousEnd]) == 1:
                    length = int(EndingPosition[i]) - int(i) + 1
                else:
                    length2 = i - int(EndingPosition[previousEnd])
                    spaces = ' ' * (length2 - 1)
                    length = int(EndingPosition[i]) - int(i) + 1
            else:
                length = int(EndingPosition[i]) - int(i) + 1

            if int(i) != int(MandatoryFields[k]):
                if i in ValidFieldNumbers:
                    toprint+=spaces+str(TotalValidFields[i][0]).ljust(length,padding)[:length]
                else:
                    spaces2=' '*length
                    toprint+=spaces+spaces2
            else:
                spaces2=' '* length
                toprint+=spaces+spaces2
        if Trailer:
            global TrailerText
            toprint+=TrailerText
        file=open(filename1,'w')
        file.write(toprint)
        file.close()

Header = False
Trailer = False
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

HeaderDone = False
TrailerDone = False

Position=True
Position=parser.getboolean('Definition','EndingPosition')

File=open(ReadFilePath,'r')
ListofRecords=File.readlines()
Headers=ListofRecords[0].strip().split('\t')
StartPositions=ListofRecords[2].split('\t')
Endorlength=ListofRecords[3].split('\t')

FieldRange={}
Traverse=0

for i in StartPositions:
    if i=='':
        logger.warning(f'Starting Position is not mentioned for "{Headers[Traverse]}"')
        exit()
    if Endorlength[Traverse]=='':
        logger.warning(f'Ending Position is not mentioned for "{Headers[Traverse]}"')
        exit()
    if Position:
        m=int(Endorlength[Traverse])
    else:
        addinglength = Endorlength[Traverse]
        m = int(i) + int(addinglength)-1
    for k in range(int(i),m+1):
        try:
            if FieldRange[k]==True:
                logger.warning(f'Field Range for {Headers[Traverse]} is already covered in other field range')
                exit()
        except KeyError:
            FieldRange[k]=True
    Traverse+=1


StartingPosition={}
StartList=[]
EndingPosition={}
FieldsWithNumbers={}
MandatoryFields={}
FieldNumbers=set()
FieldPossibleValues={}
TotalValidFields={}
ValidCounter={}
TotalInvalidFields={}
ValidFieldNumbers=[]
InvalidFieldNumbers=[]
InvalidCounter={}
PaddingFields=parser.get('Definition','paddingfields').split(',')
EmployeeFieldValue=str(parser.get('Definition','EmployeeFieldValue'))
logger.info(f'Employee Field Value is {EmployeeFieldValue}')

SeparateHeader = False
SeparateTrailer = False
HeaderText='Header'+'\n'
TrailerText='\n'+'Trailer'
SeparateHeader = parser.getboolean('Definition', 'SeparateHeader')
SeparateTrailer = parser.getboolean('Definition', 'SeparateTrailer')

if Header and SeparateHeader:
    DefaultHeaderPath = parser.get('Definition', 'DefaultHeaderPath')
    try:
        HeaderFile = open(DefaultHeaderPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultHeaderPath "{DefaultHeaderPath}" is not proper\n Check the FilePath')
        exit()
    HeaderText = HeaderFile.readline().strip()

if Trailer and SeparateTrailer:
    DefaultTrailerPath = parser.get('Definition', 'DefaultTrailerPath')
    try:
        TrailerFile = open(DefaultTrailerPath, 'r')
    except FileNotFoundError:
        logger.error(f'DefaultTrailerPath "{DefaultTrailerPath}" is not proper\n Check the FilePath')
        exit()
    TrailerText = TrailerFile.readline().strip()

df = pd.read_csv(ReadFilePath, sep='\t', dtype=str)
for toprow in Headers:
    ColumnList = df[toprow].values.tolist()
    mandatory = True
    StartingPoint = True
    PositionDone=True
    RealColumnList=[]
    for i in ColumnList:
        if str(i) == 'nan':
            if mandatory:
                logger.warning(f'The mandatory status for the field "{toprow}" is not mentioned:')
                InputMandatory = input('Enter the Status with ' + '"Y" or ' + '"N":')
                IsMandatoryField = MandatoryCheck(InputMandatory, i)
                try:
                    start = int(str(ColumnList[1]))
                except ValueError:
                    start = int(input('Please Give the Starting Field Number for ' + toprow + ' :'))
                try:
                    end=int(str(ColumnList[2]))
                except ValueError:
                    end= int(input('Please Give the Ending Field Number for ' + toprow + ' :'))
                FieldNumbers = FieldChecker(start, FieldNumbers)
                if IsMandatoryField:
                    MandatoryFields[toprow] = start
                FieldsWithNumbers[toprow] = start
                mandatory = False
            else:
                continue
        elif mandatory:
            IsMandatoryField = MandatoryCheck(i, toprow)
            try:
                start = int(str(ColumnList[1]))
            except ValueError:
                start = int(input('Please Give the Starting Field Number for ' + toprow + ' :'))
            try:
                end = int(str(ColumnList[2]))
            except ValueError:
                end = int(input('Please Give the Ending Field Number for ' + toprow + ' :'))
            FieldNumbers = FieldChecker(start, FieldNumbers)
            if IsMandatoryField:
                MandatoryFields[toprow] = start
            FieldsWithNumbers[toprow] = start
            mandatory = False
        elif StartingPoint:
            StartingPoint = False
            continue
        elif PositionDone:
            PositionDone=False
            continue
        else:
            RealColumnList.append(i)
    FieldPossibleValues[toprow] = RealColumnList
    StartingPosition[start]=RealColumnList
    if Position:
        EndingPosition[start]=end
    else:
        positionnum=start+end-1
        EndingPosition[start]=positionnum
    StartList.append(start)
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
        TotalValidFields[start] = ValidtopRow
        ValidFieldNumbers.append(start)
        ValidCounter[start] = len(ValidtopRow) - 1
    if len(InvalidtopRow) >= 1:
        TotalInvalidFields[start] = InvalidtopRow
        InvalidCounter[start] = len(InvalidtopRow) - 1
        InvalidFieldNumbers.append(start)


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
    logger.warning(f'In order to avoid the overiding of basic info to existing upin,Please give more valid SSNs around {RequiredSSNNumber}')

print("These are the Fields for your ETL:\n")
print("{:>36} {:>10} {:>10}".format('FieldName', 'FieldNumbers', 'MandatoryStatus'))

for k in sorted(StartList):
    value = MandatoryFields.__contains__(GetFieldName(k))
    if value:
        status = 'True'
    else:
        status = 'False'
    print("{:>36}{:>5}-{:<5} {:>10}".format(GetFieldName(k), k,EndingPosition[k],status))



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
