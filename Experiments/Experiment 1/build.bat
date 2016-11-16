pyinstaller src\Experiment.py -F -i src\resources\uzh.ico
mkdir dist\resources
copy src\resources\*.* dist\resources
mkdir dist\Data
mkdir dist\Data\SimilarityMatrix
mkdir dist\Data\TrialsDetail
mkdir dist\sdl_dll
copy src\sdl_dll\*.* dist\sdl_dll