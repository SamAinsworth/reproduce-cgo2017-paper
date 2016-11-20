Artifact Evaluation Reproduction for "Software Prefetching for Indirect Memory Accesses", CGO 2017, using CK. 
==================================================

This repository contains artifacts and workflows
to reproduce experiments from the CGO 2017 paper 
by S.Ainsworth and T.M.Jones

"Software Prefetching for Indirect Memory Accesses"

Hardware pre-requisities
========================
Any of the follows three architectures:
* Intel-based 
* ARMv7
* ARM64

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

You can install LLVM 3.9 via CK as follows:
$ ck install package:compiler-llvm-3.9.0-linux-download

You can install 2 LLVM plugins described in the above paper as follows:
$ ck install package:plugin-llvm-sw-prefetch-no-strides-pass
$ ck install package:plugin-llvm-sw-prefetch-pass

Testing installation
====================

You can compile and run one of the benchmarks (NAS CG) with the LLVM plugin as follows:

$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=auto

$ ck run program:nas-cg

Running experimental workflows (reproducing figures)
====================================================



TBD add compilation to the experimental workflow:


```
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=auto
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=man-inorder
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=man-outoforder
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=man-inorder-nostride
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=man-outoforder-nostride
$ ck compile program:graph500 --speed --env.CK_COMPILATION_TYPE=no
```

```
$ ck compile program:hashjoin-ph-2 --env.CK_COMPILATION_TYPE=auto
$ ck compile program:hashjoin-ph-2 --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:hashjoin-ph-2 --env.CK_COMPILATION_TYPE=man
$ ck compile program:hashjoin-ph-2 --env.CK_COMPILATION_TYPE=offset --env.CK_FETCHDIST={2,4,8,16,32,64,128,256}
```

```
$ ck compile program:hashjoin-ph-2 --env.CK_COMPILATION_TYPE=no
$ ck compile program:hashjoin-ph-8 --env.CK_COMPILATION_TYPE=auto
$ ck compile program:hashjoin-ph-8 --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:hashjoin-ph-8 --env.CK_COMPILATION_TYPE=man
$ ck compile program:hashjoin-ph-8 --env.CK_COMPILATION_TYPE=prefetches --env.CK_NUMPREFETCHES={1,2,3,4}
$ ck compile program:hashjoin-ph-8 --env.CK_COMPILATION_TYPE=no
```

```
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=auto
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=man
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=offset --env.CK_FETCHDIST={2,4,8,16,32,64,128,256,2048}
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=offset-64-nostride
$ ck compile program:nas-cg --speed --env.CK_COMPILATION_TYPE=no
```

```
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=auto
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=man
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=offset --env.CK_FETCHDIST={2,4,8,16,32,64,128,256,2048}
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=offset-64-nostride
$ ck compile program:nas-is --speed --env.CK_COMPILATION_TYPE=no
```

```
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=auto
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=auto-nostride
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=man
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=offset --env.CK_FETCHDIST={2,4,8,16,32,64,128,256}
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=offset-32-nostride
$ ck compile program:randacc --speed --env.CK_COMPILATION_TYPE=no
```

Compare with pre-recorded results (expected)

If unexpected behavior, report to the author


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
