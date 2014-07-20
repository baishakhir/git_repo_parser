
import sys
import os
import codecs
import re
from datetime import datetime, timedelta

sys.path.append("../util")

from dumpLogs import dumpLogs

SHA   = '[a-f0-9]{40}'
#EMAIL = '<[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}>'
EMAIL = '<[A-Z0-9._%+-]+@([a-z0-9-])+>'
DATE  = '[0-9]{4}-[0-9]{2}-[0-9]{2}'



def toStr(text):
  try:
    text1 = str(text).encode('iso-8859-1')
    temp_text = text1.replace("\'","\"")
    temp_text = temp_text.strip()
    return "\'" + str(temp_text) + "\'"
  except:
    print type(text)
    return "\'NA\'"
#text = str(text).encode('utf-8')

class PatchMethod:

  def __init__(self, methodName):

    self.method  = methodName

    self.assert_add = 0 # No. of assertion added
    self.assert_del = 0 # No. of assertion deleted
    self.total_add  = 0 # No. of lines added
    self.total_del  = 0 # No. of lines deleted

  def printPatch(self):

    #retStr  = "\n\t\t------ Method -----\n"
    retStr  = ""
    retStr += "\t\tmethod      = %s\n" % (self.method)
    retStr += "\t\tassert_add  = %d\n" % (self.assert_add)
    retStr += "\t\tassert_del  = %d\n" % (self.assert_del)
    retStr += "\t\ttotal_add   = %d\n" % (self.total_add)
    retStr += "\t\ttotal_del   = %d\n" % (self.total_del)

    return retStr

  def dumpMethod(self):

    method      = toStr(self.method)
    assert_add  = toStr(self.assert_add)
    assert_del  = toStr(self.assert_del)
    total_add   = toStr(self.total_add)
    total_del   = toStr(self.total_del)

    methodStr = (",").join((method,assert_add,assert_del,total_add,total_del))
    return methodStr


class Patch:

  def __init__(self, fileName, language):

    self.file_name = fileName
    self.language  = language

    self.is_test    = False
    self.methods  = []

  def addMethod(self, methodName):

    method = PatchMethod(methodName)
    self.methods.append(method)


  def printPatch(self):

    retStr  = "\n\t------ Patch -----\n"
    retStr += "\tlanguage    = %s\n" % (self.language)
    retStr += "\tfile        = %s\n" % (self.file_name)
    retStr += "\tis_test     = %s\n" % (self.is_test)

    for m in self.methods:
      retStr += m.printPatch()

    return retStr

  def dumpPatch(self, sha, project, dumpLog):

    sha      = toStr(sha)
    project  = toStr(project)
    language = toStr(self.language)
    fileName = toStr(self.file_name)
    isTest   = toStr(self.is_test)

    for m in self.methods:
      patchStr = (",").join((project, sha, language, fileName, isTest, m.dumpMethod()))
      #print patchStr
      dumpLog.dumpMethodChanges(patchStr)

class Sha:

  def __init__(self, project, sha):

    self.project    = project
    self.sha        = sha

    self.language   = None
    self.file_name  = None
    self.function   = None

    self.author     = None
    self.date       = None
    self.is_bug     = False
    self.log        = None

    self.patches    = []

  def __str__(self):

    return self.printSha()

  def dumpSha(self, dumpLogDb):

    project = toStr(self.project)
    sha     = toStr(self.sha)
    author  = toStr(self.author)
    commit_date = toStr(self.date)
    log     = toStr(self.log)
    is_bug  = toStr(self.is_bug)

    #shaStr = (",").join((project,sha,author,commit_date,log,is_bug))
    shaStr = (",").join((project,sha,author,commit_date,is_bug))
    print shaStr

    dumpLogDb.dumpSummary(shaStr)

    self.dumpPatches(dumpLogDb)




  def printSha(self):

    retStr  = "------ Sha Details -----\n"
    retStr += "project     = %s\n" % (self.project)
    retStr += "sha         = %s\n" % (self.sha)
    retStr += "author      = %s\n" % (self.author)
    retStr += "commit date = %s\n" % (self.date)
    retStr += "log         = %s\n" % (self.log)
    retStr += "is_bug      = %s\n" % (self.is_bug)

    retStr += self.printPatches()
    #print self.patches

    print retStr

  def dumpPatches(self,dumpLogDb):

    for p in self.patches:
      p.dumpPatch(self.sha, self.project, dumpLogDb)


  def printPatches(self):

    retStr = ""
    for p in self.patches:
      retStr += p.printPatch()

    return retStr


  def setLog(self, log):

    self.log = log

    if len(log) > 1000:
      self.log = log[:1000]

    err_str  = ' error | bug | fix | issue | mistake | blunder | incorrect|" \
      + " fault | defect | flaw | glitch | gremlin '
    if re.search(err_str, log, re.IGNORECASE):
      self.is_bug = True


