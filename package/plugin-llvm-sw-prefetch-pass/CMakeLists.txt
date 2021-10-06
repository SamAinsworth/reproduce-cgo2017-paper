cmake_minimum_required(VERSION 3.16)
project(SwPrefetchPass)

if (DEFINED LLVM_BUILD_DIR)
find_package(LLVM REQUIRED PATHS "${LLVM_BUILD_DIR}")
else ()
find_package(LLVM REQUIRED CONFIG)
endif ()

add_definitions(${LLVM_DEFINITIONS})
include_directories(${LLVM_INCLUDE_DIRS})
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)

add_llvm_library(SwPrefetchPass MODULE SwPrefetchPass.cc PLUGIN_TOOL clang)
