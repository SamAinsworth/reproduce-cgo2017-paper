{
cd ../../program
echo ""
echo "---------------------------------"
echo ""
echo "cg"
cd nas-cg/bin/arm
echo ""
echo "***************"
echo "no prefetching"
./cg-no;./cg-no;./cg-no
cd ../arm-offsets
for i in 2 4 8 16 32 64 128 256
do
  echo ""
  echo "***************"
  echo "offset " $i
  ./cg-offset-$i;./cg-offset-$i;./cg-offset-$i;
done
echo ""
echo "---------------------------------"
echo ""
echo "is"
cd ../../../nas-is/bin/arm
echo ""
echo "***************"
echo "no prefetching"
./is-no;./is-no;./is-no
cd ../arm-offsets
for i in 2 4 8 16 32 64 128 256
do
  echo ""
  echo "***************"
  echo "offset " $i
  ./is-offset-$i;./is-offset-$i;./is-offset-$i;
done
echo ""
echo "---------------------------------"
echo ""
echo "rand"
cd ../../../randacc/bin/arm
echo "no prefetching"
time ./randacc-no 100000000;time ./randacc-no 100000000;time ./randacc-no 100000000;
cd ../arm-offsets
for i in 2 4 8 16 32 64 128 256
do
  echo ""
  echo "***************"
  echo "offset " $i
  time ./randacc-offset-$i 100000000;time ./randacc-offset-$i 100000000;time ./randacc-offset-$i 100000000;
done
cd ../../../hashjoin-ph-2/src/bin/arm
echo ""
echo "---------------------------------"
echo ""
echo "hj2"
echo ""
echo "***************"
echo "no prefetching"
./hj2-no -a NPO_st -r 12800000 -s 12800000;./hj2-no -a NPO_st -r 12800000 -s 12800000;./hj2-no -a NPO_st -r 12800000 -s 12800000;
cd ../arm-offsets
for i in 2 4 8 16 32 64 128 256
do
  echo ""
  echo "***************"
  echo "offset " $i
  ./hj2-offset-$i -a NPO_st -r 12800000 -s 12800000;./hj2-offset-$i -a NPO_st -r 12800000 -s 12800000;./hj2-offset-$i -a NPO_st -r 12800000 -s 12800000;
done

} &>results_arm_fig6.out
