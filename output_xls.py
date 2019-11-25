import os
from excel.readExistInfo import write_app_addrs


if __name__ == '__main__':
    for root, dirs, files in os.walk(os.path.join('.','2009-2015联合申请专利')):
        for file in files:
            if file[-3:] == 'xls':
                fileName = os.path.join(root, file)
                newFileName = os.path.join(root, '_'+file)
                write_app_addrs(fileName, newFileName)