cd src
clang -O3 npj2epb.c -Xclang -load -Xclang ../../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 npj2epb.ll -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj2epb.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj2-auto
clang -O3 npj2epb.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj2epb.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj2-no
clang -O3 npj2epbsw.c -DFETCHDIST=64 -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj2epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj2-man
for i in 2 4 8 16 32 64 128 256
do
clang -O3 npj2epbsw.c -DFETCHDIST=$i -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj2epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm-offsets/hj2-offset-$i
done
clang -O3 npj8epb.c -Xclang -load -Xclang ../../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 npj8epb.ll -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj8epb.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj8-auto
clang -O3 npj8epb.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj8epb.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj8-no
clang -O3 npj8epbsw.c -DNUMPREFETCHES=3 -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj8epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm/hj8-man
for i in 1 2 3 4
do
clang -O3 npj8epbsw.c -DNUMPREFETCHES=$i -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj8epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm-offsets/hj8-prefetches-$i
done
clang -O3 npj8epbsw.c -DNUMPREFETCHES=3 -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj8epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm-offsets/hj8-prefetches-4-nostride
clang -O3 npj2epbsw.c -DFETCHDIST=64 -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 npj2epbsw.o main.c generator.c genzipf.c perf_counters.c cpu_mapping.c parallel_radix_join.c -lpthread -lm -std=c99  -o bin/arm-offsets/hj2-offset-64-nostride
