import os
from os.path import exists, isdir, islink, join, normpath, basename
import config
import glob

BOT_ROOT = "/home/{}/".format(config.HOST_USERNAME)
BOT_CWD = BOT_ROOT

def pstring():
        return "{}@{}:$ ".format(config.HOST_USERNAME, BOT_CWD)

def hr_file_size(filename):
        Prefixes = ['K', 'M', 'G', 'T', 'E', 'P', 'Y']
        size_in_bytes = os.path.getsize(filename)

        if size_in_bytes <= 1023:
                return str(size_in_bytes)
        else:
                for Prefix in Prefixes:
                        size_in_bytes /= 1024
                        if size_in_bytes < 1024:
                                return "{:3.1f} {}".format(size_in_bytes, Prefix)
                return "{:3.1f}".format(size_in_bytes)+" Y"

def change_dir(path):
        path = path.replace("\ ", " ")
        global BOT_CWD
        if path[0]=="/":
                if exists(path):
                        if isdir(path):
                                if os.access(path, os.X_OK):
                                        BOT_CWD = path
                                else:
                                        return "cd: You cannot access {}: Permission denied.".format(path)
                        else:
                                return "cd: Cannot access {}: Not a directory.".format(path)
                else:
                        return "cd: Cannot access {}: No such file or directory..".format(path)
        else:
                prospective_path = normpath(join(BOT_CWD, path))
                if exists(prospective_path):
                        if isdir(prospective_path):
                                if os.access(prospective_path, os.X_OK):
                                        BOT_CWD = prospective_path
                                else:
                                        return "cd: You cannot access {}: Permission denied.".format(prospective_path)
                        else:
                                return "cd: Cannot access {}: Not a directory.".format(prospective_path)
                else:
                        return "cd: Cannot access {}: No such file or directory.".format(prospective_path)
        return "You are now in "+BOT_CWD


def ls(*paths):
        ret_str = ""
        if not paths:
                Paths = [BOT_CWD]
        else:
                Paths = []
                for Path in paths:
                        if Path[0] == "/":
                                Paths.extend(glob.glob(Path))
                        else:
                                Paths.extend(glob.glob(normpath(join(BOT_CWD, Path))))
        if len(Paths) == 0:
                for Path in paths:
                        ret_str += "ls: cannot access {}: no such file or directory\n".format(Path)
                return ret_str

        for Path in Paths:
                CNT = 1
                ret_str += "\n"
                ret_str += Path
                ret_str += " (" + hr_file_size(Path) +")"
                if isdir(Path):
                        ret_str += "/:\n"
                        if os.access(Path, os.R_OK):
                                for File in os.listdir(Path):
                                        if isdir(join(Path, File)):#FIXME MAKING DIRECTORIES DIFFERENTLY FORMATTED
                                                ret_str += "{}. <b><u>{}/</u></b> ({})\n".format(CNT, basename(File), hr_file_size(join(Path, File)))
                                        else:
                                                ret_str += "{}. {} ({})\n".format(CNT, basename(File), hr_file_size(join(Path, File)))
                                        CNT += 1
                        else:
                                ret_str += "ls: cannot stat {}: Permission denied.".format(Path)
                ret_str += "\n"
        return ret_str
       
def get(*paths):
        ret_str = ""
        full_file_names = []
        CNT = 1
        if not paths:
                Paths = [BOT_CWD]
        else:
                Paths = []
                for Path in paths:
                        if Path[0] == "/":
                                Paths.extend(glob.glob(Path))
                        else:
                                Paths.extend(glob.glob(normpath(join(BOT_CWD, Path))))
        if len(Paths) == 0:
                for Path in paths:
                        ret_str += "\nget: cannot access {}: no such file or directory.\n".format(Path)

        for Path in Paths:
                ret_str += "\n"
                if  not os.access(Path, os.R_OK):
                        ret_str += "\nget: cannot send {}: Permission denied\n".format(basename(Path))
                else:
                        if isdir(Path):
                                ret_str += "\nget: cannot send {}: is a directory.\n".format(basename(Path))
                        else:
                                if os.path.getsize(Path) > 50*1024*1024:
                                        ret_str += "get: cannot send {}: file is too large.".format(basename(Path))
                                else:
                                        full_file_names.append(Path)
                                        ret_str += "{}. get: sending {}\n".format(CNT, basename(Path))
                                        CNT += 1
        return ret_str, full_file_names
