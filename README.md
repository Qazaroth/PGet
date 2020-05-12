# PGet
Python port for [BGet](https://github.com/jahwi/bget), at least that was the main idea... You can run the
files either through the batch files provided or your own command prompt.

Python Version Used: **3.8**

Get Python here: https://www.python.org/downloads/

## CMD:
![Pget screenshot](https://github.com/Qazaroth/pget-list/blob/master/images/screenshot1.png)

## Table of Contents
1. [Introduction](https://github.com/Qazaroth/PGet/blob/master/README.md#introduction)
2. [Features](https://github.com/Qazaroth/PGet/blob/master/README.md#features)
3. [Running PGet](https://github.com/Qazaroth/PGet/blob/master/README.md#running-pget)
4. [Bugs & Fixes](https://github.com/Qazaroth/PGet/blob/master/README.md#bugs-and-fixes)
5. [Switches](https://github.com/Qazaroth/PGet/blob/master/README.md#switches)
6. [Contact](https://github.com/Qazaroth/PGet/blob/master/README.md#contact)

## Introduction
PGet is essentially just a python port for BGet, but now, it's BGet but for Python. It's a tool for handling Python
scripts and files. It is built to help script writers and users alike to easily download, update and remvoe scripts.

## Features
1. Download scripts from the PGet server: The scripts are vetted and sorted by us. As of now, the selection are few but
if you want to add your scripts, do contact us at [here](https://github.com/Qazaroth/PGet/blob/master/README.md#contact).
2. Update scripts: Instead of manually re-downloading the latest version of every script, PGet handles that for you.
Just run `-get "SCRIPT_NAME"` and it'll update the script for you if you already have it downloaded.
3. Easily remove scripts: Don't like a script you downloaded? Easily remove it with PGet! All it takes is just one
command line!
5. Update feature: PGet also updates itself or at least checks for new updates so that you are always up-to-date.

## Running PGet
For Windows Users: You can use the batch files provided <br>
For Non-Windows Users: I'm not sure...

Here's an example:

Fetching a script named `test` from the server. The easiest way to do this would be:
1. Start pget.py
2. Type in `-get "test"`

## Bugs and Fixes:
If it says that there is no new update while there clearly is, you can navigate to bin/hash.txt and change the value
inside to 0 or just download the new update from github. This rarely occurs but there are chances it might.

## Switches
You'll see the available switches/commands when you start PGet.

## Contact
If you're having an issue with PGet or would like to submit a script. Well, as of now, you can't, but in the future,
it'll be possible.