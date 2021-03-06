"""
This script should replicate all the runs
presented in the paper. Note:
plots will be generated, which need to be manually
closed for the script to continue. It assumes
everything has been compiled already.

NOTE: the RJObject_1DMixture example is fairly time-consuming.
"""
import os

# Python command on your system
my_python = "python"

def run_example(directory):
    os.chdir(directory)
    os.system("./main -s 0")
    os.system(my_python + " showresults.py")
    os.chdir("..")

os.chdir("../code/Examples")
run_example("StraightLine")
run_example("RJObject_1DMixture")
run_example("ABC")

