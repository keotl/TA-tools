if (( $# != 1 )); then
    echo "missing parent dir"
fi

startingDir=$(pwd)
for dir in $1/*/
do
    dir=${dir%*/}
    cd ${dir} && rm -rf .git && cd ${startingDir}
done
