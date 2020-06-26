#Building docker container
echo "Building docker container..."
sudo docker build -t benchmark .
#Execute benchmarks within container
echo "Running benchmarks..."
echo -e "\e[31mWarning: This takes several hours...\e[0m"
sudo docker run -t -v $PWD/.tmp:/usr/src/app/diagrams benchmark
#Extract results
sudo rm -rf data/
cp -r .tmp/ data/
sudo rm -r .tmp/
