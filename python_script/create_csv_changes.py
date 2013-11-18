#!/usr/bin/env python
import sys
import re
import os
from os.path import isfile
import fnmatch
import argparse
import csv
import re
from datetime import datetime, timedelta


'''
The log we are expecting here is of this form:
sha | committer | commit date | author | author date | subject | body
short change statistics

Example:
04a87564bbf807bb51e6c176cb3da244b1779c3b | cburroughs | Tue Mar 15 14:43:26 2011 -0400 | cburroughs | Tue Mar 15 14:43:26 2011 -0400 | Initial Commit. |

53 files changed, 291072 insertions(+)
'''

def get_time(commit_date):

    #print commit_date
    if len(commit_date.strip().rsplit(" ",1)) != 2:
        return None
    d, t = commit_date.strip().rsplit(" ",1)
    #print d, ",", t
    date_object = datetime.strptime(d, '%a %b %d %H:%M:%S %Y')
    h = int(t[1:3])
    m = int(t[4:6])
    if t[0]=='-':
        delta = date_object + timedelta(hours=h, minutes=m)
    else:
        delta = date_object - timedelta(hours=h, minutes=m)

    #print str(delta)
    return str(delta)

def if_conflict(author, committer):
    isBug = False

    err_str = 'mergeconflict'
    if re.search(err_str, author, re.IGNORECASE):
        isBug = True
    if re.search(err_str, committer, re.IGNORECASE):
        isBug = True

    return isBug

def if_bug(subject, body):
    # add bug checking logic
    isBug = False

    err_str = 'error|bug|fix|fuck|issue|bitch|mistake|blunder|incorrect| fault|defect|flaw|glitch|gremlin|change'
    if re.search(err_str, subject, re.IGNORECASE):
        isBug = True
    if re.search(err_str, body, re.IGNORECASE):
        isBug = True

    return isBug

def log_parse(log_file, proj, language, csv_file):
    print log_file, proj, language, csv_file
    sha , committer, commit_date, author,  author_date, subject, body = "", "", "", "", "", "", ""

    csvf = open(csv_file, 'a')

    csv_writer = csv.writer(csvf, delimiter='|',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    lf = open(log_file, 'r')

    isHeader = True

    for line in lf:
        file_changed  = 0
        insertion     = 0
        deletion      = 0

        #print line
        if isHeader:
            isHeader = False
            continue
        line = line.rstrip()
        column_count = line.count('|')
        if column_count == 6:
            #this is the commit details
            sha, committer, commit_date, author,  author_date, subject, body = line.split('|')

            #print line

            body = body.decode('ascii', 'ignore')
            commit_date = get_time(commit_date)
            author_date = get_time(author_date)

            if author_date is None or commit_date is None:
                print "!! ----> " , proj, language
                print line
            #print sha, committer, commit_date, author,  author_date, subject, body

        elif "file changed," in line:
            change_stat = line.split(',')
            #print change_stat
            #print len(change_stat)
            for c in change_stat:
                if 'file changed' in c:
                    file_changed = c.split('file changed')[0]
                    file_changed = file_changed.strip()
                elif 'insertion(+)' in c:
                    insertion = c.split('insertion(+)')[0]
                    insertion = insertion.strip()
                elif 'insertions(+)' in c:
                    insertion = c.split('insertions(+)')[0]
                    insertion = insertion.strip()
                elif 'deletion(-)' in c:
                    deletion = c.split('deletion(-)')[0]
                    deletion = deletion.strip()
                elif 'deletions(-)' in c:
                    deletion = c.split('deletions(-)')[0]
                    deletion = deletion.strip()

            isBug = 0
            if if_bug(subject, body) is True:
                isBug = 1
            if if_conflict(author, committer) is True:
                isBug += 2

            subject = subject.decode('ascii', 'ignore')
            author = author.decode('ascii', 'ignore')
            committer = committer.decode('ascii', 'ignore')
            csv_writer.writerow([proj, language, sha, committer, commit_date, author,  author_date, subject.strip(), body.strip(), file_changed, insertion, deletion, isBug])
        else:
            body += line.decode('ascii', 'ignore')


def parse_dir(lang_dir, csv_file):
    language = lang_dir.split("top_")[1]
    for root, dirnames, filenames in os.walk(lang_dir):
        for filename in fnmatch.filter(filenames, 'no_merge_log.txt'):
            proj = os.path.basename(root)
            file_name = (os.path.join(root, filename))
            log_parse(file_name, proj, language, csv_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tool to create csv file from parsing git log')
    parser.add_argument('--version', action='version', version='Repertoire 1.0')
    #parser.add_argument('-i',dest="log_file", help="the git log to be parsed")
    #parser.add_argument('-d',dest="csv_file", help="the output csv file")
    parser.add_argument('-i',dest="lang_dir", help="the directories contaning src code, and contains log")
    parser.add_argument('-d',dest="csv_file", help="the output csv file")

    args = parser.parse_args()

    lang_dir = args.lang_dir
    csv_file = args.csv_file

    if lang_dir is None:
        print "!! Please provide a valid log file"
        sys.exit()

    if csv_file is None:
        print "!! Please provide a valid csv file to store output"
        sys.exit()

    if not os.path.exists(lang_dir):
        print "!! log file %s does not exit" % (lang_dir)
        sys.exit()

    print lang_dir, csv_file
    csvf = open(csv_file, 'w')
    csv_writer = csv.writer(csvf, delimiter='|',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['project', 'language', 'sha', 'committer', 'commit_date', 'author',  'author_date', 'subject', 'body', 'file_changed', 'insertion', 'deletion', 'isBug'])
    csvf.close()

    parse_dir(lang_dir, csv_file)
    #print if_bug("allow LiftJsonRequestBody.jsonFormats to be overridden by any type extending Formats (rather than the object DefaultFormats", "")
    #commit_date = 'Mon Oct 18 23:29:15 2010 +0500'
    #print get_time(commit_date)




