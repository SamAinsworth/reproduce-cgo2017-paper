/**
 * @file    genzipf.h
 * @version $Id: genzipf.h 3017 2012-12-07 10:56:20Z bcagri $
 *
 * Data generation with Zipf distribution.
 *
 * @author Jens Teubner <jens.teubner@inf.ethz.ch>
 *
 * (c) 2011 ETH Zurich, Systems Group
 *
 * $Id: genzipf.h 3017 2012-12-07 10:56:20Z bcagri $
 */

#ifndef GENZIPF_H
#define GENZIPF_H

#include "types.h" /* tuple_t */

typedef tuple_t item_t;

item_t * gen_zipf (unsigned int stream_size,
                   unsigned int alphabet_size,
                   double zipf_factor,
                   item_t ** output);

#endif  /* GENZIPF_H */
