clang -O3 randacc.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 randacc.ll -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 randacc.o -o bin/arm/randacc-auto
clang -O3 randacc.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 randacc.o -o bin/arm/randacc-no
clang -O3 randaccswpf.c -DFETCHDIST=32 -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 randaccswpf.o -o bin/arm/randacc-man
for i in 2 4 8 16 32 64 128 256
do
  clang -O3 randaccswpf.c  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=$i
  aarch64-linux-gnu-gcc -O3 randaccswpf.o -o bin/arm-offsets/randacc-offset-$i
done
  clang -O3 randaccswpf.c  --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu -c -DFETCHDIST=32 -DSTRIDE
  aarch64-linux-gnu-gcc -O3 randaccswpf.o -o bin/arm-offsets/randacc-offset-32-stride

