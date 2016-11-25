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

form_name='wa_web_form'
onchange='document.'+form_name+'.submit();'

benchmarks=['nas-cg','nas-is','graph500-s16','graph500-s21','hashjoin-ph-2','hashjoin-ph-8','randacc']


##############################################################################
# Sorting

import re
def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return float(m.group()) if m else 0


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
              program_uoa       - program UID or alias

              (deps)            - pre-resolved deps
              (env)             - compile/run environment
              (cmd)             - if !='', use as cmd_key

              (quiet)           - if 'yes', do not ask to press enter
              (title)           - print title (and record to log)

              (results)         - dict with results
              (key)             - key to check results

              (record)          - if 'yes', record results
              (record_repo_uoa) - repo where to record
              (record_data_uoa) - data where to record
              (os_abi)          - OS ABI to record in dict
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

    rec=i.get('record','')
    rruoa=i.get('record_repo_uoa','')
    rduoa=i.get('record_data_uoa','')

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
    os_abi=i.get('os_abi','')
    dd=i.get('results',{})
    results=dd.get(os_abi,{})

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
    for x in range(0,3):
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
    tmean=float(sum(times))/max(len(times),1)

    stmin='%.4f' % tmin
    stmax='%.4f' % tmax
    stmean='%.4f' % tmean

    # Check if results exist:
    estmin='' # expected min
    estmax='' # expected max
    estmean='' # expected max
    if key!='':
       x=results.get(key,{}).get('stmin','')
       if x!='': estmin=' (from paper: '+x+')'
       x=results.get(key,{}).get('stmax','')
       if x!='': estmax=' (from paper: '+x+')'
       x=results.get(key,{}).get('stmean','')
       if x!='': estmean=' (from paper: '+x+')'

       # Check pre-record results or write to temporal evaluator entry
       if rec=='yes':
          if key not in results:
             results[key]={}
          results[key]['stmin']=stmin
          results[key]['stmax']=stmax
          results[key]['stmean']=stmean

          dd['tags']=["cgo2017","sw-prefetch"]

          # Update result entry
          r=ck.access({'action':'update',
                       'module_uoa':cfg['module_deps']['result'],
                       'repo_uoa':rruoa,
                       'data_uoa':rduoa,
                       'substitute':'yes',
                       'sort_keys':'yes',
                       'ignore_update':'yes',
                       'dict':dd})
          if r['return']>0: return r

       else:
          # Load local result if exists
          dlocal={}
          r=ck.access({'action':'load',
                       'module_uoa':cfg['module_deps']['result'],
                       'data_uoa':cfg['recorded-result-uoa']})
          if r['return']==0: 
             dlocal=r['dict']

          if os_abi not in dlocal:
             dlocal[os_abi]={}

          if key not in dlocal[os_abi]:
             dlocal[os_abi][key]={}

          dlocal[os_abi][key]['stmin']=stmin
          dlocal[os_abi][key]['stmax']=stmax
          dlocal[os_abi][key]['stmean']=stmean

          dlocal['tags']=["cgo2017","sw-prefetch"]

          r=ck.access({'action':'update',
                       'module_uoa':cfg['module_deps']['result'],
                       'data_uoa':cfg['recorded-result-uoa'],
                       'substitute':'yes',
                       'sort_keys':'yes',
                       'ignore_update':'yes',
                       'dict':dlocal})
          if r['return']>0: return r

    # Print
    log({'string':'', 'out':'yes'})
    log({'string':'Min  execution time: '+stmin+estmin, 'out':'yes'})
    log({'string':'Max  execution time: '+stmax+estmax, 'out':'yes'})
    log({'string':'Mean execution time: '+stmean+estmean, 'out':'yes'})

    return {'return':0, 'times':times, 'tmin':tmin, 'tmax':tmax, 'stmin':stmin, 'stmax':stmax}

##############################################################################
# run workflow

