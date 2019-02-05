from script import *
from writer import *

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