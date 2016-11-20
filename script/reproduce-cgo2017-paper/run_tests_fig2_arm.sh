{
cd ../../program
cd nas-is/bin/arm
echo ""
echo "---------------------------------"
echo ""
echo "is"
echo ""
echo "***************"
echo "no prefetching"
./is-no;./is-no;./is-no
cd ../arm-offsets
echo ""
echo "***************"
echo "intuitive"
./is-offset-64-nostride;./is-offset-64-nostride;./is-offset-64-nostride;
echo ""
echo "***************"
echo "too small"
./is-offset-2;./is-offset-2;./is-offset-2;
echo ""
echo "***************"
echo "too big"
./is-offset-2048;./is-offset-2048;./is-offset-2048;
echo ""
echo "***************"
echo "best"
./is-offset-64;./is-offset-64;./is-offset-64
} &>results_x86_fig2.out
