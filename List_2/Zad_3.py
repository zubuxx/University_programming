import zipfile
import os
from datetime import datetime

def archive_folders(folders,
                    archive_path: str=os.environ['HOME'] + '/Archives',
                    default_directory: str= os.environ['HOME'],
                    arch_name: str=''
                    ):
    '''
    Creates archive of folders passed as a list or string in zip fromat. User can change current working path by passing 'default_directory' argument
    E.g To create an archive for folders located in Desktop and named 'Folder1' and 'Folder2' with all contents we can call function in this way:
    archive_folders(['Folder1', 'Folder2'], default_directory = '/Users/User_name/Desktop', arch_name = 'Folder1)
    The archive file will be saved in /Users/User_name/Archives. (By default!)


    :param folders: list or str
    ------------------------
    List of folders we want to create a copy as a zip file.
    It can be passed as a string, if there is only 1 folder.

    :param arch_path: str
    ------------------------
    It's the location of new archive file passed as a path.
    (/Users/User_name/Archives by default)


    :param default_directory: str
    ------------------------
    We can change current working directory by passing default_directory paramter.
    (/Users/User_name by default)

    :param arch_name: str
    ------------------------
    Name of archive file behind the date.



    :return:
    '''
    folders = [folders]
    os.chdir(default_directory)
    if archive_path[-1]=='/': archive_path = archive_path[:-1]
    if not os.path.exists(archive_path):
        os.mkdir(archive_path)
    time = datetime.now()
    time = time.strftime('%Y-%m-%d %H:%m')
    arch_path = archive_path + '/'
    if default_directory[-1]!= '/': default_directory = default_directory + '/'
    with zipfile.ZipFile(arch_path + time + arch_name + '.zip', mode='w') as myzip:
        for name in folders:
            for path, dirs, files in os.walk(name):
                print(path, dirs, files)
                myzip.write(path)
                for file in files:
                    myzip.write(path + '/' + file)




