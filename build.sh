set echo off
rm -f *.pyz
cp -r ./game ./wrapper/game
cp -r ./visualizer ./wrapper/visualizer
cp -r ./server ./wrapper/server
python3.11 -m zipapp ./wrapper -o ./launcher.pyz -c
rm -rf ./wrapper/game
rm -rf ./wrapper/visualizer
rm -rf ./warpper/server