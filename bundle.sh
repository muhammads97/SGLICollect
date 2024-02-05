rm -r ./dist
pyinstaller -F launcher.py --name SGLICollect \
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

mkdir ./dist/SGLICollect/temp
touch ./dist/SGLICollect/temp/.gitkeep