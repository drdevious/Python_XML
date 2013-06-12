#! /usr/bi/env python

####################
### DGF 9/5/2013 ###
####################

#########################
### import dei moduli ###
#########################

import os
import re
import csv
import subprocess
import datetime
from datetime import date, timedelta, datetime
import logging
import time
from time import localtime
import tempfile
import sys
import ConfigParser
import shutil
import xml.etree.ElementTree as ET


#########################################
### dichiarazioni costanti simboliche ###
#########################################

PATH_HOME = "/xxx/XXXXXX"
PATH_LOG = PATH_HOME+"/Log"
PATH_WORK = PATH_HOME+"/Work"
PATH_CONFIG = PATH_HOME+"/Config"
CONFIG_FILE = PATH_CONFIG+"/config.cfg"

### definizione dell'oggetto logger che serve a gestire i log ###

SYSTEM_DATE=time.strftime("%Y%m%d")
LOG_FILENAME = PATH_LOG+"/inn_rescue-"+SYSTEM_DATE+".log"
logger = logging.getLogger("inn_rescue-2.0.py")
hdlr = logging.FileHandler(LOG_FILENAME)
FORMAT = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')
hdlr.setFormatter(FORMAT)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

### definizione dell'oggetto parser per la lettura del file di configurazione ###

parser = ConfigParser.ConfigParser()
parser.read(CONFIG_FILE)

############################
### definizione funzioni ###
############################

def ControlConfigFile():
    try:
        f = open(CONFIG_FILE,'r')
        logger.info("Verifica file di configurazione andata a buon fine")
        f.close()
    except IOError:
        logger.error("Il file di configurazione non esiste, verificare. Esco!")
        sys.exit()

def FileXmlInput():
    tree = ET.parse(PATH_WORK+"/xml_tmp.xml")
    root = tree.getroot()

    for elem in tree.getiterator():
        #print elem.tag

        if elem.tag.find('Username') > 0:
            if elem.tag.find('UsernameToken') < 0:
                usernameXml = elem.text
                #print usernameXml

        if elem.tag.find('Password') > 0:
            passwordXml = elem.text

        if elem.tag.find('smartcardNumber') > 0:
            smartcardnumberXml = elem.text

    return usernameXml,passwordXml,smartcardnumberXml


def BuildXmlForInput(username,smartcardnumber):
    tree = ET.parse(PATH_HOME+"/xml_template.xml")
    root = tree.getroot()

    for elem in tree.getiterator():
        if elem.tag.find('Username') > 0:
            if elem.tag.find('UsernameToken') < 0:
               elem.text = username

        if elem.tag.find('smartcardNumber') > 0:
            elem.text = smartcardnumber

    tree.write(PATH_WORK+"/xml_tmp.xml")


def ReadFileXmlDownloaded():
    d_pwd = 'ERRORE'
    d_date = 'ERRORE'

    try:
        tree_a = ET.parse(PATH_WORK+"/curl_result.xml")
        root_a = tree_a.getroot()

        for elm in tree_a.getiterator():
            p12password = elm.get('p12password',default='')
            if p12password != '':
                d_pwd = p12password

            p12data = elm.get('p12data',default='')
            if p12data != '':
                d_date = p12data

        return d_pwd, d_date

    except:
        logger.error("xml malformato")
        d_pwd = 'ERRORE_XML_MALFORMATO'
        d_date = 'ERRORE_XML_MALFORMATO'

        return d_pwd, d_date


def BuildCsvFile(username, serialecertificato, p12password, p12date, file_out):
    out = csv.writer(open(file_out,"a"), delimiter='|',quoting=csv.QUOTE_ALL)
    data = [username, serialecertificato, p12password, p12date]
    out.writerow(data)
    logger.info("Ho scritto sul file output csv : "+username+", "+serialecertificato+", "+p12password)


def StartProcedure(file_in, file_out):
    with open(file_in, 'r') as f:
        reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            username = row[1]
            smartcardnumber = row[0]
            serial = row[2]

            ### Costruisco l'xml da passare a curl prendendo i dati dal file di input ###
            BuildXmlForInput(username,smartcardnumber)

            ### leggo il file xml da passare allo script curl ###
            FileXmlInput()

            ### lancio lo script bash contenente il comando curl ###
            subprocess.call(PATH_HOME+"/curl_command.sh")

            ### leggo il file xml scaricato e prendo le info che mi interessano ###
            d_pwd,d_date = ReadFileXmlDownloaded()

            ### scrivo i dati recuperati su file ###
            BuildCsvFile(username, serial, d_pwd, d_date, file_out)


def Main():
    for name_section in parser.sections():
           StartProcedure(parser.get(name_section,'path_file_input'),parser.get(name_section,'path_file_spool'))

############
### main ###
############

if __name__ == "__main__":
    ControlConfigFile()
    Main()
