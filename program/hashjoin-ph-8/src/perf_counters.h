/**
 * @file    perf_counters.h
 * @author  Cagri Balkesen <bcagri@melodica>
 * @date    Mon Feb  6 21:46:14 2012
 * @version $Id: perf_counters.h 3017 2012-12-07 10:56:20Z bcagri $
 * 
 * @brief  An interface to the Intel Performance Counters Monitoring
 * 
 * 
 */

#ifndef PERF_COUNTERS_H
#define PERF_COUNTERS_H


/** @defgroup PerformanceMonitoring Performance Monitoring Tools.
 * A set of methods to use Intel Performance Counter Monitor library.
 * @warning This tool is only available when compiled with C++ (g++).
 *
 * @{
 */

/** Is performance monitoring PER_CORE? */
#ifndef PER_CORE
#define PER_CORE 0
#endif

/** Is performance monitoring PER_SOCKET? */
#ifndef PER_SOCKET
#define PER_SOCKET 1
#endif

/** Is performance monitoring PER_SYSTEM? */
#ifndef PER_SYSTEM
#define PER_SYSTEM 0
#endif

/** custom performance counters config file, if NULL no custom config. */
extern char * PCM_CONFIG;

/** the output file for performance counter results, if NULL output to stdout */
extern char * PCM_OUT;

/** 
 * Initializes the Intel Performance Counter Monitor instance. 
 * If no config is specified, then default counters are used, i.e. 
 * instr. retired, cycles, cache misses, etc.
 * 
 * @param pcmcfg configuration file which determines counters to be used.
 * @param pcmout output file to which PCM results should go, NULL->stdout
 */
void
PCM_initPerformanceMonitor(const char * pcmcfg, const char * pcmout);

/** 
 * Starts the performance counters.
 * 
 */
void
PCM_start();

/** 
 * Stops collecting performance counter events.
 * 
 */
void
PCM_stop();

/** 
 * Prints out performance counter results to the given output file.
 * 
 * @param perf_outfile output file for performance results.
 */
void
PCM_printResults();

/** 
 * Cleans up the PCM state before program shutdown.
 * 
 */
void
PCM_cleanup();

/**
 * Accumulates results between last start and stop calls to the
 * internal accumulator state.
 *
 */
void
PCM_accumulate();

/**
 * Prints out accumlated counters so far (upto the last PCM_accumulate() call)
 *
 */
void
PCM_printAccumulators();

/**
 * Logs a message to the performance counters output file (default is stdout)
 *
 */
void
PCM_log(char * msg);

/** @} */

#endif /* PERF_COUNTERS_H */
