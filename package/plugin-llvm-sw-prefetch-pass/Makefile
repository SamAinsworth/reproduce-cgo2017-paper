# The name of the plugin.
PLUGIN = SwPrefetchPass
PLUGIN_OUT = SwPrefetchPass

# LLVM paths. Note: you probably need to update these.
LLVM_DIR = /local/scratch/sa614/clang
LLVM_BUILD_DIR = $(LLVM_DIR)/build
CLANG_DIR = $(LLVM_DIR)/tools/clang
CLANG = $(LLVM_BUILD_DIR)/bin/clang

# Compiler flags.
CXXFLAGS  = -I$(LLVM_DIR)/include -I$(CLANG_DIR)/include -I$(LLVM_DIR)/llvm/include 
CXXFLAGS += -I$(LLVM_BUILD_DIR)/include -I$(LLVM_BUILD_DIR)/tools/clang/include
CXXFLAGS += ${EXTRA_FLAGS}
CXXFLAGS += -D__STDC_LIMIT_MACROS -D__STDC_CONSTANT_MACROS -Wno-long-long
CXXFLAGS += -fPIC -fvisibility-inlines-hidden
CXXFLAGS += -fno-exceptions -fno-rtti -std=c++11
CXXFLAGS += -Wall

# Linker flags.
LDFLAGS = -shared -Wl,-undefined,dynamic_lookup

$(PLUGIN).so : $(PLUGIN).o
	$(CXX) $(LDFLAGS) -o $(PLUGIN_OUT).so $(PLUGIN).o

$(PLUGIN).o : $(PLUGIN).cc
	$(CXX) $(CXXFLAGS) -c $(PLUGIN).cc -o $(PLUGIN).o

clean :
	rm -fv $(PLUGIN).o $(PLUGIN_OUT).so
	
	
#example script taken from http://www.hanshq.net/clang-plugin-example.html
