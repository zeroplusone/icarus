#/bin/sh

if [ $# -ne 3 ]; then
    echo "Please enter #user group as the first argument"
    echo "Please enter the directory name in result folder as the second argument. ex. simTime2018-12-14_183032"
    echo "Please enter the path of allocation file as the third argument."
else
    runTime=$1
    rootPath=`pwd`
    resultPath="result/"$2
    allocationPath=$3
    if ! [ -d $resultPath ]; then
        echo $resultPath" not exist."
    else
        echo "start CCF simulation on "$resultPath
        for((i=0;i<$runTime;i=i+1))
        do
            userGroupPath=$resultPath"/user_group_"$i
            cp config2.py $userGroupPath/config.py
            startLine=$(( 10*$i+1 ))
            endLine=$(( 10*($i+1) ))
            allocation=`sed -n "${startLine},${endLine} p" $allocationPath | awk '!(NR%10){print p","$0}{p=p","$0}' `
            allocation='['${allocation:1}']'
            sed -i '' "s/.*cache_allocation.*/        experiment['cache_placement']['cache_allocation'] = $allocation/g" $userGroupPath"/config.py"
            
            dirname=$rootPath"/"$userGroupPath
            (cd $dirname && icarus run --results result.pickle config.py > "source_popularity_list.txt" && icarus results print result.pickle > "../"$allocationPath"_result_"$i".txt")
            # icarus results print $userGroupPath/result.pickle > $userGroupPath"/result_"$i".txt"
        done
    fi
fi


