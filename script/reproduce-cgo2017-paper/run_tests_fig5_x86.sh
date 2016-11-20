{
cd ../../program
echo ""
echo "---------------------------------"
echo ""
echo "cg"
cd nas-cg/bin/x86
echo ""
echo "***************"
echo "no prefetching"
./cg-no;./cg-no;./cg-no
echo ""
echo "***************"
echo "auto prefetching"
./cg-auto;./cg-auto;./cg-auto
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
./cg-auto-nostride;./cg-auto-nostride;./cg-auto-nostride
echo ""
echo "---------------------------------"
echo ""
echo "is"
cd ../../../nas-is/bin/x86
echo ""
echo "***************"
echo "no prefetching"
./is-no;./is-no;./is-no
echo ""
echo "***************"
echo "auto prefetching"
./is-auto;./is-auto;./is-auto
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
./is-auto-nostride;./is-auto-nostride;./is-auto-nostride
echo ""
echo "---------------------------------"
echo ""
echo "randacc"
cd ../../../randacc/bin/x86
echo ""
echo "***************"
echo "no prefetching"
time ./randacc-no 100000000;time ./randacc-no 100000000;time ./randacc-no 100000000;
echo ""
echo "***************"
echo "auto prefetching"
time ./randacc-auto 100000000;time ./randacc-auto 100000000;time ./randacc-auto 100000000;
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
time ./randacc-auto-nostride 100000000;time ./randacc-auto-nostride 100000000;time ./randacc-auto-nostride 100000000;
echo ""
echo "---------------------------------"
echo ""
echo "hj2"
cd ../../../hashjoin-ph-2/src/bin/x86
echo ""
echo "***************"
echo "no prefetching"
./hj2-no -a NPO_st -r 12800000 -s 12800000;./hj2-no -a NPO_st -r 12800000 -s 12800000;./hj2-no -a NPO_st -r 12800000 -s 12800000;
echo ""
echo "***************"
echo "auto prefetching"
./hj2-auto -a NPO_st -r 12800000 -s 12800000;./hj2-auto -a NPO_st -r 12800000 -s 12800000;./hj2-auto -a NPO_st -r 12800000 -s 12800000;
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
./hj2-auto-nostride -a NPO_st -r 12800000 -s 12800000;./hj2-auto-nostride -a NPO_st -r 12800000 -s 12800000;./hj2-auto-nostride -a NPO_st -r 12800000 -s 12800000
echo ""
echo "---------------------------------"
echo ""
echo "hj8"
cd ../../../hashjoin-ph-8/src/bin/x86
echo ""
echo "***************"
echo "no prefetching"
./hj8-no -a NPO_st -r 12800000 -s 12800000;./hj8-no -a NPO_st -r 12800000 -s 12800000;./hj8-no -a NPO_st -r 12800000 -s 12800000;
echo ""
echo "***************"
echo "auto prefetching"
./hj8-auto -a NPO_st -r 12800000 -s 12800000;./hj8-auto -a NPO_st -r 12800000 -s 12800000;./hj8-auto -a NPO_st -r 12800000 -s 12800000;
echo "auto prefetching (indirect only)"
./hj8-auto-nostride -a NPO_st -r 12800000 -s 12800000;./hj8-auto-nostride -a NPO_st -r 12800000 -s 12800000;./hj8-auto-nostride -a NPO_st -r 12800000 -s 12800000
cd ../../../../graph500/bin/x86
echo ""
echo "---------------------------------"
echo ""
echo "g500-s16"
echo ""
echo "***************"
echo "no prefetching"
./g500-no -s 16 -e 10;./g500-no -s 16 -e 10;./g500-no -s 16 -e 10;
echo ""
echo "***************"
echo "auto prefetching"
./g500-auto -s 16 -e 10;./g500-auto -s 16 -e 10;./g500-auto -s 16 -e 10;
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
./g500-auto-nostride -s 16 -e 10;./g500-auto-nostride -s 16 -e 10;./g500-auto-nostride -s 16 -e 10
echo ""
echo "---------------------------------"
echo ""
echo "***************"
echo "no prefetching"
./g500-no -s 21 -e 10;./g500-no -s 21 -e 10;./g500-no -s 21 -e 10;
echo ""
echo "***************"
echo "auto prefetching"
./g500-auto -s 21 -e 10;./g500-auto -s 21 -e 10;./g500-auto -s 21 -e 10;
echo ""
echo "***************"
echo "auto prefetching (indirect only)"
./g500-auto-nostride -s 21 -e 10;./g500-auto-nostride -s 21 -e 10;./g500-auto-nostride -s 21 -e 10
} &>results_x86_fig5.out
