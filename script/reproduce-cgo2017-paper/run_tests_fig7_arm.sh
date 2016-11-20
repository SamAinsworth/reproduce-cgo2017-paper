{
cd ../../program
cd hashjoin-ph-8/src/bin/arm
echo ""
echo "---------------------------------"
echo ""
echo "hj8"
echo ""
echo "***************"
echo "no prefetching"
./hj8-no -a NPO_st -r 12800000 -s 12800000;./hj8-no -a NPO_st -r 12800000 -s 12800000;./hj8-no -a NPO_st -r 12800000 -s 12800000;
cd ../arm-offsets
for i in 1 2 3 4
do
  echo ""
  echo "***************"
  echo "prefetches: " $i
  ./hj8-prefetches-$i -a NPO_st -r 12800000 -s 12800000; ./hj8-prefetches-$i -a NPO_st -r 12800000 -s 12800000; ./hj8-prefetches-$i -a NPO_st -r 12800000 -s 12800000;
done

} &>results_arm_fig7.out
