#! /bin/bash

#
# Installation script for CK packages.
#

# PACKAGE_DIR
# INSTALL_DIR

cd $INSTALL_DIR

if [ "$CK_FORCE_USE_ABI" == "" ] ; then
 MACHINE=$(uname -m)
 if [ "${MACHINE}" == "aarch64" ]; then
  CK_FORCE_USE_ABI=0
 else
  CK_FORCE_USE_ABI=1
 fi
fi

mkdir lib
rm -f lib/SwPrefetchPass.so

mkdir src
cp -f ${PACKAGE_DIR}/Makefile src
cp -f ${PACKAGE_DIR}/*.cc src

cd src
rm -rf *.o *.so

# Check if NO_STRIDES
CK_EXTRA_FLAGS=""
if [ "${CK_NO_STRIDES}" == "1" ] ; then
  CK_EXTRA_FLAGS=-DNO_STRIDES
fi

make CXX=$CK_CXX \
     LLVM_DIR=${CK_ENV_COMPILER_LLVM} \
     LLVM_BUILD_DIR=${CK_ENV_COMPILER_LLVM} \
     CLANG_DIR=${CK_ENV_COMPILER_LLVM} \
     CLANG=${CK_ENV_COMPILER_LLVM_BIN}/$CK_CC \
     EXTRA_FLAGS=${CK_EXTRA_FLAGS} \
     PLUGIN_OUT=${CK_PLUGIN_OUT} \
     FORCE_USE_ABI=${CK_FORCE_USE_ABI}
if [ "${?}" != "0" ] ; then
 echo "Error: Compilation failed in $PWD!" 
 exit 1
fi

cp -f ${CK_PLUGIN_OUT}.so ${INSTALL_DIR}/lib
