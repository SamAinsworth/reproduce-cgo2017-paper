#! /bin/bash

rm -f a.out *.o *.ll

CK_COMPILER="$CK_CC $CK_COMPILER_FLAGS_OBLIGATORY $CK_PROG_COMPILER_FLAGS"

echo ""

# Check compilation type
if [ "${CK_COMPILE_TYPE}" == "auto" ] ; then
  echo "*** auto ***"
  EXECUTE1="$CK_COMPILER ../randacc.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER randacc.ll"

elif [ "${CK_COMPILE_TYPE}" == "auto-nostride" ] ; then
  echo "*** auto-nostride ***"
  EXECUTE1="$CK_COMPILER ../randacc.c -Xclang -load -Xclang ${CK_ENV_PLUGIN_LLVM_SW_PREFETCH_NO_STRIDES_PASS_FILE} -c -S -emit-llvm"
  EXECUTE2="$CK_COMPILER randacc.ll"

elif [ "${CK_COMPILE_TYPE}" == "man" ] ; then
  echo "*** man (32) ***"
  EXECUTE1="$CK_COMPILER ../randaccswpf.c -DFETCHDIST=32"
  EXECUTE2=""

elif [ "${CK_COMPILE_TYPE}" == "offset" ] ; then
  echo "*** offset (${CK_FETCHDIST}) ***"
  EXECUTE1="$CK_COMPILER ../randaccswpf.c -DFETCHDIST=${CK_FETCHDIST}"
  EXECUTE2=""

elif [ "${CK_COMPILE_TYPE}" == "offset-32-stride" ] ; then
  echo "*** randacc-offset-32-stride ***"
  EXECUTE1="$CK_COMPILER ../randaccswpf.c -DFETCHDIST=32 -DSTRIDE"
  EXECUTE2=""

else
  echo "*** no  ***"
  EXECUTE1="$CK_COMPILER ../randacc.c"
  EXECUTE2=""
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
