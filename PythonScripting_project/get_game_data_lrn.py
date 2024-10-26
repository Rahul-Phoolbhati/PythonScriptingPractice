import os
import json
import shutil
import sys

from subprocess import PIPE, run

GAME_DIR_PATTERN = 	"game"
GAME_FILE_EXTENSION = "go"
GAME_COMPILE_COMMAND = ["go", "run"]

def get_all_game_paths(source):
	game_paths = []
	for root, dirs, files in os.walk(source):
		for directory in dirs:
			if GAME_DIR_PATTERN in directory.lower():
				path = os.path.join(source, directory)
				game_paths.append(path)

		break

	return game_paths


def create_dir(path):
	# print(path)
	# addpath = "newone"
	# path = os.path.join(path, addpath)
	# print(path)


	# if not os.path.exists(path):
	# 	os.mkdir(path)				   # no recursive thing work here
	os.makedirs(path, exist_ok=True)   # recursively adding the directories 



def get_name_from_paths(paths, to_strip):
	new_names = []
	for path in paths:
		_, dir_name = os.path.split(path)
		new_dir_name = dir_name.replace(to_strip, "")
		new_names.append(new_dir_name)

	return new_names


def copy_and_overwrite(source, dest):
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(source, dest)



def make_json_metadata_file(path, game_dirs):
	data = {
	"gameNames" : game_dirs,
	"numberOfGames": len(game_dirs)
	}


	with open(path , "w") as file:
		json.dump(data, file, indent=4)     # dumps = dump as string 

	# with open(path , "r") as file:
	# 	datalodaed = json.load(file)

	# print(datalodaed)
	# formatted_data = json.dumps(datalodaed, indent=2)

	# print(formatted_data)
	

def run_command(command, path):
	cwd = os.getcwd()
	os.chdir(path)

	print(command)

	result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
	print("result of compilation =   ", result)

	os.chdir(cwd)


def compile_game_code(path):
	file_to_run = None

	for root, dirs , files in os.walk(path):
		for file in files:
			file_ext = file.split('.')[-1]      # endswith(".go")
			# print(file_ext)
			if file_ext == GAME_FILE_EXTENSION:
				# run_command(file)
				file_to_run = file
				break
		break

	if file_to_run is None:
		return

	run_command( GAME_COMPILE_COMMAND + [file_to_run] , path)




def main(source, target):
	cwd = os.getcwd()
	source_path = os.path.join(cwd, source)
	target_path = os.path.join(cwd, target)

	game_paths = get_all_game_paths(source_path)
	# print(game_paths)
	create_dir(target_path)

	new_dir_names = get_name_from_paths(game_paths, "_game")
	

	for src,dest in zip(game_paths, new_dir_names):
		dest_path = os.path.join(target_path, dest)
		copy_and_overwrite(src, dest_path)
		compile_game_code(dest_path)

	json_file_path = os.path.join(target_path, "metadata.json")
	make_json_metadata_file(json_file_path, new_dir_names)


if __name__ == '__main__':
	args = sys.argv
	if len(args) != 3:
		raise Exception("yuu must pass only source and dest dir -- ")

	source, target = args[1:]

	main(source, target)
	

	