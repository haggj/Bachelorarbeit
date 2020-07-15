#Building docker container
echo "Building docker container..."
sudo docker build -t benchmark . >> /dev/null
#Execute benchmarks within container
echo "Running benchmarks..."
echo -e "\e[31mWarning: This takes several hours...\e[0m\n"
sudo docker run -t -e LISTEXP= -v $PWD/.tmp:/usr/src/app/data benchmark
#Extract results
sudo rm -rf data/
cp -r .tmp/ data/
sudo rm -r .tmp/
