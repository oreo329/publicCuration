#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Python Code for AgitCura system being installed at Garage by Agit @HyojaMarket
# For images uploaded at specific folder at HVR 115
# Client PC at Garage by Agit download and play the images of from the HVR 115

from __future__ import print_function

import dropbox
import argparse
import contextlib
import os,shutil
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Sync Dropbox/App/AgitCura/CuraImages to ~/Desktop/AgitCura')

parser.add_argument('sourcedir', nargs='?', default='CuraImages',
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/Downloads',
                    help='Local directory to download')
parser.add_argument('desktopdir', nargs='?', default='~/Desktop',
                    help='Local directory to download #2')

###########  Download files from dropbox
#define functions
def list_folder(dbx, folder, subfolder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')

    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumped empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv
def download(dbx, local_folder, source_folder , subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    local_path = '/%s/%s/%s' % (local_folder, subfolder.replace(os.path.sep, '/'), name)
    source_path = '/%s/%s/%s' % (source_folder, subfolder.replace(os.path.sep, '/'), name)

    while '//' in source_folder:
        source_folder = source_folder.replace('//', '/')

    while '//' in local_path:
        local_path = local_path.replace('//', '/')

    print (local_path)
    print (source_path)

    with stopwatch('download'):
        try:
            md, res = dbx.files_download(local_path,source_path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data
@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))
def pathNameCreation (path):
    while '//' in path:
        path = path.replace('//', '/')
    return  path
def searchPath(folderN):
    metaData = dbx.files_list_folder('/'+folderN).entries
    subfolderlist = []
    curFileNArr = []

    for entry in metaData:
        if len(entry.name.split('.')) == 1: #folder
            subfolderlist.append(entry.name)

        elif len(entry.name.split('.')) == 2:
            curFileNArr.append(entry.name)

    return subfolderlist, curFileNArr

# Access to the Token & Confirm the Account
myToken = 'NyT0Y0HzOuIAAAAAAAA75ayFvsIZyxY19cuL0uH_jkkRZgXuloFNyqRjtvUDUWyS'
dbx = dropbox.Dropbox(myToken)
print(dbx.users_get_current_account())

# Check the folders in side the app
for entry in dbx.files_list_folder('').entries:
    if entry.name == "CuraImages":
        adimage_folder_name = entry.name
    #print(entry.name)

## upload & check metadata of Readme.txt
# dbx.files_upload("This folder is to provide source images of the AgitCura which is rear-projection on window at Garage by Agit", '/CuraImages/Readme.txt')
print(dbx.files_get_metadata('/CuraImages/Readme.txt').server_modified)

# Check the files in AgitCuraImages Folder
# for entry in dbx.files_list_folder('/'+adimage_folder_name).entries:
#    print (entry.name)

# Set Dir Pathes and change WD
args = parser.parse_args()

source_dirN = args.sourcedir #pathname
root_dir = os.path.expanduser(args.rootdir) #path
desktop_dir = os.path.expanduser(args.desktopdir) #path
os.chdir(desktop_dir)
#print(os.getcwd())

#Create local curation dir & delete previous version of the local CuraImgaes Path
local_dirN = 'CuraImages'
if not os.path.exists(local_dirN):
    os.mkdir(local_dirN)
else:
    shutil.rmtree(os.getcwd()+'/'+local_dirN)
    os.mkdir(local_dirN)

localCuraImagesPath = os.getcwd() + '/'+ local_dirN +'/'

#App Dropbox souce path endswith "/"
dropboxSourcePath = '/Users/Seungjae/Dropbox/앱/AgitCura/'+ source_dirN +'/'
#os.chdir(dropboxSourcePath)

#print(os.path.exists('Readme.txt')) #Check wether the dropbox path is source path
#dbx.files_download_to_file(dropboxSourcePath, localCuraImagesPath)

#print (dbx.files_list_folder('/'+source_dirN).entries)
#print (dbx.files_list_folder('/'+source_dirN,recursive=True))
#a = dbx.files_list_folder('/'+source_dirN).entries
#print ( len(a[0].name.split('.') ))

root_subfolderList, root_fileList = searchPath(source_dirN)
#print(searchPath('/'+source_dirN+'/'+root_subfolderList[0]))
#root_subfolderList.append()
#print (root_fileList[0])

#print (root_fileList[0].endwith('.txt'))

def downloadCura(pathN, pre_path):

    path_subfolderList, path_fileList = searchPath(pathNameCreation(pre_path+'/'+pathN) )

    print('Descending into', pathN, '...')
    print('pre_path ', pre_path, '...')
    print(path_subfolderList,path_fileList)

    for name in path_fileList:

        os.chdir(desktop_dir+pre_path)
        print(name)

        if not os.path.exists(pathN) and not len(pathN) == 0:
            # 로컬에 저장시에 서브폴더에 들어가지 않고 루트에 모든이미지를 저장
            os.mkdir(pathN)
            print((os.getcwd()))

        #if not name.startswith('.') and not name.endswith(".txt"):
        #CuraImage가 폴더명에 중복되어서 제거
        local = pathNameCreation(localCuraImagesPath[:(len(localCuraImagesPath)-len('curaImages/'))] + '/' + pre_path +'/'+ pathN+ '/'+ name)
        source = pathNameCreation('/' + pre_path + '/' + pathN + "/" + name)
        print(local, source)

        dbx.files_download_to_file(local, source)

    if len(path_subfolderList) == 0:
        print("end of subfolders")

    else:
        for entry in path_subfolderList:

            pre_pathNew = pre_path+'/'+pathN+'/'
            print(pre_pathNew)
            downloadCura(entry, pre_pathNew)

downloadCura(source_dirN,'')





#    elif dn != []:

      #  for sub_dn, files in searchPath(dn):



'''
#download
for dn, dirs, files in os.walk(dropboxSourcePath):
    subfolder = dn[len(dropboxSourcePath):].strip(os.path.sep)
    print ("dn ", dn," dn2 " , dn[len(dropboxSourcePath):], ' dn3 ', subfolder )
    print (dirs)
    print (files)
    listing = list_folder(dbx, source_dirN, subfolder)
    #print('Descending into', subfolder, '...')

    os.chdir(localCuraImagesPath)
    if not os.path.exists(subfolder) and not len(subfolder) == 0 :
        #로컬에 저장시에 서브폴더에 들어가지 않고 루트에 모든이미지를 저장
        #os.mkdir(subfolder)
        os.listdir(os.getcwd())

    print(files)
    # print (dn, dirs,files)
    for name in files:
        fullname = os.path.join(dn, name)
        if not isinstance(name, six.text_type):
            name = name.decode('utf-8')
        nname = unicodedata.normalize('NFC', name)
        if not name.startswith('.') and not name.endswith(".txt") :

           #download(dbx, localCuraImagesPath ,source_dir, subfolder, name)

           local = pathNameCreation(localCuraImagesPath+'/'+name)
           #로컬에 저장시에 서브폴더에 들어가지 않고 루트에 모든이미지를 저장
           #local = pathNameCreation(localCuraImagesPath + '/' + subfolder + "/" + name)
           source = pathNameCreation('/'+source_dirN+'/'+subfolder+"/"+name)
           print(local, source)

           dbx.files_download_to_file(local, source)


#load image displaying module
for dn, dir, files in os.walk(localCuraImagesPath):

    #for name in files:
        imageN = files[1]
        os.chdir(localCuraImagesPath)
        image = Image.open(imageN)
        image.show()
        time.sleep(2)
        image.close()

'''