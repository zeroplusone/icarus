#/bin/sh

# check arguments
if [ $# -ne 2 ]; then
    echo "Please enter #content provider as the first argument."
    echo "Please enter #user group as the second argument"
else
    # initialize variables
    contentProvider=$1
    userGroup=$2
    rootPath=`pwd`
    experimentPath="content_provider/"$contentProvider"-"$userGroup
    date=`date +%Y-%m-%d_%H%M%S`
    resultPath=$experimentPath"/simTime"$date
    demandPath=$experimentPath"/"$contentProvider"-"$userGroup"-total.txt"

    # Step 1. Run basedline experiment
    if ! [ -f $demandPath ]; then
        echo $demandPath" not exist."
    else
        echo "start baseline simulation at "$date"..."
        echo `mkdir $resultPath`

        for((i=0;i<$userGroup;i=i+1))
        do
            # awk -v con=10 -v user=100 -v key=0 '(NR%user==key){if($1==con){print con+$1":"$3}else{print con+$1":"$3}}' 10-100-total.txt
            startLine=$(( $userGroup*$i+1 ))
            endLine=$(( $userGroup*($i+1) ))
            key=$(( $userGroup+1 ))
            demand=`sed -n "${startLine},${endLine} p"  | awk -v key=$key '!(NR%100){print p","key+(NR-1)%100":"$0}{p=p","key+(NR-1)%100":"$0}' `
            demand='{'${demand:1}'}'
            sed -i '' "s/.*source_weights.*[[:space:]]=[[:space:]].*/                experiment['content_placement']['source_weights'] =  $demand/g" config.py
        
            icarus run --results result.pickle config.py >> $resultPath/"source_popularity_list.txt"
            icarus results print result.pickle > $resultPath/"result_"$i".txt"
            dataPath=$resultPath"/user_group_"$i
            echo `mkdir $dataPath`
            echo `mv record_workload $dataPath/`
            echo `mv record_workload_pdf $dataPath/`
            echo `mv record_content $dataPath/`
            echo `mv provider_popularity $dataPath/`

        done
    fi
fi


