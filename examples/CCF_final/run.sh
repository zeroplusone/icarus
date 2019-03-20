#/bin/sh

# check arguments
if [ $# -ne 3 ] && [ $# -ne 2 ]; then
    echo "Please enter #content provider as the first argument."
    echo "Please enter #user group as the second argument"
    echo "To skip baseline simulation, the third arguement, name of simulation directory (ex. simTime2019-03-19_154133), is required."
else
    # initialize variables
    contentProvider=$1
    userGroup=$2
    rootPath=`pwd`
    experimentPath="content_provider/"$contentProvider"-"$userGroup
    resultPath=$experimentPath

    # Step 1. Run basedline experiment
    if [ $# -eq 2 ]; then
        date=`date +%Y-%m-%d_%H%M%S`
        resultPath=$resultPath"/simTime"$date
        demandPath=$experimentPath"/"$contentProvider"-"$userGroup"-total.txt"
        if ! [ -f $demandPath ]; then
            echo $demandPath" not exist."
        else
            echo "start baseline simulation at "$date"..."
            echo `mkdir $resultPath`

            sed -i '' "s/source_number[[:space:]]=[[:space:]].*/source_number = $contentProvider/g" config.py

            for ((i=1;i<=$userGroup;i=i+1))
            do
                # transfer CRLF to LF
                tr -d "\r" < $demandPath > tmp && mv tmp $demandPath
                # create demand dictionary of each usergroup
                demand=`awk -v cpN=$contentProvider -v ugN=$userGroup -v ugNow=$i 'BEGIN{ORS=","}(ugNow==$2){print cpN+$1":"$3}' $demandPath`
                demand='{'${demand%?}'}'
                # replace demand into config file
                sed -i '' "s/.*source_weights.*[[:space:]]=[[:space:]].*/        experiment['content_placement']['source_weights'] =  $demand/g" config.py
                # run simulation
                icarus run --results result.pickle config.py >> $resultPath/"source_popularity_list.txt"
                icarus results print result.pickle > $resultPath/"result_"$i".txt"
                # store baseline data
                dataPath=$resultPath"/user_group_"$i
                echo `mkdir $dataPath`
                echo `mv record_workload $dataPath/`
                echo `mv record_workload_pdf $dataPath/`
                echo `mv record_content $dataPath/`
                echo `mv provider_popularity $dataPath/`
            done

            sed -i '' "s/.*source_weights.*[[:space:]]=[[:space:]].*/        experiment['content_placement']['source_weights'] = {}/g" config.py
        fi
    fi


    # Step 2. Run CCF experiment
    if [ $# -eq 3 ]; then
        resultPath=$resultPath"/"$3
    fi
    echo $resultPath
    CCF_files=(`ls $experimentPath/*.tsv`)
    for file in ${CCF_files[@]}
    do
        fileName=`cut -d / -f 3 <<< $file`
        echo "start CCF simulation on "$resultPath" by using"$fileName
        for ((i=1;i<=$userGroup;i=i+1))
        do
            # create CCF config.py
            dataPath=$resultPath"/user_group_"$i
            cp config.py $dataPath"/"
            sed -i '' 's/IS_BASELINE[[:space:]]=[[:space:]].*/IS_BASELINE = False/g' $dataPath/config.py
            allocation=`awk -v ugNow=$i 'BEGIN{ORS=","}($2==ugNow){print $3}' $file`
            allocation='['${allocation%?}']'
            sed -i '' "s/.*cache_allocation.*/        experiment['cache_placement']['cache_allocation'] = $allocation/g" $dataPath"/config.py"
            
            dirname=$rootPath"/"$dataPath
            (cd $dirname && icarus run --results result.pickle config.py && icarus results print result.pickle > "../"$fileName"_result_"$i".txt")
        done
    done
fi


