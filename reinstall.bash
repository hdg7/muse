DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CWD=$(pwd)
cd "$DIR" || exit
pip uninstall -y muse
hatch build -t wheel
LATEST_WHEEL=$(ls -t dist | grep '.whl' | head -n 1)
pip install ./dist/"$LATEST_WHEEL"
cd "$CWD" || exit