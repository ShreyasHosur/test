from script import *
from writer import *


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
