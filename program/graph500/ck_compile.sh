#! /bin/bash

rm -f a.out *.o *.ll

CK_COMPILER="$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY $CK_PROG_COMPILER_FLAGS"

echo ""

# Check compilation type
if [ "${CK_COMPILE_TYPE}" == "auto" ] ; then
  echo "*** auto ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csr.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER seq-csr.ll -c"
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csr.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

elif [ "${CK_COMPILE_TYPE}" == "auto-nostride" ] ; then
  echo "*** auto-nostride ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csr.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_NO_STRIDES_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER seq-csr.ll -c"
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csr.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

elif [ "${CK_COMPILE_TYPE}" == "man-inorder" ] ; then
  echo "*** man-inorder ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csrswpfio.c -DSTRIDE -c"
  EXECUTE2=""
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csrswpfio.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

elif [ "${CK_COMPILE_TYPE}" == "man-outoforder" ] ; then
  echo "*** man-outoforder ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csrswpfooo.c -DSTRIDE -c"
  EXECUTE2=""
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csrswpfooo.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

elif [ "${CK_COMPILE_TYPE}" == "man-inorder-nostride" ] ; then
  echo "*** man-inorder-nostride ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csrswpfio.c -c"
  EXECUTE2=""
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csrswpfio.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

elif [ "${CK_COMPILE_TYPE}" == "man-outoforder-nostride" ] ; then
  echo "*** man-outoforder-nostride ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csrswpfooo.c -c"
  EXECUTE2=""
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csrswpfooo.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"

else
  echo "*** no ***"
  EXECUTE1="$CK_COMPILER ../seq-csr/seq-csr.c -c"
  EXECUTE2=""
  EXECUTE3="gcc -flto -g -std=c99 -Wall -O3 -I../generator seq-csr.o ../graph500.c ../options.c ../rmat.c ../kronecker.c ../verify.c ../prng.c ../xalloc.c ../timer.c ../generator/splittable_mrg.c ../generator/graph_generator.c ../generator/make_graph.c ../generator/utils.c  -lm -lrt"
fi

echo "$EXECUTE1"
$EXECUTE1
if [ "${?}" != "0" ] ; then
 exit ${?}
fi

echo "$EXECUTE2"
$EXECUTE2
if [ "${?}" != "0" ] ; then
 exit ${?}
fi

echo "$EXECUTE3"
$EXECUTE3
if [ "${?}" != "0" ] ; then
 exit ${?}
fi
