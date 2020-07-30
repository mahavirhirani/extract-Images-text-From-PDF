#!/usr/bin/python

import fitz
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import json
import re
import io
import PIL.Image as Image
import traceback


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='test1',
                                         user='root',
                                         password='')
    if connection.is_connected():
        records_to_insert = []
        pdf_document = fitz.open("./pdf/marcas2572.pdf")
        current_Date = datetime.now()
        outputFileDir = "./pdf/Output/" + current_Date.strftime('%Y-%m-%d_%H-%M-%S')
        os.mkdir(outputFileDir)
        regex = "^ *\d[\d ]*$"

        recored_id=[]
        imageData=[]

        print(pdf_document.getPageImageList(192))
        exit()
        for current_page in range(len(pdf_document)):
            if (len(pdf_document.getPageImageList(current_page)) > 0 ):
                recored_exsit = 0
                pg = pdf_document.loadPage(current_page)
                text = pg.getText('JSON')
                jsondata = json.loads(text)
                for pdfdata in jsondata['blocks']:
                    if pdfdata['type'] == 0 :
                        value = re.search(regex, pdfdata['lines'][0]['spans'][0]['text'])
                        if value != None :
                            recored_id.append(value.string)
                            recored_exsit = 1
                    elif pdfdata['type'] == 1 and recored_exsit == 1:
                        imageData.append(pdfdata['image'])
        
        print(len(recored_id))
        print(len(imageData))
        exit()
        for val in recored_id:
            outputFileName = outputFileDir + "/%s.png" % (
                        val)
            with open(outputFileName, "wb") as fh:
                fh.write(imageData[recored_id.index(val)].decode('base64'))
            records_to_insert.append((outputFileName, current_Date))    

        mySql_insert_query = """INSERT INTO pdf_images (path, datetime) 
                           VALUES (%s, %s) """
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
except Exception:
    traceback.print_exc()
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
