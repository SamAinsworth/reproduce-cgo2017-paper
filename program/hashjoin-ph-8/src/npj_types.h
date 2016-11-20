/**
 * @file    npj_types.h
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Tue May 22 16:37:59 2012
 * @version $Id: npj_types.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  Provides type definitions used by No Partitioning Join implementations.
 * 
 */
#ifndef NPO_TYPES_H
#define NPO_TYPES_H

#include "types.h" /* tuple_t */

/**
 * @defgroup NPOTypes Type definitions used by NPO.
 * @{
 */

typedef struct bucket_t        bucket_t;
typedef struct hashtable_t     hashtable_t;
typedef struct bucket_buffer_t bucket_buffer_t;

#if PADDED_BUCKET==0
/** 
 * Normal hashtable buckets.
 *
 * if KEY_8B then key is 8B and sizeof(bucket_t) = 48B
 * else key is 16B and sizeof(bucket_t) = 32B
 */
struct bucket_t {
    volatile char     latch;
    /* 3B hole */
    uint32_t          count;
    tuple_t           tuples[BUCKET_SIZE];
    struct bucket_t * next;
};
#else /* PADDED_BUCKET: bucket is padded to cache line size */
/** 
 * Cache-sized bucket where size of the bucket is padded
 * to cache line size (64B). 
 */
struct bucket_t {
    volatile char     latch;
    /* 3B hole */
    uint32_t          count;
    tuple_t           tuples[BUCKET_SIZE];
    struct bucket_t * next;
} __attribute__ ((aligned(CACHE_LINE_SIZE)));
#endif /* PADDED_BUCKET */

/** Hashtable structure for NPO. */
struct hashtable_t {
    bucket_t * buckets;
    int32_t    num_buckets;
    uint32_t   hash_mask;
    uint32_t   skip_bits;
};

/** Pre-allocated bucket buffers are used for overflow-buckets. */
struct bucket_buffer_t {
    struct  bucket_buffer_t * next;
    uint32_t count;
    bucket_t buf[OVERFLOW_BUF_SIZE];
};

/** @} */

#endif /* NPO_TYPES_H */
