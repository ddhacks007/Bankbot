import xlrd
import sys
import re

sys.stdout=open("data_model.py","w")

sample = """
from sqlalchemy import BigInteger, Column, DateTime, Integer,SmallInteger, String,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from flask import Flask
from config import params

app = Flask(__name__)
Base = declarative_base()
metadata = Base.metadata
engine = create_engine('mysql://'+params['username']+':'+params['password']+'@'+params['hostname']+':'+params['port']+'/'+params['db'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
"""

print(sample)

path = "/Users/deepak/Downloads/Banking_Bot.xlsx"

workbook = xlrd.open_workbook(path)

worksheet = workbook.sheet_by_name("banking")

model_names = []

row_count = worksheet.nrows
column_count = worksheet.ncols
for i in range(row_count):
    for j in range(column_count):
        # cell value below the cell with header 'Table Name' or 'TABLE_NAME'
        if((worksheet.cell_value(i, j) == "Table Name" 
        and worksheet.cell_value(i+1,j) != "Table Name" 
        and worksheet.cell_value(i+1,j) != "TABLE_NAME")
        or 
        (worksheet.cell_value(i, j) == "TABLE_NAME" 
        and worksheet.cell_value(i+1,j) != "Table Name" 
        and worksheet.cell_value(i+1,j) != "TABLE_NAME")):
            # to define the table class name
            i += 1
            str = worksheet.cell_value(i, j)
            str = str.capitalize()
            while(str.rfind("_") != -1):
                m = re.search("(_([a-z0-9A-Z]))", str)
                if(m):
                    str = str.replace(m.group(1),m.group(2).upper())
            print("class "+str+"(Base):")
            model_names.append(str)
            # to define the table name from class name
            temp = worksheet.cell_value(i, j).lower()
            while(temp.rfind(" ") != -1):
                m = re.search(" ", temp)
                if(m):
                    temp = temp.replace(" ","_")
            print("\t__tablename__ = \'"+ temp +"\'")
            print("\tid = Column(BigInteger, primary_key=True)")
            j += 1
            # finding the datatype of each column in the table
            while(worksheet.cell_value(i, j) != ''):
                if(worksheet.cell_value(i, j+2).lower() == 'bigint'):
                    str = "BigInteger"
                elif(worksheet.cell_value(i, j+2).lower() == 'binary'):
                    str = "BINARY"
                elif(worksheet.cell_value(i, j+2).lower() == 'date'):
                    str = "Date"
                elif(worksheet.cell_value(i, j+2).lower() == 'datetime'):
                    str = "DateTime"
                elif(worksheet.cell_value(i, j+2).lower() == 'decimal' 
                or worksheet.cell_value(i, j+2).lower() == 'decimal(10,2)' 
                or worksheet.cell_value(i, j+2).lower() == 'decimal(10,3)' 
                or worksheet.cell_value(i, j+2).lower() == 'decimal(8,2)'):
                    str = "Float"
                elif(worksheet.cell_value(i, j+2).lower() == 'int'):
                    str = "Integer"
                elif(worksheet.cell_value(i, j+2).lower() == 'numeric' 
                or worksheet.cell_value(i, j+2).lower() == 'numberic'):
                    str = "Numeric"
                elif(worksheet.cell_value(i, j+2).lower() == 'smallint' 
                or worksheet.cell_value(i, j+2).lower() == 'smallt'):
                    str = "SmallInteger"
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar(1)'
                or worksheet.cell_value(i, j+2).lower() == 'char'):  
                    str = "String(1)"  
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar2'
                or worksheet.cell_value(i, j+2).lower() == 'varchar(2)'):
                    str = "String(2)"
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar(5)'):
                    str = "String(5)"
                elif(worksheet.cell_value(i, j+2).lower() == 'password'):  
                    str = "String(50)"
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar'
                or worksheet.cell_value(i, j+2).lower() == 'varchar(100)' 
                or worksheet.cell_value(i, j+2).lower() == 'varchar?'
                or worksheet.cell_value(i, j+2).lower() == 'varchr'):
                    str = "String(100)"
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar(1500)'):
                    str = "String(150)"
                elif(worksheet.cell_value(i, j+2).lower() == 'varchar(3000)'):
                    str = "String(200)"
                else:   
                    str = "String(255)"
                # to find whether the column holds unique value or not
                unique = False
                if(worksheet.cell_value(i, j+3).lower() == 'yes'
                or worksheet.cell_value(i, j+3).lower() == 'yes - individually'
                or worksheet.cell_value(i, j+3).lower() == 'y'):
                    unique = True
                # to find the column name
                temp = worksheet.cell_value(i, j).lower()
                while(temp.rfind(" ") != -1):
                    m = re.search(" ", temp)
                    if(m):
                        temp = temp.replace(" ","_")
                sys.stdout.write("\t"+ temp +" = Column(")
                sys.stdout.write(str)
                if(unique == True):
                    sys.stdout.write(", unique=True")
                print(")")
                if(i+1 < row_count):
                    i += 1
                if(i == row_count-1):
                    break;
            print("\n")

print("Base.metadata.create_all(bind=engine)\n")