def run(i):
    """
    Input:  {
              (quiet)  - if 'yes', do not ask questions (useful to save output)
              (record) - if 'yes', record results
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
    rec=i.get('record','')

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
    rruid=r['repo_uid']
    rduid=r['data_uid']
    results=r['dict']

    if len(results.get(os_abi,{}))==0:
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-is big:',
                  'key':'figure-2-nas-is-offset-2048', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':64},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
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
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 manual out of order prefetching:',
                  'key':'figure-4-graph500-s21-man-outoforder', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})


    # Reproducing Figure 5 ###################################################################################


    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'Reproducing experiments for Figure 5',
                  'subtitle':'Validating nas-cg no prefetching:',
                  'key':'figure-5-nas-cg-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-cg auto prefetching:',
                  'key':'figure-5-nas-cg-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-cg auto-nostride prefetching:',
                  'key':'figure-5-nas-cg-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-is no prefetching:',
                  'key':'figure-5-nas-is-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-is auto prefetching:',
                  'key':'figure-5-nas-is-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-is auto-nostride prefetching:',
                  'key':'figure-5-nas-is-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})


    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating randacc no prefetching:',
                  'key':'figure-5-randacc-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating randacc auto prefetching:',
                  'key':'figure-5-randacc-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating randacc auto-nostride prefetching:',
                  'key':'figure-5-randacc-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 no prefetching:',
                  'key':'figure-5-hashjoin-ph-2-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 auto prefetching:',
                  'key':'figure-5-hashjoin-ph-2-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 auto-nostride prefetching:',
                  'key':'figure-5-hashjoin-ph-2-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 no prefetching:',
                  'key':'figure-5-hashjoin-ph-8-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 auto prefetching:',
                  'key':'figure-5-hashjoin-ph-8-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 auto-nostride prefetching:',
                  'key':'figure-5-hashjoin-ph-8-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 no prefetching:',
                  'key':'figure-5-graph500-s16-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 auto prefetching:',
                  'key':'figure-5-graph500-s16-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'cmd':'s16e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 auto-nostride prefetching:',
                  'key':'figure-5-graph500-s16-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})



    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 no prefetching:',
                  'key':'figure-5-graph500-s21-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 auto prefetching:',
                  'key':'figure-5-graph500-s21-auto', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['graph500'],
                  'env':{'CK_COMPILE_TYPE':'auto-nostride'},
                  'cmd':'s21e10',
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating graph500 auto-nostride prefetching:',
                  'key':'figure-5-graph500-s21-auto-nostride', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    # Reproducing Figure 6 ###################################################################################
    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'Reproducing experiments for Figure 5',
                  'subtitle':'Validating nas-is no prefetching:',
                  'key':'figure-6-nas-is-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    for x in [2, 4, 8, 16, 32, 64, 128, 256]:
            r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':str(x)},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-is prefetching distance: ' + str(x),
                  'key':'figure-6-nas-is-prefetching-dist-' + str(x), 'results':results})
            if r['return']>0:
                log({'string':''})
                log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-cg no prefetching:',
                  'key':'figure-6-nas-cg-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    for x in [2, 4, 8, 16, 32, 64, 128, 256]:
            r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-cg'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':str(x)},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating nas-cg prefetching distance: ' + str(x),
                  'key':'figure-6-nas-cg-prefetching-dist-' + str(x), 'results':results})
            if r['return']>0:
                log({'string':''})
                log({'string':'Experiment failed ('+r['error']+')'})

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating randacc no prefetching:',
                  'key':'figure-6-randacc-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})

    for x in [2, 4, 8, 16, 32, 64, 128, 256]:
            r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['randacc'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':str(x)},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating randacc prefetching distance: ' + str(x),
                  'key':'figure-6-randacc-prefetching-dist-' + str(x), 'results':results})
            if r['return']>0:
                log({'string':''})
                log({'string':'Experiment failed ('+r['error']+')'})


    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 no prefetching:',
                  'key':'figure-6-hashjoin-ph-2-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})


    for x in [2, 4, 8, 16, 32, 64, 128, 256]:
            r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-2'],
                  'env':{'CK_COMPILE_TYPE':'offset', 'CK_FETCHDIST':str(x)},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-2 prefetching distance: ' + str(x),
                  'key':'figure-6-hashjoin-ph-2-prefetching-dist-' + str(x), 'results':results})
            if r['return']>0:
                log({'string':''})
                log({'string':'Experiment failed ('+r['error']+')'})

    # Reproducing Figure 7 ###################################################################################

    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'Reproducing Experiments for Figure 7',
                  'subtitle':'Validating hashjoin-ph-8 no prefetching:',
                  'key':'figure-7-hashjoin-ph-8-no-prefetching', 'results':results})
    if r['return']>0:
        log({'string':''})
        log({'string':'Experiment failed ('+r['error']+')'})


    for x in [1, 2, 3, 4]:
            r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['hashjoin-ph-8'],
                  'env':{'CK_COMPILE_TYPE':'prefetches', 'CK_NUMPREFETCHES':str(x)},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'',
                  'subtitle':'Validating hashjoin-ph-8 prefetching elements: ' + str(x),
                  'key':'figure-7-hashjoin-ph-8-prefetching-elements-' + str(x), 'results':results})
            if r['return']>0:
                log({'string':''})
                log({'string':'Experiment failed ('+r['error']+')'})

    return {'return':0}

##############################################################################
# open PLUTON dashboard

def dashboard(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    i['action']='browser'
    i['cid']=''
    i['module_uoa']=''
    i['template']='cgo2017'

    return ck.access(i)

##############################################################################
# show experiment dashboard

def show(i):
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
    import copy

    st=''
    ckey=''

    h='<center>\n'
    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

    # Check host URL prefix and default module/action
    rx=ck.access({'action':'form_url_prefix',
                  'module_uoa':cfg['module_deps']['wfe'],
                  'host':i.get('host',''), 
                  'port':i.get('port',''), 
                  'template':i.get('template','')})
    if rx['return']>0: return rx
    url0=rx['url']
    template=rx['template']

    url=url0
    action=i.get('action','')
    muoa=i.get('module_uoa','')

    st=''

    url+='action=index&module_uoa=wfe&native_action='+action+'&'+'native_module_uoa='+muoa
    url1=url

    # List entries
    ii={'action':'search',
        'module_uoa':cfg['module_deps']['result'],
        'add_meta':'yes',
        'tags':'cgo2017,sw-prefetch'}
    r=ck.access(ii)
    if r['return']>0: return r

    lst=r['lst']

    # Check unique entries
    wchoices=[]

    for q in lst:
        d=q['meta']
        for k in d:
            if k!='tags' and len(d[k])>0:
               wchoices.append({'name':k, 'value':k})

    # Prepare query div ***************************************************************
    # Start form + URL (even when viewing entry)
    r=ck.access({'action':'start_form',
                 'module_uoa':cfg['module_deps']['wfe'],
                 'url':url1,
                 'name':form_name})
    if r['return']>0: return r
    h+=r['html']

    cpu_abi='cpu_abi'
    v=''
    if i.get(cpu_abi,'')!='':
        v=i[cpu_abi]

    # If ABI is not selected, try to detect the one of current machine 
    # if user runs experiments on the same one
    if v=='':
       ii={'action':'detect',
           'module_uoa':cfg['module_deps']['platform'],
           'exchange':'no'}
       r=ck.access(ii)
       if r['return']>0: return r

       pft=r['features']

       v=pft.get('os',{}).get('abi','').lower()

    if v=='' and len(wchoices)>0:
       v=wchoices[0]['value']

    # Show hardware
    ii={'action':'create_selector',
        'module_uoa':cfg['module_deps']['wfe'],
        'data':wchoices,
        'name':cpu_abi,
        'onchange':onchange, 
        'skip_sort':'no',
        'selected_value':v}
    r=ck.access(ii)
    if r['return']>0: return r

    h+='<b>Select CPU ABI:</b> '+r['html'].strip()+'\n'

    # Check min or mean
    var='st'
    vx='stmean'
    if i.get(var,'')!='':
        vx=i[var]

    # Show min or mean selector
    ii={'action':'create_selector',
        'module_uoa':cfg['module_deps']['wfe'],
        'data':[{'name':'minimal execution time', 'value':'stmin'},{'name':'max execution time', 'value':'stmax'},{'name':'mean execution time', 'value':'stmean'}],
        'name':var,
        'onchange':onchange, 
        'skip_sort':'no',
        'selected_value':vx}
    r=ck.access(ii)
    if r['return']>0: return r

    h+='<b>which value:</b> '+r['html'].strip()+'\n'


    h+='<br><br>'

    # Check if found
    llst=len(lst)
    if llst==0:
        h+='<b>No results found!</b>'
        return {'return':0, 'html':h, 'style':st}

    # Preparing figures
    figures={}
    noes = {}

    #h+=str(len(lst))

    for q in lst:
        duid=q['data_uid'] # Uid of the entry
        meta=q['meta']
        results=meta.get(v,{})
        
        for k in sorted(results):
            res=results[k]
            # Get figure from key "figure-2-nas-is-offset-2048"
            if k.startswith('figure-'):
               j=k.find('-',7)
               if j>0:
                  fig=k[7:j]
                  ext=k[j+1:].strip()

                  # Check which benchmark
                  bench=''
                  for b in benchmarks:
                      if ext.startswith(b):
                         bench=b
                         break

                  if fig not in noes:
                     noes[fig]={}
                     
                  if bench not in noes[fig]:
                     noes[fig][bench]={}

                  if(ext.endswith('no-prefetching')):
                     noes[fig][bench][duid]=res.get('stmean',None)

        
        for k in sorted(results):
            res=results[k]
            # Get figure from key "figure-2-nas-is-offset-2048"
            if k.startswith('figure-'):
               j=k.find('-',7)
               if j>0:
                  fig=k[7:j]
                  ext=k[j+1:].strip()

                  # Check which benchmark
                  bench=''
                  for b in benchmarks:
                      if ext.startswith(b):
                         bench=b
                         break

                  if fig not in figures:
                     figures[fig]={}

                  if bench not in figures[fig]:
                     figures[fig][bench]={}

                  if(not ext.endswith('no-prefetching')):

                     if ext not in figures[fig][bench]:
                        figures[fig][bench][ext]={}
    
                     figures[fig][bench][ext][duid]=res.get(vx,None)

    # Draw figures
    h+='<i>Please, check the tendency, not exact match!</i><br>'
    h+='<i> Prerecorded aarch64 results are for A57, not A53: In order architectures will perform similar to as shown in the paper.</i><br><br>'
    h+='<span style="color:#1f77b4">Blue color bars - results pre-recorded by the authors</span><br>'
    h+='<span style="color:#ff7f0e">Orange color bars - results by artifact evaluators</span><br>'

    for fig in sorted(figures):
        h+='<hr>'

        for bench in sorted(figures[fig]):

            h+='<br><b>Figure '+fig+' ('+bench+')</b><br><br>'

            ix=0
            bgraph={'0':[], '1':[]}
            legend=''

            for ext in sorted(figures[fig][bench], key = get_trailing_number) if fig!=6 else sorted(figures[fig][bench], key = get_trailing_number) :
                ix+=1

                bgraph['0'].append([ix,float(noes[fig][bench].get(cfg['pre-recorded-result-uoa'],'0'))/float(figures[fig][bench][ext].get(cfg['pre-recorded-result-uoa'],'100000000'))])
                bgraph['1'].append([ix,float(noes[fig][bench].get(cfg['recorded-result-uoa'],'0'))/float(figures[fig][bench][ext].get(cfg['recorded-result-uoa'],'100000000'))])

                legend+=str(ix)+') '+ext+'<br>'

            ii={'action':'plot',
                'module_uoa':cfg['module_deps']['graph'],

                "table":bgraph,

                "ymin":0,

                "ignore_point_if_none":"yes",

                "plot_type":"d3_2d_bars",

                "display_y_error_bar":"no",

                "title":"Powered by Collective Knowledge",

                "axis_x_desc":"Experiment",
                "axis_y_desc":"Speedup",

                "plot_grid":"yes",

                "d3_div":"ck_interactive_"+fig+'_'+bench,

                "image_width":"900",
                "image_height":"400",

                "wfe_url":url0}

            r=ck.access(ii)
            if r['return']==0:
               x=r.get('html','')
               if x!='':
                  st+=r.get('style','')

                  h+='<br>\n'
                  h+='<center>\n'
                  h+='<div id="ck_box_with_shadow" style="width:920px;">\n'
                  h+=' <div id="ck_interactive_'+fig+'_'+bench+'" style="text-align:center">\n'
                  h+=x+'\n'

                  h+=legend+'<br>'
                  h+=' </div>\n'
                  h+='</div>\n'
                  h+='</center>\n'

    h+='</center>\n'

    h+='</form>\n'

    return {'return':0, 'html':h, 'style':st}
