from Positive import *
from Negative import *
from Blank import *
from Invalid import *
from script import *

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