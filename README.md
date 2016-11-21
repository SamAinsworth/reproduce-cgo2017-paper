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
$ ck pull repo --url=https://github.com/SamAinsworth/reproduce-cgo2017-paper

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

Results will be output to ck-log-reproduce-results-from-cgo2017-paper.txt, in the current directory.

If any unexpected behavior is observed, please report it to the authors.


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

Troubleshooting
===============

* Issues with GLIBCXX_3.4.20/3.4.21 when using LLVM installed via CK: These sometimes occur on earlier Ubuntu versions (14.04) on ARM/x86. This can be fixed by upgrading to later versions of Ubuntu, or can sometimes be fixed by:

```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

* Issues with libncursesw.so.6 (not found) on some older machines.

It can be fixed by compiling and installing lib-ncurses with the support for wide characters. It can be done automatically via CK:

```
$ ck install package:lib-ncurses-6.0-root
```
