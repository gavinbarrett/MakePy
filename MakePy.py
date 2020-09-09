from os import path
from sys import argv, exit
from glob import glob
import re

class FileObject:
	def __init__(self, name, abspath, relpath, objname, depends, main):
		self.name = name
		self.abspath = abspath
		self.relpath = relpath
		self.objname = objname
		self.dependencies = depends
		self.main = main


def make_makefile(CC, CFLAGS, STD, CLEAN, OUT, FOBJS):
	LINKS = ''
	with open('Makefile', 'w') as outfile:
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


def set_makefile(compiler, outfile, fobjs):
	# set compiler variables
	CC = f'CC = {compiler}'
	CFLAGS = f'CFLAGS = -Wall -Werror'
	STD = 'STD = -std=c11'
	CLEAN = f'clean:\n\trm {argv[1]} *.o'

	# generate makefile
	make_makefile(CC,CFLAGS,STD,CLEAN,outfile,fobjs)


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


def build_map(line, deps, main):
	if (line[0] == "#include"):
		if (line[1][0] == '<'):
			deps.append(line[1].strip('<>\n'))
		if (line[1][0] == '"'):
			deps.append(line[1].strip('"\n'))
			
	# file is a main file
	if (line[0] == "int" and re.match('main\(.*\)', line[1])):
		#print('main file')
		main = True


def get_dependencies(h, c, cpp):
	files = []
	for cf in c:
		f = open(cf, 'r')
		lines = [e.split(' ') for e in f.readlines()]
		deps = []
		main = False
		for line in lines:
			build_map(line, deps, main)
		regex = re.compile('\.c$')
		c_f = list(filter(regex.search, cf.split('/')))[0]
		rel = cf.split('/')
		rel.pop()
		rel = '/'.join(rel)
		print(c_f)
		of = re.sub('\.c$', '.o', c_f)
		ef = FileObject(c_f, cf, rel, of, deps, main)
		print(f'Mapping {ef.name}')
		files.append(ef)
		f.close()
	return files


def main():
	if (len(argv) < 3):
		exit()
	direct = argv[2]
	if (path.isdir(direct)):
		h, c, cpp = grab_files(direct)
		fobjs = get_dependencies(h, c, cpp)
		set_makefile('gcc', argv[1], fobjs)
	else:
		print('Provided path is not a directory.')
		exit()


if __name__ == "__main__":
	main()
