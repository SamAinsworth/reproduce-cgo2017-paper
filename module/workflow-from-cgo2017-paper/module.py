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
              (deps)       - pre-resolved deps
              (env)        - compile/run environment
              (cmd)        - if !='', use as cmd_key
              (quiet)      - if 'yes', do not ask to press enter
              (title)      - print title (and record to log)
              (results)    - dict with results
              (key)        - key to check results
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

    deps=i.get('deps',{})

    key=i.get('key','')
    results=i.get('results',{})

    cmd=i.get('cmd','')

    # Compile program
    ck.out('')
    ck.out('Compiling program ...')
    ck.out('')

    r=ck.access({'action':'compile',
                 'module_uoa':cfg['module_deps']['program'],
                 'data_uoa':puoa,
                 'deps':deps,
                 'speed':'yes',
                 'env':env,
                 'out':oo})
    if r['return']>0: return r

    # Run program N times (to analyze variation)
    times=[]
    for x in range(0,1):
        ck.out(line1)
        ck.out('Running program ('+str(x+1)+' out of 3) ...')
        ck.out('')

        r=ck.access({'action':'run',
                     'module_uoa':cfg['module_deps']['program'],
                     'data_uoa':puoa,
                     'cmd_key':cmd,
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

    stmin='%.3f' % tmin
    stmax='%.3f' % tmax

    # Check if results exist:
    estmin='' # expected min
    estmax='' # expected max
    if key!='':
       x=results.get(key,{}).get('stmin','')
       if x!='': estmin=' (from paper: '+x+')'
       x=results.get(key,{}).get('stmax','')
       if x!='': estmax=' (from paper: '+x+')'

    # Print
    log({'string':'', 'out':'yes'})
    log({'string':'Min execution time: '+stmin+estmin, 'out':'yes'})
    log({'string':'Max execution time: '+stmax+estmax, 'out':'yes'})

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

    # Pre-load results
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['result'],
                 'data_uoa':cfg['pre-recorded-result-uoa']})
    if r['return']>0: return r
    results=r['dict'].get(os_abi,{})

    if len(results)==0:
        ck.out('')
        ck.out('We do not have pre-recorded results for your host OS ('+os_abi+') to perform comparison!')

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
    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'Reproducing experiments for Figure 2',
                  'subtitle':'Validating nas-is no prefetching:',
                  'key':'figure-2-nas-is-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset-64-nostride'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is intuitive:',
                  'key':'figure-2-nas-is-offset-64-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':2},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is small:',
                  'key':'figure-2-nas-is-offset-2', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':2048},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is big:',
                  'key':'figure-2-nas-is-offset-2048', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':2048},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is best:',
                  'key':'figure-2-nas-is-offset-64', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})




    # Reproducing Figure 4 ###################################################################################


    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'Reproducing experiments for Figure 4',
                  'subtitle':'Validating nas-cg no prefetching:',
                  'key':'figure-4-nas-cg-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-cg auto prefetching:',
                  'key':'figure-4-nas-cg-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'man'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-cg manual prefetching:',
                  'key':'figure-4-nas-cg-man', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is no prefetching:',
                  'key':'figure-4-nas-is-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is auto prefetching:',
                  'key':'figure-4-nas-is-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'man'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating nas-is manual prefetching:',
                  'key':'figure-4-nas-is-man', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating randacc no prefetching:',
                  'key':'figure-4-randacc-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating randacc auto prefetching:',
                  'key':'figure-4-randacc-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'man'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating randacc manual prefetching:',
                  'key':'figure-4-randacc-man', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 no prefetching:',
                  'key':'figure-4-hashjoin-ph-2-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 auto prefetching:',
                  'key':'figure-4-hashjoin-ph-2-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'man'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 manual prefetching:',
                  'key':'figure-4-hashjoin-ph-2-man', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 no prefetching:',
                  'key':'figure-4-hashjoin-ph-8-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 auto prefetching:',
                  'key':'figure-4-hashjoin-ph-8-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'man'},
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 manual prefetching:',
                  'key':'figure-4-hashjoin-ph-8-man', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})




    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 no prefetching:',
                  'key':'figure-4-graph500-s16-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 auto prefetching:',
                  'key':'figure-4-graph500-s16-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'man-inorder'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 manual in order prefetching:',
                  'key':'figure-4-graph500-s16-man-inorder', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'man-outoforder'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 manual out of order prefetching:',
                  'key':'figure-4-graph500-s16-man-outoforder', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 no prefetching:',
                  'key':'figure-4-graph500-s21-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 auto prefetching:',
                  'key':'figure-4-graph500-s21-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'man-inorder'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 manual in order prefetching:',
                  'key':'figure-4-graph500-s21-man-inorder', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'man-outoforder'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q,
                  'title':'',
                  'subtitle':'Validating graph500 manual out of order prefetching:',
                  'key':'figure-4-graph500-s21-man-outoforder', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    return {'return':0}
