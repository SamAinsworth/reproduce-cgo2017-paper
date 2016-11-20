/**
 * @file    main.c
 * @author  Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 * @date    Wed May 16 16:03:10 2012
 * @version $Id: main.c 3017 2012-12-07 10:56:20Z bcagri $
 *
 * @brief  Main entry point for running join implementations with given command
 * line parameters.
 * 
 * (c) 2012, ETH Zurich, Systems Group
 * 
 * @mainpage Main-Memory Hash Joins On Multi-Core CPUs: Tuning to the Underlying Hardware
 *
 * @section intro Introduction
 *
 * This package provides implementations of the main-memory hash join algorithms
 * described and studied in our ICDE 2013 paper. Namely, the implemented
 * algorithms are the following with the abbreviated names:
 * 
 *  - NPO:    No Partitioning Join Optimized (Hardware-oblivious algo. in paper)
 *  - PRO:    Parallel Radix Join Optimized (Hardware-conscious algo. in paper)
 *  - PRH:    Parallel Radix Join Histogram-based
 *  - PRHO:   Parallel Radix Join Histogram-based Optimized
 *  - RJ:     Radix Join (single-threaded)
 *  - NPO_st: No Partitioning Join Optimized (single-threaded)
 *
 * @section compilation Compilation
 *
 * The package includes implementations of the algorithms and also the driver
 * code to run and repeat the experimental studies described in the paper.
 * 
 * The code has been written using standard GNU tools and uses autotools
 * for configuration. Thus, compilation should be as simple as:
 * 
 * @verbatim
       $ ./configure
       $ make
@endverbatim
 * 
 * Besides the usual ./configure options, compilation can be customized with the
 * following options:
 * @verbatim
   --enable-debug         enable debug messages on commandline  [default=no]
   --enable-key8B         use 8B keys and values making tuples 16B  [default=no]
   --enable-perfcounters  enable performance monitoring with Intel PCM  [no]
   --enable-paddedbucket  enable padding of buckets to cache line size in NPO [no]
   --enable-timing        enable execution timing  [default=yes]
   --enable-syncstats     enable synchronization timing stats  [default=no]
   --enable-skewhandling  enable fine-granular task decomposition based skew handling in radix [default=no]
@endverbatim
 * Additionally, the code can be configured to enable further optimizations
 * discussed in the Technical Report version of the paper:
 * @verbatim
   --enable-prefetch-npj   enable prefetching in no partitioning join [default=no]
   --enable-swwc-part      enable software write-combining optimization in
                           partitioning (Experimental, not tested extensively) ? [default=no]
@endverbatim
 * Our code makes use of the Intel Performance Counter Monitor tool which was
 * slightly modified to be integrated in to our implementation. The original
 * code can be downloaded from:
 * 
 * http://software.intel.com/en-us/articles/intel-performance-counter-monitor/
 * 
 * We are providing the copy that we used for our experimental study under
 * <b>`lib/intel-pcm-1.7`</b> directory which comes with its own Makefile. Its
 * build process is actually separate from the autotools build process but with
 * the <tt>--enable-perfcounters</tt> option, make command from the top level
 * directory also builds the shared library <b>`libperf.so'</b> that we link to
 * our code. After compiling with --enable-perfcounters, in order to run the
 * executable add `lib/intel-pcm-1.7/lib' to your
 * <tt>LD_LIBRARY_PATH</tt>. In addition, the code must be run with
 * root privileges to acces model specific registers, probably after
 * issuing the following command: `modprobe msr`. Also note that with
 * --enable-perfcounters the code is compiled with g++ since Intel
 * code is written in C++. 
 * 
 * We have successfully compiled and run our code on different Linux
 * variants; the experiments in the paper were performed on Debian and Ubuntu
 * Linux systems.
 * 
 * @section usage Usage and Invocation
 *
 * The <tt>mchashjoins</tt> binary understands the following command line
 * options: 
 * @verbatim
      Join algorithm selection, algorithms : RJ, PRO, PRH, PRHO, NPO, NPO_st
         -a --algo=<name>    Run the hash join algorithm named <name> [PRO]
 
      Other join configuration options, with default values in [] :
         -n --nthreads=<N>  Number of threads to use <N> [2]
         -r --r-size=<R>    Number of tuples in build relation R <R> [128000000]
         -s --s-size=<S>    Number of tuples in probe relation S <S> [128000000]
         -x --r-seed=<x>    Seed value for generating relation R <x> [12345]    
         -y --s-seed=<y>    Seed value for generating relation S <y> [54321]    
         -z --skew=<z>      Zipf skew parameter for probe relation S <z> [0.0]  
         --non-unique       Use non-unique (duplicated) keys in input relations 
         --full-range       Spread keys in relns. in full 32-bit integer range
         --basic-numa       Numa-localize relations to threads (Experimental)

      Performance profiling options, when compiled with --enable-perfcounters.
         -p --perfconf=<P>  Intel PCM config file with upto 4 counters [none]  
         -o --perfout=<O>   Output file to print performance counters [stdout]
 
      Basic user options
          -h --help         Show this message
          --verbose         Be more verbose -- show misc extra info 
          --version         Show version

@endverbatim
 * The above command line options can be used to instantiate a certain
 * configuration to run various joins and print out the resulting
 * statistics. Following the same methodology of the related work, our joins
 * never materialize their results as this would be a common cost for all
 * joins. We only count the number of matching tuples and report this. In order
 * to materialize results, one needs to copy results to a result buffer in the
 * corresponding locations of the source code.
 *
 * @section config Configuration Parameters
 *
 * @subsection cpumapping Logical to Pyhsical CPU Mapping
 *
 * If running on a machine with multiple CPU sockets and/or SMT feature enabled,
 * then it is necessary to identify correct mappings of CPUs on which threads
 * will execute. For instance one of our experiment machines, Intel Xeon L5520
 * had 2 sockets and each socket had 4 cores and 8 threads. In order to only
 * utilize the first socket, we had to use the following configuration for
 * mapping threads 1 to 8 to correct CPUs:
 * 
 * @verbatim
cpu-mapping.txt
8 0 1 2 3 8 9 10 11
@endverbatim
 * 
 * This file is must be created in the executable directory and used by default 
 * if exists in the directory. It basically says that we will use 8 CPUs listed 
 * and threads spawned 1 to 8 will map to the given list in order. For instance 
 * thread 5 will run CPU 8. This file must be changed according to the system at
 * hand. If it is absent, threads will be assigned round-robin. This CPU mapping
 * utility is also integrated into the Wisconsin implementation (found in 
 * `wisconsin-src') and same settings are also valid there.
 * 
 * @subsection perfmonitoring Performance Monitoring
 *
 * For performance monitoring a config file can be provided on the command line
 * with --perfconf which specifies which hardware counters to monitor. For 
 * detailed list of hardware counters consult to "Intel 64 and IA-32 
 * Architectures Software Developer’s Manual" Appendix A. For an example 
 * configuration file used in the experiments, see <b>`pcm.cfg'</b> file. 
 * Lastly, an output file name with --perfout on commandline can be specified to
 * print out profiling results, otherwise it defaults to stdout.
 *
 * @subsection systemparams System and Implementation Parameters
 *
 * The join implementations need to know about the system at hand to a certain
 * degree. For instance #CACHE_LINE_SIZE is required by both of the
 * implementations. In case of no partitioning join, other implementation
 * parameters such as bucket size or whether to pre-allocate for overflowing
 * buckets are parametrized and can be modified in `npj_params.h'.
 * 
 * On the other hand, radix joins are more sensitive to system parameters and 
 * the optimal setting of parameters should be found from machine to machine to 
 * get the same results as presented in the paper. System parameters needed are
 * #CACHE_LINE_SIZE, #L1_CACHE_SIZE and
 * #L1_ASSOCIATIVITY. Other implementation parameters specific to radix
 * join are also important such as #NUM_RADIX_BITS
 * which determines number of created partitions and #NUM_PASSES which
 * determines number of partitioning passes. Our implementations support between
 * 1 and 2 passes and they can be configured using these parameters to find the
 * ideal performance on a given machine.
 *
 * @section data Generating Data Sets of Our Experiments
 *
 * Here we briefly describe how to generate data sets used in our experiments 
 * with the command line parameters above.
 *
 * @subsection workloadB Workload B 
 * 
 * In this data set, the inner relation R and outer relation S have 128*10^6 
 * tuples each. The tuples are 8 bytes long, consisting of 4-byte (or 32-bit) 
 * integers and a 4-byte payload. As for the data distribution, if not 
 * explicitly specified, we use relations with randomly shuffled unique keys 
 * ranging from 1 to 128*10^6. To generate this data set, append the following 
 * parameters to the executable
 * <tt>mchashjoins</tt>:
 *
 * @verbatim
      $ ./mchashjoins [other options] --r-size=128000000 --s-size=128000000 
@endverbatim 
 *
 * \note Configure must have run without --enable-key8B.
 * 
 * @subsection workloadA Workload A
 * 
 * This data set reflects the case where the join is performed between the 
 * primary key of the inner relation R and the foreign key of the outer relation
 * S. The size of R is fixed at 16*2^20 and size of S is fixed at 256*2^20. 
 * The ratio of the inner relation to the outer relation is 1:16. In this data 
 * set, tuples are represented as (key, payload) pairs of 8 bytes each, summing 
 * up to 16 bytes per tuple. To generate this data set do the following:
 * 
 * @verbatim
     $ ./configure --enable-key8B
     $ make
     $ ./mchashjoins [other options] --r-size=16777216 --s-size=268435456 
@endverbatim 
 * 
 * @subsection skew Introducing Skew in Data Sets
 * 
 * Skew can be introduced to the relation S as in our experiments by appending 
 * the following parameter to the command line, which is basically a Zipf 
 * distribution skewness parameter:
 * 
 * @verbatim
     $ ./mchashjoins [other options] --skew=1.05
@endverbatim
 *
 * @section wisconsin Wisconsin Implementation
 *
 * A slightly modified version of the original implementation provided by 
 * Blanas et al. from University of Wisconsin is provided under `wisconsin-src'
 * directory. The changes we made are documented in the header of the README 
 * file. These implementations provide the algorithms mentioned as 
 * `non-optimized no partitioning join' and `non-optimized radix join' in our 
 * paper. The original source code can be downloaded from 
 * http://pages.cs.wisc.edu/∼sblanas/files/multijoin.tar.bz2 .
 *
 *
 *
 * @author Cagri Balkesen <cagri.balkesen@inf.ethz.ch>
 *
 * (c) 2012, ETH Zurich, Systems Group
 *
 */

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <sched.h>              /* sched_setaffinity */
#include <stdio.h>              /* printf */
#include <sys/time.h>           /* gettimeofday */
#include <getopt.h>             /* getopt */
#include <stdlib.h>             /* exit */
#include <string.h>             /* strcmp */
#include <limits.h>             /* INT_MAX */

