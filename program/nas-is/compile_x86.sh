clang -O3 IS/is.c -c
clang -O3 is.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86/is-no
clang -O3 IS/is.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so
clang -O3 is.ll -c
clang -O3 is.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86/is-auto
clang -O3 IS/is.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-no-strides-pass/lib/SwPrefetchPass_noStrides.so
clang -O3 is.ll -c
clang -O3 is.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86/is-auto-nostride
clang -O3 IS/isswpf.c -c -DFETCHDIST=64 -DSTRIDE
clang -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86/is-man

for i in 2 4 8 16 32 64 128 256 2048
do
  clang -O3 IS/isswpf.c -c -DFETCHDIST=$i -DSTRIDE
  clang -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86-offsets/is-offset-$i
done
  clang -O3 IS/isswpf.c   -c -DFETCHDIST=64
  clang -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/x86-offsets/is-offset-64-nostride

