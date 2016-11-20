/**
 * @file    affinity.h
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Wed Aug  1 14:26:56 2012
 * @version $Id: affinity.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  Affinity methods on Mac OS X. Mac OS X does not export interfaces
 * that identify processors or control thread placement -- explicit thread to
 * processor binding is not supported. So this is just a place holder to compile
 * in Mac OS, experiments should be run in Linux.
 *
 * (c) 2012, ETH Zurich, Systems Group
 *
 */
#ifndef AFFINITY_H
#define AFFINITY_H

#include <pthread.h>            /* pthread_* */
#include "../config.h"          /* HAVE_PTHREAD_ATTR_SETAFFINITY_NP */

#ifndef HAVE_PTHREAD_ATTR_SETAFFINITY_NP

// #include <mach/mach.h>
// #include <mach/thread_policy.h>

#define CPU_ZERO(PTR) (*(PTR) = 0)
#define CPU_SET(N, PTR) (*(PTR) = (N))
#define pthread_attr_setaffinity_np(ATTR, SZ, PTR) setaffinity(ATTR, SZ, PTR)
#define sched_setaffinity(A, SZ, PTR) setaffinity(A, SZ, PTR)

typedef int cpu_set_t;

static int 
setaffinity(pthread_attr_t *attr, size_t cpusetsize, const cpu_set_t *cpuset);

int 
setaffinity(pthread_attr_t *attr, size_t cpusetsize, const cpu_set_t *cpuset)
{
    /* Not implemented */
    /*
    int tid = *cpuset;
    thread_affinity_policy ap;
    ap.affinity_tag = tid;

    int ret = thread_policy_set(
                                  pthread_mach_thread_np(tid),
                                  THREAD_AFFINITY_POLICY,
                                  (integer_t*) &ap,
                                  THREAD_AFFINITY_POLICY_COUNT
                                );
    return ret;
    */

    return 0;

}

#endif

#endif /* AFFINITY_H */
