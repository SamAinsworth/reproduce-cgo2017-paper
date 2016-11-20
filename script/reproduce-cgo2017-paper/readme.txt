To run all experiments on an x86-64 machine:
do ./run_x86.sh

To run all experiments on an Aarch64 machine:
do ./run_arm.sh

To compile all benchmarks (on an x86-64 machine, cross compiling for ARM), use compile_x86.sh or compile_aarch64.sh as appropriate. Binaries are already included for each benchmark.

The output of each test will be a text file corresponding to the figures in the paper. Each benchmark under each setting will be run three times, and the output of the program including time information will be given within each file. This time information should give comparable speedup to that exhibited within the paper.

If you would like to do so, you can recompile our prefetching pass by navigating to ''source'' and using make. The Makefile within this folder will have to be reconfigured with LLVM_DIR set to the directory of your LLVM Clang source and build.
