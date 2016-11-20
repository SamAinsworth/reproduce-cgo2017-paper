#
# Postprocessing program and converting
# raw output to the CK timing format.
#

import json
import os
import re

def ck_postprocess(i):

    ck=i['ck_kernel']

    cc={}

    # Load output as list.
    r=ck.load_text_file({'text_file':'tmp-output1.tmp','split_to_list':'yes'})
    if r['return']>0: return r

    for l in r['lst']:
        x='time : '
        y=l.find(x)
        if y>=0:
            s=l[y+len(x):].strip()
            fs=float(s)

            cc['execution_time']=fs

            break

    if len(cc)==0:
       return {'return':1, 'error':'couldn\'t parse time in stdout'}

    return {'return':0, 'characteristics':cc}

# Do not add anything here!
