from script import *
from writer import *

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