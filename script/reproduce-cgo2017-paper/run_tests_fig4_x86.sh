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
echo "manual prefetching"
./cg-man;./cg-man;./cg-man
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
echo "manual prefetching"
./is-man;./is-man;./is-man
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
echo "manual prefetching"
time ./randacc-man 100000000;time ./randacc-man 100000000;time ./randacc-man 100000000;
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
echo "manual prefetching"
./hj2-man -a NPO_st -r 12800000 -s 12800000;./hj2-man -a NPO_st -r 12800000 -s 12800000;./hj2-man -a NPO_st -r 12800000 -s 12800000;
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
echo ""
echo "***************"
echo "manual prefetching"
./hj8-man -a NPO_st -r 12800000 -s 12800000;./hj8-man -a NPO_st -r 12800000 -s 12800000;./hj8-man -a NPO_st -r 12800000 -s 12800000;
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
echo "manual prefetching (best for out of order)"
./g500-man-outoforder -s 16 -e 10;./g500-man-outoforder -s 16 -e 10;./g500-man-outoforder -s 16 -e 10;
echo ""
echo "***************"
echo "manual prefetching (best for in order)"
./g500-man-inorder -s 16 -e 10;./g500-man-inorder -s 16 -e 10;./g500-man-inorder -s 16 -e 10;
echo ""
echo "---------------------------------"
echo ""
echo "g500-s21"
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
echo "manual prefetching (best for out of order)"
./g500-man-outoforder -s 21 -e 10;./g500-man-outoforder -s 21 -e 10;./g500-man-outoforder -s 21 -e 10;
echo ""
echo "***************"
echo "manual prefetching (best for in order)"
./g500-man-inorder -s 21 -e 10;./g500-man-inorder -s 21 -e 10;./g500-man-inorder -s 21 -e 10;./g500-man-inorder -s 21 -e 10;
} &>results_x86_fig4.out