#include "no_partitioning_join.h" /* no partitioning joins: NPO, NPO_st */
#include "parallel_radix_join.h"  /* parallel radix joins: RJ, PRO, PRH, PRHO */
#include "generator.h"            /* create_relation_xk */

#include "perf_counters.h" /* PCM_x */
#include "affinity.h"      /* pthread_attr_setaffinity_np & sched_setaffinity */
#include "../config.h"     /* autoconf header */

#if !defined(__cplusplus)
int getopt(int argc, char * const argv[],
           const char *optstring);
#endif

typedef struct algo_t  algo_t;
typedef struct param_t param_t;

struct algo_t {
    char name[128];
    int64_t (*joinAlgo)(relation_t * , relation_t *, int);
};

struct param_t {
    algo_t * algo;
    uint32_t nthreads;
    uint32_t r_size;
    uint32_t s_size;
    uint32_t r_seed;
    uint32_t s_seed;
    double skew;
    int nonunique_keys;  /* non-unique keys allowed? */
    int verbose;
    int fullrange_keys;  /* keys covers full int range? */
    int basic_numa;/* alloc input chunks thread local? */
    char * perfconf;
    char * perfout;
};

extern char * optarg;
extern int    optind, opterr, optopt;

/** An experimental feature to allocate input relations numa-local */
extern int numalocalize;  /* defined in generator.c */
extern int nthreads;      /* defined in generator.c */

