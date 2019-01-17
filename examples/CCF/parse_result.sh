#/bin/sh

if [ $# -ne 3 ] && [ $# -ne 2 ] ; then
    echo "Please enter #user group as the first argument"
    echo "Please enter the directory name in result folder as the second argument. ex. simTime2018-12-14_183032"
    echo "Please enter the path of allocation file as the third argument."
else
    runTime=$1
    resultPath="result/"$2
    if ! [ -d $resultPath ]; then
        echo $resultPath" not exist."
    else
        echo "start parsing result on "$resultPath
        for((i=0;i<$runTime;i=i+1))
        do
            if [ $# -eq 2 ]; then
                filePath=$resultPath"/result_"$i".txt"
            else
                filePath=$resultPath"/"$3"_result_"$i".txt"
            fi
            awk -F'[:,=}]' '/PER_NODE_CACHE_HIT_RATIO/{print $3 $5 $7 $9 $11 $13 $15 $17 $19 $ 21}' $filePath
            # awk -F'[:]' '/SUM_CACHE_HIT_RATIO/{print $2}' $filePath
        done
    fi
fi


