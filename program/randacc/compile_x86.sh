clang -O3 randacc.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm
clang -O3 randacc.ll -o bin/x86/randacc-auto

clang -O3 randacc.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-no-strides-pass/lib/SwPrefetchPass_noStrides.so -c -S -emit-llvm
clang -O3 randacc.ll -o bin/x86/randacc-auto-nostride

clang -O3 randacc.c -o bin/x86/randacc-no




clang -O3 randaccswpf.c -DFETCHDIST=32 -o bin/x86/randacc-man

for i in 2 4 8 16 32 64 128 256
do
  clang -O3 randaccswpf.c -DFETCHDIST=$i -o bin/x86-offsets/randacc-offset-$i
done
  clang -O3 randaccswpf.c -DFETCHDIST=32 -DSTRIDE -o bin/x86-offsets/randacc-offset-32-stride
