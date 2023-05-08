#!/usr/bin/env sh

# Parse option
if [ -z $1 ]; then
    # Show menu
    echo "Note: option can be sent as parameter"
    echo "1. Run Vanilla"
    echo "2. Run with Glances"
    echo "3. Run with Perf"
    echo "0. Cancel"
    
    # Read the option
    read -p "Select an option: " option
else
    # Set the option to the parameter
    option=$1
fi

# Parse option
case $option in
    0)
        echo "Operation canceled by the user"
        exit 1
    ;;
    1)
        echo -e "Running server in vanilla mode\n"
        exec ./scripts/server.py
    ;;
    2)
        echo -e "Running server with glances monitoring\n"
        glances -w -p 24112 & # Run Glances
		exec python3 ./scripts/server.py # Run server
    ;;
    3)
        echo -e "Running server with perf monitoring\n"
		# Exec with perf recording enabled (perf.data)
        exec perf record -g --sample-cpu ./scripts/server.py
    ;;
    *)
        echo "Invalid option"
        exit 2
    ;;
esac