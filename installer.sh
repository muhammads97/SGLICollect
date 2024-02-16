unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

echo "Welcome to SGLICollect installer script."

if [ $machine = "Linux" ] 
then
    # ask for installation location
    installation_dir=$(pwd)
    echo "Please enter installation loaction (default: ${installation_dir}):"
    read user_input
    if [ ${#user_input} -gt 0  ]
    then
        if ! [ -d $user_input ] 
        then
            echo "${user_input} is not a valid directory"
            exit
        fi
        installation_dir=$user_input
    fi
    echo "SGLICollect is going to be installed in: ${installation_dir}"
    echo "Making SGLICollect directory.."
    sc_dir="${installation_dir}/SGLICollect/"
    mkdir $sc_dir -p
    cd $sc_dir
    tag=$(git ls-remote --refs --tags https://github.com/muhammads97/SGLICollect.git \
    | cut --delimiter='/' --fields=3     \
    | tr '-' '~'                         \
    | sort --version-sort                \
    | tail --lines=1 )
    echo "Installing SGLICollect version=${tag}.."
    curl \
    -H 'Accept: application/vnd.github.v3.raw' \
    -O -L "https://github.com/muhammads97/SGLICollect/raw/${tag}/dist/linux/SGLICollect"

    chmod +x "${sc_dir}/SGLICollect"

    echo "Installation completed! add (${sc_dir}) to your system path to use SGLICollect from any directory."

elif [ $machine = "Mac" ]
then
# ask for installation location
    installation_dir=$(pwd)
    echo "Please enter installation loaction (default: ${installation_dir}):"
    read user_input
    if [ ${#user_input} -gt 0  ]
    then
        if ! [ -d $user_input ] 
        then
            echo "${user_input} is not a valid directory"
            exit
        fi
        installation_dir=$user_input
    fi
    echo "SGLICollect is going to be installed in: ${installation_dir}"
    echo "Making SGLICollect directory.."
    sc_dir="${installation_dir}/SGLICollect/"
    mkdir $sc_dir -p
    cd $sc_dir
    tag=$(git ls-remote --refs --tags https://github.com/muhammads97/SGLICollect.git \
    | cut --delimiter='/' --fields=3     \
    | tr '-' '~'                         \
    | sort --version-sort                \
    | tail --lines=1 )
    echo "Installing SGLICollect version=${tag}.."
    curl \
    -H 'Accept: application/vnd.github.v3.raw' \
    -O -L "https://github.com/muhammads97/SGLICollect/raw/${tag}/dist/linux/SGLICollect"

    chmod +x "${sc_dir}/SGLICollect"

    echo "Installation completed! add (${sc_dir}) to your system path to use SGLICollect from any directory."
fi