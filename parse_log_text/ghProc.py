import sys
import os
from git import *

sys.path.append("../util")

import Util
from ghLogDb import ghLogDb


LOG_FILE = "all_log.txt"

def dumpLog(projPath):

  log_file = projPath + os.sep + LOG_FILE

  if os.path.isfile(log_file):
  	print("%s exists!!" % (log_file))
  	return

  with Util.cd(projPath):

  	logCmd = "git log --date=short -U1 -- \*.java > all_log.txt"
  	print logCmd
  	os.system(logCmd)

def processLog(projPath):
  
  log_file = projPath + os.sep + LOG_FILE
  ghDb = ghLogDb(log_file)
  ghDb.processLog()

def checkProj(project):

  if not os.path.isdir(project):
  	print("!! %s does not exist" % (project))
  	return False

  '''
  repo = Repo(project)
  if(repo.bare == False):
  	print("!! %s is not a git repository" % (project))
  	return False
  '''

  return True


def main():
  print "Utility to process github logs"

  if len(sys.argv) < 2:
  	print "!!! Usage: python ghProc.py project"
  	sys.exit()

  project = sys.argv[1]

  if checkProj(project) == False:
    print("!! Please provide a valid directory")
    return

  #dumpLog(project)
  processLog(project)


if __name__ == '__main__':
  main()








