import sys, os
import psycopg2
import logging
import codecs

sys.path.append("../util")

from DatabaseCon import DatabaseCon
from Config import Config
import Util


class dumpLogs:

  def __init__(self, configFile='config.ini'):

    self.cfg = Config(configFile)
    self.connectDb()
    #self.clean_db()


  def connectDb(self):

    self.db_config = self.cfg.ConfigSectionMap("Database")
    logging.debug("Database configuration = %r\n", self.db_config)
    self.dbCon = DatabaseCon(self.db_config['database'], self.db_config['user'], \
                             self.db_config['host'], self.db_config['port'])


  def cleanDb(self):

    schema = self.db_config['schema']
    response = raw_input("Deleting database %s ?" % (self.db_config['schema']))

    if response.lower().startswith('y'):
      pass
      # for table in [self.db_config['table_entropy']]:
      #   tab = schema + "."  + table
      #   print("Deleting table %r \n" % table)
      #   sql_command = "DELETE FROM " + tab
      #   self.dbCon.insert(sql_command)

    self.dbCon.commit()


  # def insert_change_table(self, valueStr):

  #   schema = self.project #self.db_config['schema']
  #   table = schema + "." + self.db_config['table_entropy']

  #   #logging.debug("table = %r" % table)

  #   sql_command = "INSERT INTO " + table + \
  #               "(language, project, snapshot, file_name, line_no, prefix, " + \
  #                 "suffix, is_cache, cache_min_order, cache_backoff_weight, train_type)" + \
  #                 "VALUES (" + valueStr + ")"

  #   print sql_command
  #   #logging.debug(sql_command)
  #   self.dbCon.insert(sql_command)

  def close(self):
    self.dbCon.commit()
    self.dbCon.close()

  def dumpSummary(self, summaryStr):

    schema = self.db_config['schema']
    table = schema + "." + self.db_config['table_change_summary']

    sql_command = "INSERT INTO " + table + \
                "(project, sha, author, commit_date, is_bug)" + \
                "VALUES (" + summaryStr + ")"

    print sql_command
    self.dbCon.insert(sql_command)
    #self.dbCon.commit()

  def dumpMethodChanges(self, methodChange):

    schema = self.db_config['schema']
    table = schema + "." + self.db_config['table_method_detail']

    sql_command = "INSERT INTO " + table + \
                "(project, sha, language, file_name, is_test, method_name, assertion_add, " + \
                "assertion_del, total_add, total_del)" + \
                "VALUES (" + methodChange + ")"

    print sql_command
    self.dbCon.insert(sql_command)
    #self.dbCon.commit()


