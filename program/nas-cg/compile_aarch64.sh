clang -O3 CG/cg.c   --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c
aarch64-linux-gnu-gcc -O3 cg.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/arm/cg-no
clang -O3 CG/cg.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 -c cg.ll  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c
aarch64-linux-gnu-gcc -O3 cg.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/arm/cg-auto
clang -O3 CG/cgswpf.c  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=64 -DSTRIDE
aarch64-linux-gnu-gcc -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/arm/cg-man

for i in 2 4 8 16 32 64 128 256 2048
do
  clang -O3 CG/cgswpf.c  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=$i -DSTRIDE
  aarch64-linux-gnu-gcc -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/arm-offsets/cg-offset-$idone
  clang -O3 CG/cgswpf.c  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=64
  aarch64-linux-gnu-gcc -O3 cgswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -lm ../nas-common/c_randdp.c -o bin/arm-offsets/cg-offset-64-nostride
