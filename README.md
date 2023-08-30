This fork is just a modified version of Ayman0x03's script, all credit goes to him
# massar-py
Python script to use [moutamadris](https://massarservice.men.gov.ma/moutamadris/Account)
 to avoid using the slow website
 
## Requirements
In order to use the script you need ```lxml```, ```pandas```,and ```requests```.

You can doit by simply running the follwing command.
```
pip install requirements.txt 
```
## Notes 
-If the website is compltely non functioning it won't work.

-This fork makes it so that if you do not want to type in the current school year every time, you can just leave the prompt that asks you for the school year blank ( massar shut down the ability to get your school years :/ )

-Saves your grades into a cvs file called grades.cvs

-This fork of the script adds the ability to save your credentials to a creds.txt file, just create the file and add:

```
username=(your username)

password=(your password)
```
if the script doesn't detect the creds.txt file, write the whole path in: Line 31: with open(r'creds.txt', 'r') as file:

## To Do List
- [ ] support the [waliye website](https://massarservice.men.gov.ma/waliye/Account).

