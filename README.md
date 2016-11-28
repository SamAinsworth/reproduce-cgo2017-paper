Artifact Evaluation Reproduction for "Software Prefetching for Indirect Memory Accesses", CGO 2017, using CK. 
==================================================

This repository contains artifacts and workflows
to reproduce experiments from the CGO 2017 paper 
by S.Ainsworth and T.M.Jones

"Software Prefetching for Indirect Memory Accesses"

Hardware pre-requisities
========================
Any of the following architectures:
* Intel-based 
* ARM64 with 64-bit kernel

Software pre-requisites
=======================

* Python 2.7 or 3.3+
* git client
* Collective Knowledge Framework (CK) - http://cKnowledge.org
* All other dependencies will be installed by CK (LLVM 3.9 and plugins)

You can install above dependencies on Ubuntu via:
```
$ sudo apt-get install python python-pip git
$ sudo pip install ck
```

Installation
============

You can install this repository via CK as follows:

```
$ ck pull repo --url=https://github.com/SamAinsworth/reproduce-cgo2017-paper
```

If you already have CK installed, please update before use:

```
$ ck pull all
```


Testing installation
====================

You can compile and run one of the benchmarks (NAS CG) with the LLVM plugin as follows:

```
$ ck compile program:nas-cg --speed --env.CK_COMPILE_TYPE=auto
```

```
$ ck run program:nas-cg
```

Running experimental workflows (reproducing figures)
====================================================

Run

```
$ ck run workflow-from-cgo2017-paper
```

The script runs experiments from the paper, in order of figures (2,4-7). At the end of each experiment, times are output, along with the example values we achieved on Haswell (in the case of x86) or the A57-powered Nvidia TX1 (in the case of ARM64). Though we don't expect the overall times to be similar across different systems, the trends shown in the paper should be largely similar for a given class of microarchitecture.

By default, the script above waits for user input at the end of each experiment. To turn this off, run with the --quiet option:

```
$ ck run workflow-from-cgo2017-paper --quiet
```

If any unexpected behaviour is observed, please report it to the authors.

Validation of results
====================================================

To generate bar graphs of the data, run 

```
ck dashboard workflow-from-cgo2017-paper
```

This will output speedups for the data you have generated, and also graphs for prerecorded data for x86 (Haswell) and aarch64 (A57), but not aarch64 (A53).

Results will also be output to ck-log-reproduce-results-from-cgo2017-paper.txt, in the directory in which you run the workflow.

This file will include the results observed on your machine, and those observed on either Haswell or A57 for reference, depending on your target ISA.

While we do not expect absolute values to match, it is expected that overall trends, as shown in the related figures (2,4-7) within the paper, will match up depending on your microarchitecture.

Please note that the reference results on ARM64 systems when running on in-order architectures such at the A53 will still be from the A57, so are not expected to match up directly: you should instead compare ratios given in the paper itself.

If anything in unclear, or any unexpected results occur, please report it to the authors.

Manual validation (if problems with CK)
=======================================

for x86-64:

```
$cd script/reproduce-cgo2017-paper
```

To compile:

```
$./compile_x86.sh
```

To run:

```
$./run_x86.sh
```

for ARM64:

cross compilation for ARM64 on an x86-64 machine:

```
$cd script/reproduce-cgo2017-paper
$./compile_aarch64.sh
```

running on an ARM64 machine:

```
$cd script/reproduce-cgo2017-paper
$./run_arm.sh
```

Recompilation should not be necessary, as all binaries are included, but is provided as an option.

Authors
=======
S.Ainsworth and T.M.Jones

Acknowledgments
===============
This work was supported by the Engineering and Physical Sciences Research Council (EPSRC), through grant references EP/K026399/1 and EP/M506485/1, and ARM Ltd.


Customisation 
===============

Our CK integration allows customisation of both benchmarks and settings. New workflows can be added in the style exhibited by module/workflow-from-cgo-paper/module.py:

```
    r=experiment({'host_os':hos, 'target_os':tos, 'device_id':tdid, 'out':oo,
                  'program_uoa':cfg['programs_uoa']['nas-is'],
                  'env':{'CK_COMPILE_TYPE':'no'},
                  'deps':deps,
                  'quiet':q, 'record':rec, 'record_repo_uoa':rruid, 'record_data_uoa':rduid, 'os_abi':os_abi,
                  'title':'Reproducing experiments for Figure 2',
                  'subtitle':'Validating nas-is no prefetching:',
                  'key':'figure-2-nas-is-no-prefetching', 'results':results})
```

CK_COMPILE_TYPE can be configured as "no", "auto", "auto-nostride" or "man" to run the relevant experiment. The behaviour of each of these is specified in the ck_compile.sh included in each benchmark. Other customisable properties are available depending on the benchmark: see module.py for more details. The program can be specified in cfg, output text in title and subtitle, and new results output and optionally stored (--record) using JSON with a new "key".


Similarly, benchmarks can be compiled and run individually, for example:

```
$ ck compile program:nas-is --speed --env.CK_COMPILE_TYPE=auto
$ ck run program:nas-is
```

The software prefetching shared object pass can also be compiled and installed using CK, then used separately:

```
	$ ck install package:plugin-llvm-sw-prefetch-pass
	$ clang -Xclang -load -Xclang $(ck find package:plugin-llvm-sw-prefetch-pass)/lib/SwPrefetchPass.so -O3 ...
```



Troubleshooting
===============

Issues with GLIBCXX_3.4.20/3.4.21 when using LLVM installed via CK: These sometimes occur on earlier Ubuntu versions (14.04) on ARM/x86. This can be fixed by upgrading to later versions of Ubuntu, or can sometimes be fixed by:

```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

Issues with libncursesw.so.6 (not found) on some older machines: It can be fixed by compiling and installing lib-ncurses with the support for wide characters. This can be done automatically via CK:


```
$ ck install package:lib-ncurses-6.0-root
```

 undefined symbol:  _ZNK4llvm12FunctionPass17createPrinterPassERNS_11raw_ostreamERKSs when compiling using Clang:
 
 This occurs on some machines depending on other libraries installed. To fix this, run 

```
$ ck install package:plugin-llvm-sw-prefetch-pass -DCK_FORCE_USE_ABI=0
$ ck install package:plugin-llvm-sw-prefetch-no-strides-pass -DCK_FORCE_USE_ABI=0
```

or

```
$ ck install package:plugin-llvm-sw-prefetch-no-strides-pass -DCK_FORCE_USE_ABI=1
$ ck install package:plugin-llvm-sw-prefetch-pass -DCK_FORCE_USE_ABI=1
```

and retry compilation.

If this var is not specified, CK build script will try to detect host machine and will set it to 1 on aarch64 and to 0 on anything else: if this fails, try the opposite.
