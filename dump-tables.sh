#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

database=$1
for table in `sqlite3 $database .tables`
do
    output="table-"$table".txt"
    echo "try to dump: $table to $output" 
    sqlite3 $database ".dump $table" > $output
done
