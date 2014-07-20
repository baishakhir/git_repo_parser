import sys
import os
from git import *

sys.path.append("../util")

import Util
from ghLogDb import ghLogDb


LOG_FILE = "all_log.txt"

def dumpLog(projPath):

  if not os.path.isdir(projPath):
    print("!! Please provide a valid directory")
    return

  log_file = projPath + os.sep + LOG_FILE

  if os.path.isfile(log_file):
  	print("%s exists!!" % (log_file))
  	return

  with Util.cd(projPath):
    os.system("git pull")
    logCmd = "git log --date=short -U1 -- \*.c > all_log.txt"
    print logCmd
    os.system(logCmd)

    logCmd = "git log --date=short -U1 -- \*.cpp >> all_log.txt"
    print logCmd
    os.system(logCmd)
##    logCmd = "git log --date=short -U1 -- \*.h >> all_log.txt"
##    print logCmd
##    os.system(logCmd)
##    logCmd = "git log --date=short -U1 -- \*.hpp >> all_log.txt"
##    print logCmd
##    os.system(logCmd)

    logCmd = "git log --date=short -U1 -- \*.java >> all_log.txt"
    print logCmd
    os.system(logCmd)


def processLog(projPath):

  if not os.path.isdir(projPath):
    print("!! Please provide a valid directory")
    return

  log_file = projPath + os.sep + LOG_FILE
  ghDb = ghLogDb(log_file)
  ghDb.processLog()


def getGitLog(project):

  projects = os.listdir(project)
  for p in projects:
    proj_path = os.path.join(project, p)
    print proj_path
    dumpLog(proj_path)
    processLog(proj_path)

def main():
  print "==== Utility to process Github logs ==="

  if len(sys.argv) < 2:
  	print "!!! Usage: python ghProc.py project"
  	sys.exit()

  project = sys.argv[1]

  if not os.path.isdir(project):
    print("!! Please provide a valid directory")
    return

  getGitLog(project)


if __name__ == '__main__':
  main()








