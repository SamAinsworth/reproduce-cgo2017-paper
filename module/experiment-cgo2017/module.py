#
# Collective Knowledge (Reproducing experiment from CGO2017 paper)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: cTuning foundation, admin@cTuning.org, http://cTuning.org
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# reproduce experiment

def reproduce(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os
    os.environ['CK_FETCHDIST']="32"

    r=ck.access({"action":"compile",
                 "module_uoa":"program",
                 "data_uoa":"randacc-swpf",
                 "out":"con"})
    if r['return']>0: return r

    r=ck.access({"action":"run",
                 "module_uoa":"program",
                 "data_uoa":"randacc-swpf",
                 "out":"con"})
    if r['return']>0: return r

#    import json
#    print (json.dumps(r,indent=2))
    exec_time=r['characteristics']['total_execution_time']

    ck.out('')
    ck.out('Total execution time via CK: '+str(exec_time))

    return {'return':0}
