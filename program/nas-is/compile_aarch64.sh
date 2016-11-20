clang -O3 -c IS/is.c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c
aarch64-linux-gnu-gcc -O3 is.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/arm/is-no
clang -O3 IS/is.c -S -emit-llvm  -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 is.ll  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c
aarch64-linux-gnu-gcc -O3 is.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/arm/is-auto
clang -O3 IS/isswpf.c   --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=64 -DSTRIDE
aarch64-linux-gnu-gcc -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/arm/is-man


for i in 2 4 8 16 32 64 128 256 2048
do
  clang -O3 IS/isswpf.c   --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=$i -DSTRIDE
  aarch64-linux-gnu-gcc -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/arm-offsets/is-offset-$i
done
   clang -O3 IS/isswpf.c   --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=64
  aarch64-linux-gnu-gcc -O3 isswpf.o ../nas-common/c_print_results.c ../nas-common/c_timers.c ../nas-common/wtime.c -o bin/arm-offsets/is-offset-64-nostride


