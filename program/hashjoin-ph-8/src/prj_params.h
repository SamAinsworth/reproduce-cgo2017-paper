/**
 * @file    prj_params.h
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Tue May 22 14:03:52 2012
 * @version $Id: prj_params.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  Constant parameters used by Parallel Radix Join implementations.
 * 
 */

#ifndef PRJ_PARAMS_H
#define PRJ_PARAMS_H

/** number of total radix bits used for partitioning. */
#ifndef NUM_RADIX_BITS
#define NUM_RADIX_BITS 14
#endif

/** number of passes in multipass partitioning, currently fixed at 2. */
#ifndef NUM_PASSES
#define NUM_PASSES 2
#endif

/** number of probe items for prefetching: must be a power of 2 */
#ifndef PROBE_BUFFER_SIZE
#define PROBE_BUFFER_SIZE 4
#endif

/** 
 * Whether to use software write-combining optimized partitioning, 
 * see --enable-optimized-part config option 
 */
/* #define USE_SWWC_OPTIMIZED_PART 1 */

/** @defgroup SystemParameters System Parameters
 *  Various system specific parameters such as cache/cache-line sizes,
 *  associativity, etc. 
 *  @{
 */

/** L1 cache parameters. \note Change as needed for different machines */
#ifndef CACHE_LINE_SIZE
#define CACHE_LINE_SIZE 64
#endif

/** L1 cache size */
#ifndef L1_CACHE_SIZE
#define L1_CACHE_SIZE 32768
#endif

/** L1 associativity */
#ifndef L1_ASSOCIATIVITY
#define L1_ASSOCIATIVITY 8
#endif

/** number of tuples fitting into L1 */
#define L1_CACHE_TUPLES (L1_CACHE_SIZE/sizeof(tuple_t))

/** thresholds for skewed partitions in 3-phase parallel join */
#ifndef SKEW_HANDLING
#define SKEW_HANDLING 0
#endif
#define THRESHOLD1(NTHR) (NTHR*L1_CACHE_TUPLES)
#define THRESHOLD2(NTHR) (NTHR*NTHR*L1_CACHE_TUPLES)

/** }*/


/** \internal some padding space is allocated for relations in order to
 *  avoid L1 conflict misses and PADDING_TUPLES is placed between 
 *  partitions in pass-1 of partitioning and SMALL_PADDING_TUPLES is placed
 *  between partitions in pass-2 of partitioning. 3 is a magic number. 
 */

/* num-parts at pass-1 */
#define FANOUT_PASS1 (1 << (NUM_RADIX_BITS/NUM_PASSES))
/* num-parts at pass-1 */
#define FANOUT_PASS2 (1 << (NUM_RADIX_BITS-(NUM_RADIX_BITS/NUM_PASSES)))

/** 
 * Put an odd number of cache lines between partitions in pass-2:
 * Here we put 3 cache lines.
 */
#define SMALL_PADDING_TUPLES (3 * CACHE_LINE_SIZE/sizeof(tuple_t))
#define PADDING_TUPLES (SMALL_PADDING_TUPLES*(FANOUT_PASS2+1))

/** @warning This padding must be allocated at the end of relation */
#define RELATION_PADDING (PADDING_TUPLES*FANOUT_PASS1*sizeof(tuple_t))

/** \endinternal */


#endif /* PRJ_PARAMS_H */
