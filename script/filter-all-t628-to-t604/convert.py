#
# Collective Knowledge (Experiment to check that filter optimizations 
#  may depend on image features and hence require run-time adaptation)
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://cTuning.org/lab/people/gfursin
#

import os
import sys
import copy
import ck.kernel as ck

sep='***************************************************************************'

euoa1='hog-mali-t604'
euoa2='hog-mali-t628-as-t604'

######################################################################
def run(i):
    # Get path1
    r=ck.access({'action':'load',
                 'module_uoa':'experiment',
                 'data_uoa':euoa1})
    if r['return']>0: return r
    p1=r['path']

    # Get path1
    r=ck.access({'action':'load',
                 'module_uoa':'experiment',
                 'data_uoa':euoa2})
    if r['return']>0: return r
    p2=r['path']

    # Going through points in path 2
    dirList1=os.listdir(p1)
    dirList2=os.listdir(p2)

    for fn2 in dirList2:
        if fn2.endswith('.features.json'):
           ck.out('Loading point '+fn2+' ...')

           px2=os.path.join(p2, fn2)

           r=ck.load_json_file({'json_file':px2})
           if r['return']>0: return r

           df2=r['dict'].get('features',{})

           # Searching in p1
           found=False
           for fn1 in dirList1:
               if fn1.endswith('.features.json'):
                  px1=os.path.join(p1, fn1)

                  r=ck.load_json_file({'json_file':px1})
                  if r['return']>0: return r

                  df1=r['dict'].get('features',{})
     
                  rx=ck.compare_dicts({'dict1':df1, 'dict2':df2})
                  if rx['return']>0: return rx

                  equal=rx['equal']
                  if equal=='yes':
                     found=True
                     break

           if found:
              ck.out('  Found!')
           else:
              # Removing point
              ck.out('    Removing point ...')

              fn=fn2[:-14]

              for fn0 in dirList2:
                  if fn0.startswith(fn):
                     p0=os.path.join(p2,fn0)
                     os.remove(p0)

    return {'return':0}

######################################################################
r=run({})
if r['return']>0:
   ck.err(r)
   exit(1)
