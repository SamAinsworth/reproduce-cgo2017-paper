clang -O3 CG/cg.c -c
clang -O3 cg.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86/cg-no
clang -O3 CG/cg.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so
clang -O3 cg.ll -c
clang -O3 cg.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86/cg-auto
clang -O3 CG/cg.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-no-strides-pass/lib/SwPrefetchPass_noStrides.so
clang -O3 cg.ll -c
clang -O3 cg.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86/cg-auto-nostride
clang -O3 CG/cgswpf.c -c -DFETCHDIST=64 -DSTRIDE
clang -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86/cg-man
for i in 2 4 8 16 32 64 128 256 2048
do
  clang -O3 CG/cgswpf.c -c -DFETCHDIST=$i -DSTRIDE
  clang -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86-offsets/cg-offset-$i
done
  clang -O3 CG/cgswpf.c  -c -DFETCHDIST=64
  clang -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/x86-offsets/cg-offset-64-nostride

