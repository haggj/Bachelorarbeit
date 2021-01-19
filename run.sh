if [ $1 = "build" ]; then
    # Building docker container
    sudo docker build -t benchmark .
elif [ $1 = "benchmark" ]; then
    # Building docker container
    echo "Building docker container..."
    sudo docker build -t benchmark . >> /dev/null
    # Execute benchmarks within container
    echo "Running benchmarks..."
    echo -e "\e[31mWarning: This takes several hours...\e[0m\n"
    sudo docker run --privileged -t -v $PWD/.tmp:/usr/src/app/data benchmark python3 benchmarking.py $2
    # Extract results
    sudo rm -rf data/
    cp -r .tmp/ data/
    sudo rm -r .tmp/
elif [ $1 = "test" ]; then
    # Building docker container
    echo "Building docker container..."
    sudo docker build -t benchmark . >> /dev/null
    # Execute unit tests within container
    sudo docker run benchmark pytest --color=yes -o log_cli=true --log-cli-level=INFO -k "TestSIKE"
elif [ $1 = "coverage" ]; then
    # Building docker container
    echo "Building docker container..."
    sudo docker build -t benchmark . >> /dev/null
    # Execute unit tests within container
    sudo docker run benchmark pytest --cov=src --cov-report term-missing src/test/ -v
elif [ $1 = "bash" ]; then
    # Building docker container
    echo "Building docker container..."
    sudo docker build -t benchmark . >> /dev/null
    # Execute unit tests within container
    sudo docker run  --privileged -ti benchmark bash
else
    echo "Command not found"
fi