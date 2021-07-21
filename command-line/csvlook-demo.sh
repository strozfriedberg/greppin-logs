#!/usr/bin/env sh

ls -la datasets/

wc -l datasets/*.csv

csvstat -n datasets/employees.csv

csvstat -n datasets/salaries.csv

head -n 5 datasets/employees.csv | csvlook
head -n 5 datasets/salaries.csv | csvlook

csvclean -n datasets/employees.csv

cp datasets/employees.csv datasets/employees-clean.csv
vim datasets/employees-clean.csv

csvclean -n datasets/employees-clean.csv
csvclean -n datasets/salaries.csv

csvstat datasets/employees-clean.csv
csvstat datasets/salaries.csv

csvjoin \
    datasets/employees-clean.csv \
    datasets/salaries.csv > datasets/employees-with-salaries.csv

wc -l datasets/employees-with-salaries.csv
head datasets/employees-with-salaries.csv | csvlook

csvcut -c 1,6 datasets/employees-with-salaries.csv | sha256sum - && \
    sha256sum datasets/salaries.csv
