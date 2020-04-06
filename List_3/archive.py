import os
import argparse
from datetime import datetime, timedelta

windows = True

parser = argparse.ArgumentParser(description='Archive any number of text files into one.')



def archive_files(path_list):
    arch_path = path_list[-1]
    if os.path.exists(arch_path):
        print("Archive of this name already exists. Pass path to archive that doesn't exist.")
        return
    if os.path.basename(arch_path).split(".")[-1] != "txt":
        raise ValueError("'.txt' shoud be at the and of the last path")
    for path in path_list[:-1]:
        if not os.path.exists(path):
            raise ValueError(f"The path of this name doesn't exist.\n{path}")
    with open(arch_path, 'a') as ar:
        for file in path_list[:-1]:
            with open(file, 'r') as fl:
                ar.write(f"File_name: {os.path.basename(file)}\n{'#'*20}\n")
                for line in fl.readlines():
                    ar.write(line)
                ar.write(f"\n{'#'*20}\n\n")

    "New archive has been created!"

def unarchive_files(path_list):
    arch_path = path_list[0]
    if os.path.basename(arch_path).split(".")[-1] != "txt":
        raise ValueError("Archive file should be of '.txt' format")
    if len(path_list)==1:
        path_list.append(os.path.dirname(arch_path))
    directory = path_list[1]
    with open(arch_path) as ar:
        lines = ar.readlines()
        starts = [lines.index(x) for x in lines if x.startswith("File_name: ")]
        for i in starts:
            f_name = lines[i][11:lines[i].index(".txt")+4]
            with open(os.path.join(directory, f_name), 'a') as new_file:
                k = i + 2
                while True:
                    if lines[k].startswith("#####"):
                        break
                    new_file.write(lines[k])
                    k += 1


def backup(format, directory, windows=windows):
    os.chdir(os.path.dirname(os.path.abspath(directory)))
    if directory.endswith("/"):
        directory = directory[:-1]
    copy_comand = "cp"
    if windows:
        copy_comand = "copy"
    backup_directory = "Backup/copy-"+str(datetime.now().date())
    if not os.path.exists(backup_directory):
        if not os.path.exists("Backup"):
            os.mkdir("Backup")
        os.mkdir(backup_directory)
    today = datetime.now()
    for path, dir, files in os.walk(os.path.basename(directory)):
        for element in files:
            file_path = os.path.join(path, element)
            if element.endswith("." + format) and (datetime.fromtimestamp(os.path.getmtime(file_path)) + timedelta(days=3)>today):
                os.popen(f"{copy_comand}  '{file_path}' '{os.path.join(backup_directory, element)}'")

def endlines(directory, transformation):
    if directory.endswith("/"):
        directory = directory[:-1]
    os.chdir(os.path.dirname(os.path.abspath(directory)))
    if directory.endswith(".txt"):
        with open(os.path.basename(directory)) as dl:
            text = dl.read()
            if transformation == "unix_to_wind":
                text = text.replace("\n", "\r\n")
            elif transformation == "wind_to_unix":
                text = text.replace("\r\n", "\n")
        with open(os.path.basename(directory), "w") as am:
            am.write(text)
    else:
        for path, dirs, files in os.walk(os.path.basename(directory)):
            print(files, path, dir)
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(path, file), "r") as fl:
                        text =  fl.read()
                        if transformation == "unix_to_wind":
                            text = text.replace("testowanie", "costm")
                        elif transformation =="wind_to_unix":
                            text = text.replace("\r\n", "\n")

                    with open(os.path.join(path, file), "w") as wr:
                        wr.write(text)


parser.add_argument('--mode', metavar='Program_mode', type=str, nargs=1, help="Choose one mode of program: (archive, unarchive, backup, endlines_unix(change endlines from unix to windows), "
                                                                              " endlines_windows(change endlines from windows to unix)")
parser.add_argument('--archive_paths', metavar='archive_paths', type=str, nargs='+',
                        help='Firtly you should pass paths to the files that are to be archived, then pass the path to'
                             ' location of archive. Remember about name of file in the last path!'
                             ' Use only with --mode archive!')
parser.add_argument('--unarchive_paths',  metavar="unarchive_paths", type=str, nargs=2,
                    help="Pass as a argument path to archive file and directory, where texts files are to save."
                         "  Use only with --mode unarchive!")



parser.add_argument('--backup_paths', metavar='Backup_paths', type=str, nargs=1, help='Pass path to the folder where files are located.  Use only with --mode backup!')

parser.add_argument('--format', metavar='Format', nargs="+",type=str, help="Specify what kind of files you want to backup.  Use only with --mode archive!")
parser.add_argument('--unix_to_wind', metavar='endlines', type=str, nargs=1,
                        help='Pass path to the folder where you want to change endlines from unix systems to windows')
parser.add_argument('--wind_to_unix', metavar='endlines', type=str, nargs=1,
                        help='Pass path to the folder where you want to change endlines from unix systems to windows')

args = parser.parse_args()
if args.mode is None:
    raise ValueError("Please pass --mode argument.")
elif args.mode[0]=='archive':
    if len(args.archive_paths) >= 2:
        archive_files(args.archive_paths)
    else:
        raise ValueError("--archive_paths must consist of at least 2 arguments.")
elif args.mode[0]=='unarchive':
    if len(args.unarchive_paths) == 2:
        unarchive_files(args.unarchive_paths)
    else:
        raise ValueError("--unarchive_paths must consist of 2 arguments. Firsly archive file, and then directory, where texts are to save.")

elif args.mode[0]=='backup':
    if args.format is None or args.backup_paths is None:
        raise ValueError("Arguments error. Pass at least one format to --format and path to the folder with files.")
    elif len(args.backup_paths) == 1 and len(args.format)==1:
        backup(args.format[0], args.backup_paths[0])
elif args.mode[0] =="change_endlines":
    if (args.unix_to_wind is None and args.wind_to_unix is None) or (args.unix_to_wind is not None and args.wind_to_unix is not None):
        raise ValueError("Please pass only one of these arguments: --unix_to_wind or --wind_to_unix")
    elif len(args.unix_to_wind) == 1:
        endlines(args.unix_to_wind[0], transformation="unix_to_wind")
    elif len(args.wind_to_unix) == 1:
        endlines(args.wind_to_unix[0], transformation="wind_to_unix")
else:
    raise ValueError("--mode can take only following arguments: archive, unarchive, backup, change_endlines")



print(parser.parse_args())