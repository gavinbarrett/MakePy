# Description
This is a small python utility for generating Makefiles for C and C++ programs.

# Installation
Currently, MakePy is only being released for Linux distributions.

Install it by running
```bash
# download the raw python script
wget https://raw.githubusercontent.com/gavinbarrett/MakePy/master/makepy.py

# set executable permissions on the script
chmod +x makepy.py

# move the scipt to a place in your path
mv makepy.py /usr/local/bin
```

Alternatively, if you have Git installed, run:
```bash
# clone to repo to some directory for storing software
git clone https://github.com/gavinbarrett/MakePy /tmp

# enter the directory
cd MakePy

# set executable permissions on the script
chmod +x makepy.py

# move the scipt to a place in your path
mv makepy.py /usr/local/bin

# (Optional) Remove the MakePy directory
rm -fr /tmp/MakePy
```

In the future, MakePy will be available through the pip package manager.

# Usage
You can then run the script 
```python
makepy.py <executable> <project>
```

This command will run the MakePy.py script in the \<project\> directory and output a file named Makefile in the \<project\> directory containing a rule for building the binary executable named \<executable\>.
