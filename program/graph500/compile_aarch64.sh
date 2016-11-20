clang -O3 seq-csr/seq-csr.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
clang -O3 seq-csr.ll -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csr.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-auto
clang -O3 seq-csr/seq-csr.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csr.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-no
clang -O3 seq-csr/seq-csrswpfio.c  -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfio.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-man-inorder
clang -O3 seq-csr/seq-csrswpfooo.c  -DSTRIDE -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfooo.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-man-outoforder
clang -O3 seq-csr/seq-csrswpfio.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfio.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-man-inorder-nostride
clang -O3 seq-csr/seq-csrswpfooo.c -c --target=aarch64-none-linux-gnu --sysroot=/usr/aarch64-linux-gnu
aarch64-linux-gnu-gcc -O3 -flto -fwhole-program -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfooo.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/arm/g500-man-outoforder-nostride


