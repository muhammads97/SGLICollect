unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
if [ $machine = "Linux" ] 
then
    out="./dist/linux"
elif [ $machine = "Mac" ] 
then
    out="./dist/mac"
elif [ $machine = "MinGw" ] 
then
    out="./dist/mingw"
elif [ $machine = "./dist/cygwin" ] 
then
    out="./dist/cygwin"
else
    echo "unsupported OS"
    exit
fi
    rm -r $out
    pyinstaller -F launcher.py --name SGLICollect --distpath $out\
        -p . \
        -p src \
        -p src/extractors \
        -p src/gportal \
        -p src/gportal/gportal_types \
        -p src/jasmes \
        -p src/jasmes/jasmes_types \
        --hidden-import src \
        --hidden-import io \
        --hidden-import io.open \
        --collect-all src \
        --noconfirm
