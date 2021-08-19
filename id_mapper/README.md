# ID Mapper
This is a small script that I wrote few years back to do mapping of students' IDs between two systems. To do the work manually, It would take me forever to map 300+ students at times, with this script, I get the work done within 3 minutes for 300 students. 

To invoke the code:
* a `secrets.py` file needs to be in the same directory, which contains 4 fixed variables including the username and password.
* at the command line type `python id_mapper.py -i <your_input_file.csv>`
* as a result the code will generate a new file with name `<processed_your_input_file.csv>
