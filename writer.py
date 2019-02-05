from script import *
import csv

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
