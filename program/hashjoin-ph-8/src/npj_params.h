/**
 * @file    npj_params.h
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Tue May 22 13:39:58 2012
 * @version $Id: npj_params.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  Constant parameters used by No Partitioning Join implementations.
 * 
 */
#ifndef NPJ_PARAMS_H
#define NPJ_PARAMS_H
// DEBUG
// KEY_8B
// NO_TIMING
// PREFETCH_NPJ

/** Number of tuples that each bucket can hold */
#ifndef BUCKET_SIZE
#define BUCKET_SIZE 2
#endif

/** Size of system cache line in bytes */
#ifndef CACHE_LINE_SIZE
#define CACHE_LINE_SIZE 64
#endif

/** Pre-allocation size for overflow buffers */
#ifndef OVERFLOW_BUF_SIZE
#define OVERFLOW_BUF_SIZE 1024 
#endif

/** Should hashtable buckets be padded to cache line size */
#ifndef PADDED_BUCKET
#define PADDED_BUCKET 0 /* default case: not padded */
#endif

#ifndef PREFETCH_DISTANCE
#define PREFETCH_DISTANCE 32
#endif

#endif /* NPJ_PARAMS_H */