/** all available algorithms */
static struct algo_t algos [] = 
  {
      {"PRO", PRO},
      {"RJ", RJ},
      {"PRH", PRH},
      {"PRHO", PRHO},
      {"NPO", NPO},
      {"NPO_st", NPO_st}, /* NPO single threaded */
      {{0}, 0}
  };

/* command line handling functions */
void 
print_help();

void
print_version();

void 
parse_args(int argc, char ** argv, param_t * cmd_params);

int 
main(int argc, char ** argv)
{
    relation_t relR;
    relation_t relS;
    int64_t    results;

    /* start initially on CPU-0 */
    /*cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(0, &set);
    if (sched_setaffinity(0, sizeof(set), &set) <0) {
        perror("sched_setaffinity");
    }*/

    /* Command line parameters */
    param_t cmd_params;

    /* Default values if not specified on command line */
    cmd_params.algo     = &algos[0]; /* PRO */
    cmd_params.nthreads = 2;
    /* default dataset is Workload B (described in paper) */
    cmd_params.r_size   = 128000000;
    cmd_params.s_size   = 128000000;
    cmd_params.r_seed   = 12345;
    cmd_params.s_seed   = 54321;
    cmd_params.skew     = 0.0;
    cmd_params.verbose  = 0;
    cmd_params.perfconf = NULL;
    cmd_params.perfout  = NULL;
    cmd_params.nonunique_keys   = 0;
    cmd_params.fullrange_keys   = 0;
    cmd_params.basic_numa = 0;

    parse_args(argc, argv, &cmd_params);

#ifdef PERF_COUNTERS
    PCM_CONFIG = cmd_params.perfconf;
    PCM_OUT    = cmd_params.perfout;
#endif
    
    /* create relation R */
    fprintf(stdout,
            "[INFO ] Creating relation R with size = %.3lf MiB, #tuples = %d : ",
            (double) sizeof(tuple_t) * cmd_params.r_size/1024.0/1024.0,
            cmd_params.r_size);
    fflush(stdout);

    seed_generator(cmd_params.r_seed);

    /* to pass information to the create_relation methods */
    numalocalize = cmd_params.basic_numa;
    nthreads     = cmd_params.nthreads;

    if(cmd_params.fullrange_keys) {
        create_relation_nonunique(&relR, cmd_params.r_size, INT_MAX);
    }
    else if(cmd_params.nonunique_keys) {
        create_relation_nonunique(&relR, cmd_params.r_size, cmd_params.r_size);
    }
    else {
        create_relation_pk(&relR, cmd_params.r_size);
    }
    printf("OK \n");


    /* create relation S */
    fprintf(stdout,
            "[INFO ] Creating relation S with size = %.3lf MiB, #tuples = %d : ",
            (double) sizeof(tuple_t) * cmd_params.s_size/1024.0/1024.0,
            cmd_params.s_size);
    fflush(stdout);

    seed_generator(cmd_params.s_seed);

    if(cmd_params.fullrange_keys) {
        create_relation_fk_from_pk(&relS, &relR, cmd_params.s_size);
    }
    else if(cmd_params.nonunique_keys) {
        /* use size of R as the maxid */
        create_relation_nonunique(&relS, cmd_params.s_size, cmd_params.r_size);
    }
    else {
        /* if r_size == s_size then equal-dataset, else non-equal dataset */

        if(cmd_params.skew > 0){
            /* S is skewed */
            create_relation_zipf(&relS, cmd_params.s_size, 
                                 cmd_params.r_size, cmd_params.skew);
        }
        else {
            /* S is uniform foreign key */
            create_relation_fk(&relS, cmd_params.s_size, cmd_params.r_size);
        }
    }
    printf("OK \n");


    /* Run the selected join algorithm */
    printf("[INFO ] Running join algorithm %s ...\n", cmd_params.algo->name);

    results = cmd_params.algo->joinAlgo(&relR, &relS, cmd_params.nthreads);

    printf("[INFO ] Results = %llu. DONE.\n", results);

    /* clean-up */
    delete_relation(&relR);
    delete_relation(&relS);

    return 0;
}

