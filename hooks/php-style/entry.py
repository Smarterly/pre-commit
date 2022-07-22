#!/usr/bin/env python3

from subprocess import Popen, PIPE, check_output, STDOUT
import os
import sys
import shlex

# ------------------------------------ #
#               Functions             #
# ----------------------------------- #

def yesNoQuestion(question, default = "no"):
  yesAnswers = {'yes','y'}
  noAnswers = {'no','n'}
  choice = ''
  sys.stdin = open('/dev/tty')
  while choice not in yesAnswers or choice not in noAnswers:
      print(bcolors.WARNING + question + bcolors.ENDC)
      choice = input().lower()
      if choice in yesAnswers:
         return True
      elif choice in noAnswers:
         return False
      else:
         print(bcolors.FAIL + "Please respond with 'yes' or 'no'" + bcolors.ENDC)

def separator():
  print("________________________________________________________________________________________________")
  print("")

def fixStyleAndAdd(files):
  # PHPCBF Exit codes
  # Exit code 0 is used to indicate that no fixable errors were found, so nothing was fixed
  # Exit code 1 is used to indicate that all fixable errors were fixed correctly
  # Exit code 2 is used to indicate that PHPCBF failed to fix some of the fixable errors it found
  # Exit code 3 is used for general script execution errors
  fix_style_process = Popen(shlex.split("make fix-style FILES='" + files + "'"), stdout=PIPE, stderr=PIPE)
  output, error = fix_style_process.communicate()
  print(output.decode('utf-8').strip())
  if fix_style_process.returncode > 1:
    print(bcolors.WARNING + "PHPCBF failed to fix the style erros"  + bcolors.ENDC)
    return 1
  os.system("git add " + files)
  print(bcolors.OKGREEN + "PHPCBF ran successfully"  + bcolors.ENDC)
  return 0


# ------------------------------------ #
#               Classes             #
# ----------------------------------- #

class bcolors:
    HEADER = '\033[1m\033[95m'
    SUBHEADER = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CWHITE  = '\33[37m'

# ------------------------------------ #
#                Script               #
# ----------------------------------- #

separator()
print(bcolors.HEADER + "RUNNING PRE-COMMIT HOOK" + bcolors.ENDC)

separator()
print(bcolors.SUBHEADER +  "STAGED FILES:" + bcolors.ENDC)
STAGED_FILES = check_output("git diff --cached --name-only --diff-filter=ACMR HEAD", shell=True).decode('utf-8').strip()

if len(STAGED_FILES) < 1:
  print(bcolors.WARNING + "No staged files. Aborting..")
  sys.exit(1)

print(STAGED_FILES)

separator()
print(bcolors.SUBHEADER + "RUNNING PHPCS CHECK" + bcolors.ENDC)
SPACE_SEPARATED_STAGED_FILES = STAGED_FILES.replace('\r', ' ').replace('\n', ' ')
check_style_process = Popen(shlex.split("make check-style FILES='" + SPACE_SEPARATED_STAGED_FILES + "'"), stdout=PIPE, stderr=PIPE)
output = check_style_process.communicate()[0]
print(output.decode('utf-8').strip())

if check_style_process.returncode != 0:
    separator()
    print(bcolors.SUBHEADER + "RUNNING PHPCBF AUTOMATIC REPAIRS" + bcolors.ENDC)
    if yesNoQuestion("Do you want to repair these files automatically? [y/n] [ENTER]"):
        fixed = fixStyleAndAdd(SPACE_SEPARATED_STAGED_FILES)
        sys.exit(fixed)
    else:
        print(bcolors.FAIL + bcolors.BOLD + "Please fix the styles manually and try again" + bcolors.ENDC)
        sys.exit(1)
else:
    print(bcolors.OKGREEN + "Good work! No style errors found" + bcolors.ENDC)

sys.exit(0)
