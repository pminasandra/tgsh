# tgsh-0.1

## Context
Ever been away from your computer, and had a life-threatening emergency that required a file from your PC to solve? Ever been paranoid about whether anyone else is using your desktop? Wish you had some quick and secure way of accessing your computer through your phone?

`tgsh` provides a cool way of accessing the contents of your computer securely from anywhere in the world. All you need is your phone and the free app [Telegram](https://telegram.org/) and is implemented using [python-telegram-bot](https://python-telegram-bot.org/). `tgsh`, which stands for _telegram shell_, provides a clean and secure basic interface for your laptop through a chatting app!

## Installation
The installation process for this bit of code is very simple:

### On your phone
* Install the app Telegram.
* Set up your account, and in _Settings_, create a unique username for yourself.
* Contact the user `@BotFather` to create a bot and obtain a unique token. This bot will serve as your \`secretary' on your computer.

### On your PC
**Note:** This software currently only works with Linux systems. It can easily be ported to other OSes, and you are welcome to do so.

* I assume that you have a python-3.5+ installation ready on your system.
* Install necessary python modules.
  ```
  sudo apt-get install python3-pip
  pip3 install numpy
  pip3 install opencv-python
  pip3 install python-telegram-bot
  ```
* Now clone this repo using `git clone git://github.com/pminasandra/tgsh`.
* Enter the `src` directory using `cd tgsh/src`.
* Type the command `make` for automatic complete installation.

## Usage
As of now, the functionality of this software is limited. This is not because it is difficult to code, but because of privacy concerns. Soon (sometime in the next twenty years), a new version of this software that uses linux file permissions to restrict access to particular files will be updated on this repo.

Here is a list of available commands. Send them to the bot you created after finishing the installation procedure.
* `/start`: Greets you, declares its own name, and sets up a prompt string.
* `/cd`: Usual navigation between directories. Use \ for directories with spaces.
* `/ls`: Prints contents. Also supports wildcard expansions. E.g. `/ls ../*.mp3` lists all mp3 files in the parent directory.
* `/get`: Sends appropriate files to you. Files need to be small enough, and you need to have read permissions. Wildcard expansion works.
* `/pic`: Takes a picture with your web-cam and sends it to you.
