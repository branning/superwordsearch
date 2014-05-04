#!/usr/bin/env python

import copy
import os
import sys
import time

def usage():
  print "Super Word Search!"
  print "usage: {} <input file>".format(os.path.basename(__file__))
  print "options:"
  print "\t--test\ttest some examples"
  print "\t--help\tprint this message"

class SuperInputError(Exception):
  pass

class SuperWordSearch(object):

  def __init__(self, logging=0):
    self.input_states = [self.__shape,self.__grid,self.__wrap,self.__n_words,self.__words]
    self._state = self.input_states[0]
    #self.error = None
    self.done = False
    self.use_trie = False
    self.logging = logging

  def read(self, line):
    if self.logging >= 2:
      print "State: {}, input: {}".format(self._state.__func__.__name__, line)
    if line.strip() == '':
      return
    if self._state in self.input_states:
      self._state = self._state(line)
    else:
      raise SuperInputError("Not ready for input")

  def find(self):
    if self._state == self.__find:
      self._state = self._state()
    else:
      print "Not ready to find, input not complete. Try using {}".format(self.read)

  def write(self, filename=None):
    if filename is None:
      out = sys.stdout
    else:
      out = open(filename, 'w')
    if self._state == self.__write:
      self._state = self._state(out)
    else:
      print "Search hasn't been performed yet.  Try using {} first".format(self.find)

  # State machine for reading sections of input file
  # shape -> grid -> wrap -> n words -> words
  def __shape(self, line):
    self.rows, self.cols = map(int, line.split(' '))
    self.grid = []
    return self.__grid

  def __grid(self, line):
    row = list(line)
    if len(row) == self.cols:
      self.grid.append(row)
      if len(self.grid) == self.rows:
        return self.__wrap
      else:
        return self.__grid
    else:
      self.error = "{} has the wrong number of columns!".format(line)
      # return None

  def __wrap(self, line):
    if line=="WRAP":
      self.wrap = True
      return self.__n_words
    elif line=="NO_WRAP":
      self.wrap = False
      return self.__n_words
    #else:
    #  return None

  def __n_words(self, line):
    self.n_words = int(line)
    self.words = []
    return self.__words

  def __words(self, line):
    self.words.append(line)
    if len(self.words) == self.n_words:
      # ready to do the super word search!! omg
      self.done = True
      return self.__find
    else:
      return self.__words

  def __find(self):
    # A letter cannot be used twice.  Keep track of the ones we've already used
    self.covered = [[False] * self.cols] * self.rows

    # Make a trie to search for the words
    if self.use_trie:
      self.trie = {}
      for word in self.words:
        t = self.trie
        for a,b in zip(word,word[1:] + '\n'): # pairs of adjacent characters
          if a not in t and b != '\n':
            t[a] = {}
          t[a][b] = {}
          t = t[a]

    # Make a working copy of the words and sort by length
    words = copy.copy(self.words)
    words.sort(key=len)
    self.found = {} # word -> (start row, start col), (end row, end col)

    # Search all outward paths from each letter.
    # This will cover all inward paths eventually
    points = ((x,y) for x in range(self.rows) for y in range(self.cols))
    x,y = 0,1 # rows, cols
    for start in points:
        for direction in ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)):
          # keep adding to search path until:
          #   path wraps onto itself or
          #   path runs off the grid
          #   path is longer than the longest search word
          #   path runs into a letter that's already been used
          search_path = (start,)
          while True:
            peek = tuple(e+d for e,d in zip(search_path[-1],direction))
            if self.wrap:
              peek = (peek[x] % self.rows, peek[y] % self.cols)
              if peek in search_path:
                break # don't include a letter twice
            elif peek[x] > self.cols-1 or peek[y] > self.rows-1 \
                 or peek[x] < 0 or peek[y] < 0:
              break # ran off the end of the grid
            if self.covered[peek[x]][peek[y]]:
              break # ran into a letter that's already used
            if len(search_path) == len(words[-1]):
              break # path length as long as longest search word
            search_path += (peek,)
          # search if we have a path that's at least as long as shortest word
          search_string = ''.join([self.grid[i][j] for i,j in search_path])
          if len(search_string) >= len(self.words[0]):
            if self.logging >= 2:
              print "Start {}, {}".format(start, search_string)
            for i,word in enumerate(words):
              if search_string[:len(word)] == word:
                if self.logging >= 1:
                  print "Found {} at {}".format(word, start)
                self.found[word] = (search_path[0], search_path[len(word)-1])
                words.pop(i)
                if len(words) == 0:
                  return self.__write # no more words left to find
                break
    return self.__write # read to write output file

  def __write(self, out):
    with out:
      for word in self.words:
        if word in self.found:
          start,end = self.found[word]
          # python puts a space between comma and items in tuples, remove them
          out.write("{} {}\n".format(str(start).replace(' ',''), str(end).replace(' ','')))
        else:
          out.write("NOT FOUND\n")
    return self.__write

def ex1():
  ws = SuperWordSearch()
  with open('example1.txt','r') as ex1:
    for line in ex1.readlines():
      ws.read(line.strip())
  ws.find()
  ws.write('ex1.out')
  return ws

def ex2():
  ws = SuperWordSearch()
  with open('example2.txt','r') as ex2:
    for line in ex2.readlines():
      ws.read(line.strip())
  ws.find()
  ws.write('ex1.out')
  return ws

def runtest(infile,outfile,answerfile):
  start = time.time()
  print "{},".format(infile),
  ws = SuperWordSearch()
  with open(infile,'r') as source:
    for line in source:
      ws.read(line.strip())
  print "{}x{} grid, {} words ...".format(ws.rows, ws.cols, len(ws.words)),
  ws.find()
  ws.write(outfile)
  with open(outfile,'r') as out:
    with open(answerfile,'r') as answer:
      if out.read() == answer.read():
        print "pass",
      else:
        print "fail",
      print "{:.3f} s".format(time.time() - start)

def test():
  # test is (input file, testoutput, golden answer, expected exception)
  tests = [('example1.txt','ex1.out','example1.out',None),
          ('example2.txt','ex2.out','example2.out',None),
          ('bad_input.txt','bad.out','',SuperInputError),
          ]
  for infile,outfile,answerfile,exception in tests:
    if exception is not None:
      try:
        runtest(infile,outfile,answerfile)

      except exception:
        print "expected exception, ok".format(exception)
    else:
      runtest(infile,outfile,answerfile)


if __name__=="__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == '--test': # hacked arg parsing
      test()
      quit()
    elif sys.argv[1] == '--help':
      usage()
      quit()
    else:
      infile = open(sys.argv[1], 'r')
  else:
    infile = sys.stdin

  with infile:
    ws = SuperWordSearch()
    for line in infile:
      ws.read(line.strip())
      if ws.done:
        ws.find()
        ws.write()
        break
    else:
      print "{} is an incomplete input file".format(fileinput.filename())
