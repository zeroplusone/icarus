#/bin/sh

if [ $# -ne 2 ]; then
    echo "Please enter #user group as the first argument"
    echo "Please enter the path of allocation file as the third argument."
else
    if ! [ -d result ]; then
        echo "#Create result directory..."
        echo `mkdir result`
    fi

    runTime=$1
    date=`date +%Y-%m-%d_%H%M%S`
    resultPath="result/simTime"$date
    rootPath=`pwd`
    demandPath=$2
    if ! [ -f $demandPath ]; then
        echo $demandPath" not exist."
    else
        echo "start simulation at "$date"..."
        echo `mkdir $resultPath`

        for((i=0;i<$runTime;i=i+1))
        do
            startLine=$(( $runTime*$i+1 ))
            endLine=$(( $runTime*($i+1) ))
            key=$(( $runTime+1 ))
            demand=`sed -n "${startLine},${endLine} p" $demandPath | awk -v key=$key '!(NR%100){print p","key+(NR-1)%100":"$0}{p=p","key+(NR-1)%100":"$0}' `
            demand='{'${demand:1}'}'
            sed -i '' "s/.*source_weights.*[[:space:]]=[[:space:]].*/                experiment['content_placement']['source_weights'] =  $demand/g" config.py
        
            icarus run --results result.pickle config.py >> $resultPath/"source_popularity_list.txt"
            icarus results print result.pickle > $resultPath/"result_"$i".txt"
            dataPath="result/simTime"$date"/user_group_"$i
            echo `mkdir $dataPath`
            echo `mv record_workload $dataPath/`
            echo `mv record_workload_pdf $dataPath/`
            echo `mv record_content $dataPath/`
            echo `mv provider_popularity $dataPath/`

        done
    fi
fi


