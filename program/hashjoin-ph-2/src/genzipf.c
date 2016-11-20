/**
 * @file
 *
 * Generate Zipf-distributed input data.
 *
 * @author Jens Teubner <jens.teubner@inf.ethz.ch>
 *
 * (c) ETH Zurich, Systems Group
 *
 * $Id: genzipf.c 3017 2012-12-07 10:56:20Z bcagri $
 */

#include <assert.h>
#include <stdlib.h>
#include <math.h>

#include "genzipf.h"

/**
 * Create an alphabet, an array of size @a size with randomly
 * permuted values 0..size-1.
 *
 * @param size alphabet size
 * @return an <code>item_t</code> array with @a size elements;
 *         contains values 0..size-1 in a random permutation; the
 *         return value is malloc'ed, don't forget to free it afterward.
 */
static uint32_t *
gen_alphabet (unsigned int size)
{
    uint32_t *alphabet;

    /* allocate */
    alphabet = (uint32_t *) malloc (size * sizeof (*alphabet));
    assert(alphabet);

    /* populate */
    for (unsigned int i = 0; i < size; i++)
        alphabet[i] = i+1;   /* don't let 0 be in the alphabet */

    /* permute */
    for (unsigned int i = size-1; i > 0; i--)
    {
        unsigned int k = (unsigned long) i * rand () / RAND_MAX;
        unsigned int tmp;

        tmp = alphabet[i];
        alphabet[i] = alphabet[k];
        alphabet[k] = tmp;
    }

    return alphabet;
}

/**
 * Generate a lookup table with the cumulated density function
 *
 * (This is derived from code originally written by Rene Mueller.)
 */
static double *
gen_zipf_lut (double zipf_factor, unsigned int alphabet_size)
{
    double scaling_factor;
    double sum;

    double *lut;              /**< return value */

    lut = (double *) malloc (alphabet_size * sizeof (*lut));
    assert (lut);

    /*
     * Compute scaling factor such that
     *
     *   sum (lut[i], i=1..alphabet_size) = 1.0
     *
     */
    scaling_factor = 0.0;
    for (unsigned int i = 1; i <= alphabet_size; i++)
        scaling_factor += 1.0 / pow (i, zipf_factor);

    /*
     * Generate the lookup table
     */
    sum = 0.0;
    for (unsigned int i = 1; i <= alphabet_size; i++)
    {
        sum += 1.0 / pow (i, zipf_factor);
        lut[i-1] = sum / scaling_factor;
    }

    return lut;
}

/**
 * Generate a stream with Zipf-distributed content.
 */
item_t *
gen_zipf (unsigned int stream_size,
          unsigned int alphabet_size,
          double zipf_factor,
          item_t ** output)
{
    item_t *ret;

    /* prepare stuff for Zipf generation */
    uint32_t  *alphabet = gen_alphabet (alphabet_size);
    assert (alphabet);

    double  *lut = gen_zipf_lut (zipf_factor, alphabet_size);
    assert (lut);

    if(*output == NULL)
        ret = (item_t *) malloc (stream_size * sizeof (*ret));
    else
        ret = *output;

    assert (ret);

    for (unsigned int i = 0; i < stream_size; i++)
    {
        /* take random number */
        double       r     = ((double) rand ()) / RAND_MAX;

        /* binary search in lookup table to determine item */
        unsigned int left  = 0;
        unsigned int right = alphabet_size - 1;
        unsigned int m;       /* middle between left and right */
        unsigned int pos;     /* position to take */

        if (lut[0] >= r)
            pos = 0;
        else
        {
            while (right - left > 1)
            {
                m = (left + right) / 2;

                if (lut[m] < r)
                    left = m;
                else
                    right = m;
            }

            pos = right;
        }

        uint32_t * dst = (uint32_t *)&ret[i];
        *dst = alphabet[pos];
        /* ret[i] = alphabet[pos]; */
    }

    free (lut);
    free (alphabet);

    *output = ret;

    return ret;
}
