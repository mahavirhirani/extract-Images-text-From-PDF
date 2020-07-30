#!/usr/bin/python

import fitz
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os


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
        for current_page in range(1,len(pdf_document)):
            

            
            for image in pdf_document.getPageImageList(current_page):
                pg = pdf_document.loadPage(192)
                text = pg.getText('JSON')
                print(text)
                exit()
                xref = image[0]
                print(xref)
                exit()
                pix = fitz.Pixmap(pdf_document, xref)
                outputFileName = None
                if pix.n < 5:        # this is GRAY or RGB
                    outputFileName = outputFileDir + "/page%s-%s.png" % (
                        current_page, xref)
                    pix.writePNG(outputFileName)
                else:                # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    outputFileName = outputFileDir + "/page%s-%s.png" % (
                        current_page, xref)
                    pix1.writePNG(outputFileName)
                    pix1 = None
                pix = None
                
                records_to_insert.append((outputFileName, current_Date))

        mySql_insert_query = """INSERT INTO pdf_images (path, datetime) 
                           VALUES (%s, %s) """
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