class ghLogDb:

  def __init__(self, logFile):

    self.log_file = logFile
    self.project_name = None
    self.curr_method = None
    self.shas = []

  def __str__(self):

    print self.project_name
    for s in shas:
      print s

  def isSha(self,line):

    is_sha = re.search(SHA, line, re.IGNORECASE)
    sha = None
    if line.startswith("commit") and is_sha:
      sha = is_sha.group(0)
    return sha

  def isAuthor(self,line,shaObj):

    assert(shaObj != None)
    is_auth = re.search(EMAIL, line, re.IGNORECASE)
    if line.startswith("Author:") and is_auth:
      author = is_auth.group(0)
      #print "!!!!"
      print author
      #print line.split(author)
      shaObj.author =  line.split(author)[0].split("Author:")[1]
      shaObj.author = shaObj.author.strip()
      print shaObj.author
      return True
    return False

  def isDate(self,line,shaObj):

    assert(shaObj != None)
    is_date = re.search(DATE, line, re.IGNORECASE)
    if line.startswith("Date:") and is_date:
      date = is_date.group(0)
      #print shaObj.sha, "---->" , date
      shaObj.date = date
      return True
    return False

  def createPatchWithNoPrevVersion(self, line):
    #there was no previous version of a file

    patchObj = None
    if line.startswith("index "):
      pass

    elif line.startswith("+++ b/"):
      #print line.split("+++ b/")

      file_name = line.split("+++ b/")[1]
      fileName, extension = os.path.splitext(file_name)

      if extension == "":
        language = ""
      else:
        language = extension.split(".")[1]

      patchObj = Patch(file_name, language)

      if "test" in fileName:
        patchObj.is_test = True

    return patchObj

  def createPatch(self, line):

    patchObj = None
    if line.startswith("index "):
      pass

    elif line.startswith("--- a/"):

      file_name = line.split("--- a/")[1]
      fileName, extension = os.path.splitext(file_name)

      if extension == "":
        language = ""
      else:
        language = extension.split(".")[1]

      patchObj = Patch(file_name, language)

      if "test" in fileName:
        patchObj.is_test = True

    return patchObj

  def processPatch(self, line, patchObj):

    if line.startswith("index "):
      pass

    elif line.startswith("--- a/"):
      assert(patchObj == None)
      file_name = line.split("--- a/")[1]
      fileName, extension = os.path.splitext(file_name)

      if extension == "":
        language = ""
      else:
        language = extension.split(".")[1]

      patchObj = Patch(file_name, language)

      if "test" in fileName:
        patchObj.is_test = True

    elif line.startswith("+++ b/"):
      pass

    elif line.startswith("@@ "):
      temp_func   = line.split("@@ ")
      #print temp_func
      if len(temp_func) <= 2:
        #method name does not exis
        method_name = "NA"
      else:
        temp_func = temp_func[-1]
        if '(' in temp_func:
          temp_func   = temp_func.rsplit('(')[0]
          method_name = temp_func.split(" ")[-1]
        else:
          #not a traditional method, contains other signature
          method_name = temp_func

      #print "method name = " , method_name
      patchObj.addMethod(method_name)

    else:

      if line.startswith("-"):
        #print "------" , line
        m = patchObj.methods[-1]
        m.total_del += 1
        if "assert" in line:
          m.assert_del += 1

      elif line.startswith("+"):
        #print "++++++" , line
        m = patchObj.methods[-1]

        m.total_add += 1
        if "assert" in line:
          m.assert_add += 1

    return patchObj



  def processLog(self):

    project1 = os.path.split(self.log_file)[0]
    project1 = project1.rstrip(os.sep)
    self.project_name = os.path.basename(project1)
    print("---------- %s ------------\n" % (self.project_name))

    dl = dumpLogs()

    inf = codecs.open(self.log_file, "r", "iso-8859-1")
    #lines = inf.readlines()
    #inf.close()

    shaObj   = None
    patchObj = None
    is_diff  = False
    log_mssg = ""
    is_no_prev_ver = False
    is_no_next_ver = False

    #for i,l in enumerate(lines):
    for l in inf:
      #continue
      #print i+1, line
      sha  = self.isSha(l)
      #line = l.strip()
      line = l
      #print line

      if sha:
        # if shaObj != None:
        #   shaObj.dumpSha(dl)

        shaObj = Sha(self.project_name, sha)
        self.shas.append(shaObj)
        is_diff = False
        log_mssg = ""
        continue

      elif self.isAuthor(line,shaObj):
        continue

      elif self.isDate(line,shaObj):
        continue

      line = line.strip()

      if line.startswith('diff --git '):
        shaObj.setLog(log_mssg)
        is_diff = True
        is_no_prev_ver = False
        is_no_next_ver = False
        continue
        '''
        if patchObj != None:
          shaObj.patches.append(patchObj)
        '''
      elif is_diff == False:
        if not line.strip():
          continue
        log_mssg += line + "\t"


      if is_diff:
        if line.startswith("--- a/"):
          #print "<a> : " , line
          patchObj = self.createPatch(line)
          shaObj.patches.append(patchObj)
          #print patchObj
          #print shaObj.patches
        elif (line == '--- /dev/null'): #earlier file was empty
          #print "<b> : " , line
          is_no_prev_ver = True
        elif (line == '+++ /dev/null'): #next file version was empty
          #print "<c> : " , line
          is_no_next_ver = True
          continue
        elif (is_no_prev_ver == True) and line.startswith("+++ b/"):
          #print "<d> : " , line
          patchObj = self.createPatchWithNoPrevVersion(line)
          shaObj.patches.append(patchObj)
          #print shaObj.patches
        else:
          #print "<e> : " , line
          self.processPatch(line,patchObj)

    if shaObj != None:
      shaObj.patches.append(patchObj)

    for s in self.shas:
      #s.printSha()
      if s != None:
        s.dumpSha(dl)

    dl.close()
    inf.close()
    print len(self.shas)



#---------test-----------#
def test():
  if len(sys.argv) < 2:
    print "!!! Pass a log file."
    print "usage ./ghLogDb.py ccv_all_log.txt"
    sys.exit()

  log_file = sys.argv[1]
  ghDb = ghLogDb(log_file)
  ghDb.processLog()


if __name__ == '__main__':
  test()
