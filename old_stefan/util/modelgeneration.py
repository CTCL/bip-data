#NASTY SCRIPT TO RESOLVE DEPENDENCIES AMONG AK CLASSES YIELDED BY INSPECTDB



import re

fk_re = re.compile('ForeignKey\([a-zA-Z]+')

collection = {}

def get_class(text):
    return text.split('(')[0].replace('class','').strip()

def get_deps(text):
    ans = []
    for line in text.split('\n'):
        test = fk_re.search(line)
        if test != None:
            ans.append(test.group(0).split('(')[1])
    return ans

class Node:
    def __init__(self,args):
        self.name = args['name']
        self.collection = args['collection']
        self.deps = args['deps']
        self.text = args['text']
    def edges(self):
        for dep in self.deps:
            yield self.collection[dep]
         
def dep_resolve(node, resolved, seen):
   """modified http://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/"""
   seen.append(node)
   for edge in node.edges():
      if edge not in resolved:
         if edge in seen:
            raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
         for x in dep_resolve(edge, resolved, seen):
             yield x
   resolved.append(node)
   print node.name
   yield node.text




def go():
  """Generate new api/data/models.py file. Use with caution."""
  import sys,os
  from fabric.api import local
  from fabric.context_managers import lcd
  with lcd('src/api'):#&&
    local('pwd')
    local('python manage.py inspectdb > data/unordered_models.py')
  in_fname = os.path.abspath('src/api/data/unordered_models.py')#os.path.abspath(sys.argv[1])
  out_fname = os.path.abspath('src/api/data/models.py')#os.path.abspath(sys.argv[2])
  #assert os.path.exists(in_fname) and not os.path.exists(out_fname)
  src_file = open(in_fname).read().split("from django.db import models")
  header = src_file[0]
  src = src_file[1]
  classes = ['class' + x for x in src.split("""

class""")]
  for c in classes:
    collection[get_class(c)] = Node({'text':c,'name':get_class(c),'deps':get_deps(c),'collection':collection})
  resolved = []
  done = []
  for k in sorted(collection.keys()):
    if k == '': continue
    done += [x for x in dep_resolve(collection[k], resolved, [])]

  outfile = open(out_fname,'w')
  outfile.write(header.replace('''Rearrange models' order''','''Rearrange models' order (DONE)'''))
  outfile.write("from django.db import models\n")
  outfile.write('\n\n'.join(done))
  outfile.close()
  print "Code written to %s. Please review the contents of this file." % out_fname

























