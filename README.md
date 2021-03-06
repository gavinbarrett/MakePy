## Description
This is a small Python utility for generating Makefiles for C and C++ programs.

![](https://github.com/gavinbarrett/MakePy/workflows/MakePy%20Build%20Test/badge.svg)

## Installation
Currently, MakePy is only being released for Linux distributions.

Install it by running
```bash
# download the raw python script
wget https://raw.githubusercontent.com/gavinbarrett/MakePy/master/makepy.py

# move the scipt to a place in your path
mv makepy.py /usr/local/bin
```

Alternatively, if you have Git installed, run:
```bash
# clone to repo to some directory for storing software
git clone https://github.com/gavinbarrett/MakePy /tmp

# enter the directory
cd MakePy

# move the scipt to a place in your path
mv makepy.py /usr/local/bin

# (Optional) Remove the MakePy directory
rm -fr /tmp/MakePy
```

In the future, MakePy will be available through the pip package manager.

## Usage
You can then run the script 
```python
makepy.py <executable> <project>
```

This command will run the MakePy.py script in the \<project\> directory and output a file named Makefile in the \<project\> directory containing a rule for building the binary executable named \<executable\>.

## Testing
As of right now, testing is limited. You can create your own c/c++ project folders, or you can test on the minimal test folder that is provided.

```bash
# run the test script on the test directory
./runtests tests/
```
or
```bash
# run the test script on your project directory
./runtests <project>
```
