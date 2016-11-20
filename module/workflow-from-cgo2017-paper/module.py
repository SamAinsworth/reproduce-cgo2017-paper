#
# Collective Knowledge (Experiment workflow from CGO2017 paper)
#
#  
#  
#
# Developer:  ,  ,  
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
line='**********************************************************************************'
line1='----------------------------------------------------------------------------------'
flog='ck-log-reproduce-results-from-cgo2017-paper.txt'
fflog=''
log_init=False

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
# Log results

def log(i):
    """

    Input:  {
              string         - text to append to log
              (out)          - if 'yes', print string
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    global log_init,fflog

    if not log_init:
       fflog=os.path.join(os.getcwd(),flog)
       if os.path.isfile(fflog):
           os.remove(fflog)

       log_init=True

    s=i['string']

    # Append text
    r=ck.save_text_file({'text_file':fflog, 'string':s+'\n', 'append':'yes'})

    if i.get('out','')=='yes':
        ck.out(s)

    return r

##############################################################################
# Run experiments

def experiment(i):
    """

    Input:  {
              program_uoa  - program UID or alias
              (env)        - compile/run environment
              (quiet)      - if 'yes', do not ask to press enter
              (title)      - print title (and record to log)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    o=i.get('out','')
    oo=''
    if o=='con': oo=o

    # Print title
    q=i.get('quiet','')
    title=i.get('title','')
    subtitle=i.get('subtitle','')

    if title!='':
        log({'string':line, 'out':'yes',})
        log({'string':title, 'out':'yes'})
        log({'string':'', 'out':'yes'})

    if subtitle!='':
        log({'string':line1, 'out':'yes',})
        log({'string':subtitle, 'out':'yes'})
        log({'string':'', 'out':'yes'})

    if q!='yes': 
       ck.out('')
       r=ck.inp({'text':'Press Enter to continue!'})

    hos=i.get('host_os','')
    tos=i.get('target_os', '')
    tdid=i.get('device_id', '')

    puoa=i['program_uoa']
    env=i.get('env',{})

    # Compile program
    ck.out('')
    ck.out('Compiling program ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':puoa,
                 'speed':'yes',
                 'env':env,
                 'out':oo})
    if r['return']>0: return r

    # Run program 3 times
    times=[]
    for x in range(0,3):
        ck.out(line1)
        ck.out('Running program ('+str(x+1)+' out of 3) ...')
        ck.out('')

        r=ck.access({'action':'run',
                     'module_uoa':cfg['module_deps']['program'],
                     'data_uoa':puoa,
                     'env':env,
                     'out':oo})
        if r['return']>0: return r

        ch=r.get('characteristics',{})
        if ch.get('run_success','')!='yes':
            return {'return':1, 'error':'execution failed ('+ch.get('fail_reason','')+')'}

        et=ch.get('execution_time',0.0)
        times.append(et)

    # Check some stats (later move to CK)
    tmin=float(min(times))
    tmax=float(max(times))

    stmin='%.2f' % tmin
    stmax='%.2f' % tmax

    # Print
    log({'string':'', 'out':'yes'})
    log({'string':'Min execution time: '+stmin, 'out':'yes'})
    log({'string':'Max execution time: '+stmax, 'out':'yes'})

    return {'return':0, 'times':times, 'tmin':tmin, 'tmax':tmax, 'stmin':stmin, 'stmax':stmax}

##############################################################################
# run workflow

def run(i):
    """
    Input:  {
              (quiet)  - if 'yes', do not ask questions (useful to save output)
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    # Check output (console, json, file...)
    o=i.get('out','')
    oo=''
    if o=='con': oo=o

    q=i.get('quiet','')

    # Get platform features
    ck.out(line)
    ck.out('Note that results will be logged to '+flog+' - please check it afterwards!')
    ck.out('')
    if q!='yes': r=ck.inp({'text':'Press Enter to continue!'})

    log({'string':'Experiment workflow started!'})
    log({'string':''})

    # Get platform features
    ck.out(line)
    ck.out('We will now detect your platform features. If you encounter any unexpected behavior, please report them to the authors! Thank you!')
    ck.out('')
    if q!='yes': r=ck.inp({'text':'Press Enter to continue!'})

    hos=i.get('host_os','')
    tos=i.get('target_os', '')
    tdid=i.get('device_id', '')

    ii={'action':'detect',
        'module_uoa':cfg['module_deps']['platform'],
        'out':oo,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'skip_info_collection':'',
        'force_platform_name':'',
        'exchange':'no'}
    r=ck.access(ii)
    if r['return']>0: return r

    pft=r['features']

    hos=r['host_os_uoa']
    hosd=r['host_os_dict']

    tos=r['os_uoa']
    tosd=r['os_dict']
    tbits=tosd.get('bits','')
    tdid=r['device_id']

    if hos=='':
       return {'return':1, 'error':'"host_os" is not defined or detected'}

    if tos=='':
       return {'return':1, 'error':'"target_os" is not defined or detected'}

    # Check which system you run
    os_abi=pft.get('os',{}).get('abi','').lower()

    ck.out(line)
    if os_abi=='':
        ck.out('Your host OS ABI was not detected. Will skip comparison with pre-recorded results!')
    else:
        ck.out('Detected host OS ABI: '+os_abi)

        if os_abi=='x86_64' or os_abi=='armv7l' or os_abi=='aarch64':
            ck.out('')
            ck.out('We have pre-recorded results for your host OS and will perform comparison!')

    ck.out('')
    if q!='yes': r=ck.inp({'text':'Press Enter to continue!'})

    # Check if package is installed
    ck.out(line)
    ck.out('We will now check/install software dependencies [LLVM and plugins] via CK!')
    ck.out('')
    if q!='yes': r=ck.inp({'text':'Press Enter to continue!'})

    # Get dependencies from meta from any program from this repo
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':cfg['programs_uoa']['randacc']})
    if r['return']>0: return r

    deps=r['dict']['compile_deps']

    # Resolving deps
    ii={'action':'resolve',
        'module_uoa':cfg['module_deps']['env'],
        'host_os':hos,
        'target_os':tos,
        'device_id':tdid,
        'deps':deps,
        'out':oo}
    rx=ck.access(ii)
    if rx['return']>0: return rx

    # Reproducing Figure 2 ###################################################################################
    exp='figure-2-nas-is-no-prefetching'

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'quiet':q,
                  'title':'Reproducing experiments for Figure 2',
                  'subtitle':'Validating NAS-IS no prefetching:'})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})








    return {'return':0}
