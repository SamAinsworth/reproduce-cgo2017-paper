clang -O3 seq-csr/seq-csr.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-pass/lib/SwPrefetchPass.so -c -S -emit-llvm 
clang -O3 seq-csr.ll -c 
gcc -flto -g -std=c99 -Wall -O3 -I./generator   seq-csr.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-auto

clang -O3 seq-csr/seq-csr.c -Xclang -load -Xclang ../../package/plugin-llvm-sw-prefetch-no-strides-pass/lib/SwPrefetchPass_noStrides.so -c -S -emit-llvm 
clang -O3 seq-csr.ll -c 
gcc -flto -g -std=c99 -Wall -O3 -I./generator   seq-csr.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-auto-nostride
clang -O3 seq-csr/seq-csr.c -c 
gcc -flto -g -std=c99 -Wall -O3 -I./generator   seq-csr.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-no
clang -O3 seq-csr/seq-csrswpfio.c -DSTRIDE -c 
gcc -O3 -flto -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfio.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-man-inorder
clang -O3 seq-csr/seq-csrswpfooo.c -DSTRIDE -c 
gcc -O3 -flto -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfooo.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-man-outoforder
clang -O3 seq-csr/seq-csrswpfio.c -c 
gcc -O3 -flto -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfio.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-man-inorder-nostride
clang -O3 seq-csr/seq-csrswpfooo.c -c 
gcc -O3 -flto -g -std=c99 -Wall -O3 -I./generator   seq-csrswpfooo.o graph500.c options.c rmat.c kronecker.c verify.c prng.c xalloc.c timer.c generator/splittable_mrg.c generator/graph_generator.c generator/make_graph.c generator/utils.c  -lm -lrt -o bin/x86/g500-man-outoforder-nostride



