#! /usr/bin/env python
"""
    This utility first unzip all databases from all zip files under the given
    directory, then combine them using the combineEbeDatabases script located
    under ../EBE-Node/EbeCollector. If the target folder for unzipping already
    exists, the database is assumed to be already existed under it and will not
    be unzipped again. Any subfolder generated by this program will be removed;
    existing one will be kept and collections are done from both existing
    subdirectories and from zip files.
"""

from sys import argv, exit
from os import path, listdir, remove, removedirs
from subprocess import call

try:
    parentFolder = path.abspath(argv[1])
except:
    print("Usage: combineEbeDatabases.py parent_folder [database_filename]")
    exit()

# get optional parameters
if len(argv)>=3:
    databaseFilename = argv[2]
else:
    databaseFilename = "collected.db"
    
# loop over subdirectories and extract zip files
toBeDeleted = [] # will remove these directories
for aZipFile in listdir(parentFolder):
    zipFoldername, ext = path.splitext(aZipFile)
    if ext.lower() == ".zip":
        zipFolder = path.join(parentFolder, zipFoldername)
        if path.exists(zipFolder):
            continue
        else:
            toBeDeleted.append(zipFolder) # will be removed afterwards
            commandString = ("unzip %s %s" 
                % (aZipFile, path.join(zipFoldername, databaseFilename)))
            call(commandString, shell=True, cwd=parentFolder)
    elif (ext.lower() == ".bz2" or ext.lower() == '.gz' 
          or ext.lower() == '.tar'):
        zipFoldername = zipFoldername.split('.tar')[0]
        zipFolder = path.join(parentFolder, zipFoldername)
        if path.exists(zipFolder):
            continue
        else:
            toBeDeleted.append(zipFolder) # will be removed afterwards
            commandString = ("tar -xf %s %s" 
                % (aZipFile, path.join(zipFoldername, databaseFilename)))
            call(commandString, shell=True, cwd=parentFolder)
# combine them
print("Combining...")
commandString = "python combineEbeDatabases.py %s" % parentFolder
call(commandString, shell=True, cwd="../EBE-Node/EbeCollector")

# remove intermediate directories
for aDir in toBeDeleted:
    remove(path.join(aDir, databaseFilename)) # do not use rmtree for safety concern
    removedirs(aDir)
