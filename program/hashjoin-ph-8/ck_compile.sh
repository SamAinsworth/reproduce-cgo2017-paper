#! /bin/bash

rm -f a.out *.o *.ll

if [ "${CK_PROG_COMPILER_FLAGS}" == "" ] ; then
  export CK_PROG_COMPILER_FLAGS="-O3"
elif [ "${CK_PROG_COMPILER_FLAGS}" == " " ] ; then
  export CK_PROG_COMPILER_FLAGS="-O3"
fi

CK_COMPILER="$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY $CK_PROG_COMPILER_FLAGS"

echo ""

# Check compilation type
if [ "${CK_COMPILE_TYPE}" == "auto" ] ; then
  echo "*** auto ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epb.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER npj8epb.ll -c"
  EXECUTE3="$CK_COMPILER npj8epb.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"

elif [ "${CK_COMPILE_TYPE}" == "auto-nostride" ] ; then
  echo "*** auto-nostride ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epb.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_NO_STRIDES_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER npj8epb.ll -c"
  EXECUTE3="$CK_COMPILER npj8epb.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"

elif [ "${CK_COMPILE_TYPE}" == "man" ] ; then
  echo "*** man (3) ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epbsw.c -DNUMPREFETCHES=3 -DSTRIDE -c"
  EXECUTE2=""
  EXECUTE3="$CK_COMPILER npj8epbsw.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"

elif [ "${CK_COMPILE_TYPE}" == "prefetches" ] ; then
  echo "*** prefetches (${CK_NUMPREFETCHES}) ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epbsw.c -DNUMPREFETCHES=${CK_NUMPREFETCHES} -DSTRIDE -c"
  EXECUTE2=""
  EXECUTE3="$CK_COMPILER npj8epbsw.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"

elif [ "${CK_COMPILE_TYPE}" == "prefetches-3-nostride" ] ; then
  echo "*** prefetches-3-nostride  ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epb.c -DNUMPREFETCHES=3 -c"
  EXECUTE2=""
  EXECUTE3="$CK_COMPILER npj8epb.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"

else
  echo "*** no  ***"
  EXECUTE1="$CK_COMPILER ../src/npj8epb.c -c"
  EXECUTE2=""
  EXECUTE3="$CK_COMPILER npj8epb.o ../src/main.c ../src/generator.c ../src/genzipf.c ../src/perf_counters.c ../src/cpu_mapping.c ../src/parallel_radix_join.c -lpthread -lm -std=c99"
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
