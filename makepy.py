#!/usr/bin/env python3

import re
from os import path
from glob import glob
from sys import argv, exit

GREEN = '\u001b[32m'
WHITE = '\u001b[37m'
RED = '\033[91m'
CEND = '\033[0m'

class FileObject:
	
	def __init__(self, name, abspath, relpath, objname, depends, main):
		self.name = name
		self.abspath = abspath
		self.relpath = relpath
		self.objname = objname
		self.dependencies = depends
		self.main = main


def make_makefile(CC, CFLAGS, STD, CLEAN, OUT, FOBJS, PATH):
	with open(f'{PATH}Makefile', 'w') as outfile:
		# write compiler variables
		outfile.write(f'{CC}\n{CFLAGS}\n{STD}\nOBJ = {" ".join([f.objname for f in FOBJS])}\n\n')		

		# write rule for linking executable
		outfile.write(f'{OUT}: $(OBJ)\n')
		outfile.write(f'\t$(CC) $(CFLAGS) $(STD) -o {OUT} $(OBJ)\n\n')

		# write rules for each input file
		for fo in FOBJS:
			outfile.write(f'{fo.objname}: {fo.name} {" ".join(fo.dependencies)}\n')
			outfile.write(f'\t$(CC) $(CFLAGS) $(STD) -c {fo.name} -I.\n\n')

		# write out cleaning rul
		outfile.write(CLEAN);
	print(f'{GREEN}\u2713 Makefile generated for {OUT}{CEND}')


def set_makefile(compiler, outfile, fobjs, path):
	# set compiler variables
	CC = f'CC = {compiler}'
	CFLAGS = f'CFLAGS = -Wall -Werror'
	STD = 'STD = -std=c11'
	CLEAN = f'clean:\n\trm {argv[1]} *.o'
	if (path[-1] != '/'):
		path += '/'

	# generate makefile
	make_makefile(CC,CFLAGS,STD,CLEAN,outfile,fobjs,path)


def grab_files(directory):
	# gather all c files
	files = glob(f'{directory}/**', recursive=True)

	# create regexes for h, c, cc/c++/cpp files
	h_reg = re.compile(r'\.h$')
	c_reg = re.compile(r'\.c$')
	cpp_reg = re.compile(r'(\.cc$)|(\.c\+\+$)|(\.cpp$)')
	
	# filter h, c, and cc/c++/cpp files
	h_files = list(filter(h_reg.search, files))
	c_files = list(filter(c_reg.search, files))
	cpp_files = list(filter(cpp_reg.search, files))
	return h_files, c_files, cpp_files


def build_map(line, dependencies, main):
	# check if file has dependencies
	if (line[0] == "#include"):
		if (line[1][0] == '<'):
			dependencies.append(line[1].strip('<>\n'))
		if (line[1][0] == '"'):
			dependencies.append(line[1].strip('"\n'))
	# FIXME: check for multiple main functions
	# check if file has a main function
	if (line[0] == "int" and re.match('main\(.*\)', line[1])):
		main = True


def determine_regex(compiler):
	return re.compile('\.c$') if compiler == 'gcc' else re.compile('(\.cc$)|(\.c\+\+$)|(\.cpp$)')


def determine_file_type(compiler, c, cpp):
	return c if compiler == 'gcc' else cpp


def get_dependencies(compiler, h, c, cpp):
	
	files = []
	# get the regex for the file type
	regex = determine_regex(compiler)

	# determine whether to iterate through c or cpp files
	c_files = determine_file_type(compiler, c, cpp)

	# iterate through all files
	for c_file in c_files:
		with open(c_file, 'r') as f:
			dependencies = []
			main = False
			lines = [lines.split(' ') for lines in f.readlines()]
			
			# check line for dependencies and main functions
			for line in lines:
				build_map(line, dependencies, main)
			
			# get file name
			c_file_name = list(filter(regex.search, c_file.split('/')))[0]
			
			# strip the absolute path a level above the file
			relpath = c_file.split('/')
			relpath.pop()
			relpath = '/'.join(relpath)
			
			# create object files from .c or .cc/.c++/.cpp
			objfiles = re.sub('\.c$', '.o', c_file_name)
			
			# create a file object
			fileobject = FileObject(c_file_name, c_file, relpath, objfiles, dependencies, main)
			# add fileobject to the list of files
			files.append(fileobject)

	return files


def check_file_format(c, cpp):
	if (len(c) and len(cpp)):
		print(f'{RED}\u2717 Found both .c and .cc/.c++/.cpp files. MakePy currently doesn\'t support compiling C++ programs with C files.{CEND}')
		exit()
	if (not len(c) and not len(cpp)):
		print(f'{RED}\u2717 No .c or .cc/.c++/.cpp found.{CEND}')
		exit()
	return 'gcc' if len(c) else 'g++'


def main():
	if (len(argv) < 3):
		exit()
	direct = argv[2]
	# check if directory exists
	if (path.isdir(direct)):

		# gather all relevant files
		h, c, cpp = grab_files(direct)
	
		# check for c or cpp files
		compiler = check_file_format(c, cpp)
		
		# gather file dependencies
		fobjs = get_dependencies(compiler, h, c, cpp)
		
		# set compiler options and generate makefile
		set_makefile(compiler, argv[1], fobjs, direct)
	else:
		print(f'{RED}\u2717 Provided path is not a directory.{CEND}')
		exit()


if __name__ == "__main__":
	main()
