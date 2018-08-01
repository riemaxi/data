
All the programs have essentially the same structure

A file with the models: model.h
A file with the main program that uses the models: shell.cpp
A parameter file used by both cpp and python code: model.par
A script that normalize the output from Gecode: report.py
A script that calculate the average: report_average.py
A script that rules them all: report.bat

To compile:
 1- Enter the corresponding folder
 2- run ..\build.bat
 
 To run:
 1- update model.par with custom parameters
 2- run report.bat
 
 result is saved on report.tsv
 
 To clear all:
  ..\clear.bat
  
 The coding has been made as clear as possible acoiding class hierarchies, i.e, every case has a class of its own.
 As a result the logic is fairly easy to follow