/* command line handling functions */
void 
print_help(char * progname)
{
    printf("Usage: %s [options]\n", progname);

    printf("\
    Join algorithm selection, algorithms : RJ, PRO, PRH, PRHO, NPO, NPO_st    \n\
       -a --algo=<name>    Run the hash join algorithm named <name> [PRO]     \n\
                                                                              \n\
    Other join configuration options, with default values in [] :             \n\
       -n --nthreads=<N>  Number of threads to use <N> [2]                    \n\
       -r --r-size=<R>    Number of tuples in build relation R <R> [128000000]\n\
       -s --s-size=<S>    Number of tuples in probe relation S <S> [128000000]\n\
       -x --r-seed=<x>    Seed value for generating relation R <x> [12345]    \n\
       -y --s-seed=<y>    Seed value for generating relation S <y> [54321]    \n\
       -z --skew=<z>      Zipf skew parameter for probe relation S <z> [0.0]  \n\
       --non-unique       Use non-unique (duplicated) keys in input relations \n\
       --full-range       Spread keys in relns. in full 32-bit integer range  \n\
       --basic-numa       Numa-localize relations to threads (Experimental)   \n\
                                                                              \n\
    Performance profiling options, when compiled with --enable-perfcounters.  \n\
       -p --perfconf=<P>  Intel PCM config file with upto 4 counters [none]   \n\
       -o --perfout=<O>   Output file to print performance counters [stdout]  \n\
                                                                              \n\
    Basic user options                                                        \n\
        -h --help         Show this message                                   \n\
        --verbose         Be more verbose -- show misc extra info             \n\
        --version         Show version                                        \n\
    \n");
}

