### MAKE config.py and variables.pyo

import getpass
import os.path
import subprocess
import shutil

from os.path import join, normpath, exists

def answer_yes(Question):

        Input = input(Question + "\t").lower().lstrip()[0]
        if Input == "y":
                return True
        elif Input == "n":
                return False
        else:
                print("yes or no answers only.")
                answer_yes(Question)

with open("variables.py", "w") as variables:
        if answer_yes("Process with installation at /home/{}/.tgsh/ ?".format(getpass.getuser())):
                TGT_DIR = "/home/{}/.tgsh/".format(getpass.getuser())
        else:
                TGT_DIR = input("Please enter the full /path/to/desired/target/directory/ : ")
                TGT_DIR.replace("\ ", " ")
                if not os.path.isdir(os.path.normpath(TGT_DIR)):
                        print(TGT_DIR, "is not a valid directory. Choosing /home/{}/.tgsh".format(getpass.getuser()))
                        TGT_DIR = "/home/{}/.tgsh/".format(getpass.getuser())

        variables.write("PROJECTROOT = \"" + normpath(TGT_DIR)+ "/\"\n")

print("\n----\n")

with open("config.py", "w") as config:
        config.write("EMPLOYER_FIRST_NAME=\"" + (input("Your first name:\t").title() or "User")+ "\"\n")
        config.write("EMPLOYER_LAST_NAME=\"" + (input("Your last name:\t").title() or "User")+ "\"\n")
        config.write("SECRETARY_NAME=\"" + (input("What would you like to call your bot?:\t").title() or "tgsh") + "\"\n")

        if answer_yes("Do you already have both a telegram account and a telegram bot?"):
                config.write("BOT_TOKEN=\"" + input("Enter bot token: ") + "\"\n")
        else:
                if answer_yes("Would you like instructions on setting up an account and a bot?"):
                        print("1. Download and install the app telegram on your smartphone.")
                        print("2. Register and perform necessary setup as instructed by the app.")
                        print("3. [Important!] Go to 'Settings' (swipe from left) and set a unique username.")
                        print("4. [Important!] Search for the user '@BotFather', and send the command /newbot")
                        print("5. [Important!] Follow instuctions from this account and obtain a token.")
                config.write("BOT_TOKEN=\"" + input("Enter bot token: ") + "\"\n")

        config.write("HOST_USERNAME=\"{}\"\n".format(getpass.getuser()))
        config.write("TG_USERNAME=\"{}\"\n".format(input("Enter *your* telegram username (not your bot's):\t@")))

import config

with open("{}-tgsh.service".format(config.SECRETARY_NAME.lower()), "w") as unit:
        unit.write("[Unit]\n")
        unit.write("Description = {} TGSH Backdoor\n".format(config.SECRETARY_NAME))
        unit.write("\n")
        unit.write("[Service]\n")
        unit.write("ExecStart={} {}\n".format(shutil.which("python3"), join(TGT_DIR, "src", "main.py")))
        unit.write("Environment=PYTHONUNBUFFERED=1\n")
        unit.write("Restart=on-failure\n")
        unit.write("\n")
        unit.write("[Install]\n")
        unit.write("WantedBy=default.target\n")

if exists(TGT_DIR):
        shutil.rmtree(TGT_DIR)
        print("removed that fuck")

try:
        subprocess.run(["mkdir", "-pv", "/home/{}/.config/systemd/user/".format(getpass.getuser())])
except FileExistsError:
        pass

shutil.copy("{}-tgsh.service".format(config.SECRETARY_NAME.lower()), "/home/{}/.config/systemd/user".format(getpass.getuser()))
shutil.copytree(normpath(".."), TGT_DIR)

subprocess.run("systemctl --user start {}-tgsh".format(config.SECRETARY_NAME.lower()).split())
subprocess.run("systemctl --user enable {}-tgsh".format(config.SECRETARY_NAME.lower()).split())
