#/bin/sh

if ! [ -d result ]; then
    echo "#Create result directory..."
    echo `mkdir result`
fi

runTime=$1
date=`date +%Y-%m-%d_%H%M%S`

resultPath="result/simTime"$date

echo "start simulation at "$date"..."
echo `mkdir $resultPath`

# runTime = #userGroup = #content_provider
sed -i '' "s/source_number[[:space:]]=[[:space:]].*/source_number = $1/g" config.py

for((i=0;i<$runTime;i=i+1))
do
    icarus run --results result.pickle config.py >> $resultPath/"source_popularity_list.txt"
    icarus results print result.pickle > $resultPath/"result_"$i".txt"
    dataPath="result/simTime"$date"/user_group_"$i
    echo `mkdir $dataPath`
    echo `mv record_workload $dataPath/`
    echo `mv record_workload_pdf $dataPath/`
    echo `mv record_content $dataPath/`
    echo `mv provider_popularity $dataPath/`
done