void 
print_version()
{
    printf("\n%s\n", PACKAGE_STRING);
    printf("Copyright (c) 2012, ETH Zurich, Systems Group.\n");
    printf("http://www.systems.ethz.ch/projects/paralleljoins\n\n");
}

static char * 
mystrdup (const char *s) 
{
    char *ss = (char*) malloc (strlen (s) + 1);

    if (ss != NULL)
        memcpy (ss, s, strlen(s) + 1);

    return ss;
}

void 
parse_args(int argc, char ** argv, param_t * cmd_params) 
{

    int c, i, found;
    /* Flag set by ‘--verbose’. */
    static int verbose_flag;
    static int nonunique_flag;
    static int fullrange_flag;
    static int basic_numa;

    while(1) {
        static struct option long_options[] =
            {
                /* These options set a flag. */
                {"verbose",    no_argument,    &verbose_flag,   1},
                {"brief",      no_argument,    &verbose_flag,   0},
                {"non-unique", no_argument,    &nonunique_flag, 1},
                {"full-range", no_argument,    &fullrange_flag, 1},
                {"basic-numa", no_argument,    &basic_numa, 1},
                {"help",       no_argument,    0, 'h'},
                {"version",    no_argument,    0, 'v'},
                /* These options don't set a flag.
                   We distinguish them by their indices. */
                {"algo",    required_argument, 0, 'a'},
                {"nthreads",required_argument, 0, 'n'},
                {"perfconf",required_argument, 0, 'p'},
                {"r-size",  required_argument, 0, 'r'},
                {"s-size",  required_argument, 0, 's'},
                {"perfout", required_argument, 0, 'o'},
                {"r-seed",  required_argument, 0, 'x'},
                {"s-seed",  required_argument, 0, 'y'},
                {"skew",    required_argument, 0, 'z'},
                {0, 0, 0, 0}
            };
        /* getopt_long stores the option index here. */
        int option_index = 0;
     
        c = getopt_long (argc, argv, "a:n:p:r:s:o:x:y:z:hv",
                         long_options, &option_index);
     
        /* Detect the end of the options. */
        if (c == -1)
            break;
        switch (c)
        {
          case 0:
              /* If this option set a flag, do nothing else now. */
              if (long_options[option_index].flag != 0)
                  break;
              printf ("option %s", long_options[option_index].name);
              if (optarg)
                  printf (" with arg %s", optarg);
              printf ("\n");
              break;
     
          case 'a':
              i = 0; found = 0;
              while(algos[i].joinAlgo) {
                  if(strcmp(optarg, algos[i].name) == 0) {
                      cmd_params->algo = &algos[i];
                      found = 1;
                      break;
                  }
                  i++;
              }
              
              if(found == 0) {
                  printf("[ERROR] Join algorithm named `%s' does not exist!\n",
                         optarg);
                  print_help(argv[0]);
                  exit(EXIT_SUCCESS);
              }
              break;

          case 'h':
          case '?':
              /* getopt_long already printed an error message. */
              print_help(argv[0]);
              exit(EXIT_SUCCESS);
              break;
     
          case 'v':
              print_version();
              exit(EXIT_SUCCESS);
              break;

          case 'n':
              cmd_params->nthreads = atoi(optarg);
              break;

          case 'p':
              cmd_params->perfconf = mystrdup(optarg);
              break;
     
          case 'r':
              cmd_params->r_size = atoi(optarg);
              break;
     
          case 's':
              cmd_params->s_size = atoi(optarg);
              break;

          case 'o':
              cmd_params->perfout = mystrdup(optarg);
              break;

          case 'x':
              cmd_params->r_seed = atoi(optarg);
              break;

          case 'y':
              cmd_params->s_seed = atoi(optarg);
              break;

          case 'z':
              cmd_params->skew = atof(optarg);
              break;

          default:
              break;
        }
    }
     
    /* if (verbose_flag) */
    /*     printf ("verbose flag is set \n"); */

    cmd_params->nonunique_keys = nonunique_flag;
    cmd_params->verbose        = verbose_flag;     
    cmd_params->fullrange_keys = fullrange_flag;
    cmd_params->basic_numa     = basic_numa;

    /* Print any remaining command line arguments (not options). */
    if (optind < argc) {
        printf ("non-option arguments: ");
        while (optind < argc)
            printf ("%s ", argv[optind++]);
        printf ("\n");
    }
}
