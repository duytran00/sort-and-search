import sys
import re
import os
import subprocess
import io

SRC = "text_indexing.c"

if(len(sys.argv) < 2):
    print("Usage: python gradeSorting.py filename.txt [--valgrind] [--verbose]")
    print("\tTests your program against the test file provided as argument")
    print("\t[] indicates optional arguments")
    print("\tUse --valgrind flag to test with valgrind")
    print("\tUse --verbose to test code in verbose mode. The default is normal mode.")
    exit(1)

filename = sys.argv[1]
useValgrind = False
useVerbose = False
testBinarySearch = False
if "--valgrind" in sys.argv:
    useValgrind = True
if "--verbose" in sys.argv:
    useVerbose = True

cmd = ''
if useVerbose:
    cmd = f"./text-indexing 1 {filename}"
else:
    cmd = f"./text-indexing 0 {filename}"

mode = 1 if useVerbose else 0

print("cmd:", cmd)

words = []
with open(filename, 'r') as inputFile:
    print(f"Testing with file {filename}...")
    words = re.split(r"[ ,\.\?!()-/\n]", inputFile.readline())
    while '' in words:
        words.remove('')
    # words = [x.lower() for x in words]
    print(words)
    
print("Compiling your code...")
if os.system(f"gcc {SRC} -g -o text-indexing") != 0:
    print("Your code did not compile cleanly. Test failed. ❌")
    exit(1)
else:
    print("Your code compiled cleanly. ✅")

if useValgrind:
    # print(f"valgrind --leak-check=full --show-leak-kinds=all {cmd}")
    s = subprocess.run(f"valgrind --leak-check=full --show-leak-kinds=all {cmd}", shell=True, timeout=10, capture_output=True)
    if s.returncode != 0:
        print("Valgrind error(s) were detected or your program did not exit with return code 0.")
        print("Test failed. ❌")
        print("To test without valgrind, run without --valgrind")
        print(s.stderr.decode('utf-8'))
        exit(1)
    else:
        print("No Valgrind errors. ✅")

print("Testing program...")
process = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
if process.returncode != 0:
    print("Your program returned a non-zero exit code. Test failed. ❌")
    print(process.stdout.decode('utf-8'))
    exit(1)
output = io.StringIO(process.stdout.decode('utf-8'))

line = output.readline().strip()
if f"mode: {mode}" not in line or f"file: {filename}" not in line:
    print("Incorrect top line. Do not modify the code provided. Test failed. ❌")
    print(f"Expected: mode: {mode}  file: {filename}")
    print(f"Received: {line}")
    exit(1)

line = output.readline().strip()
while line == '':
    line = output.readline().strip()
if "original data" not in line.lower():
    print("Second nonempty line of output must be \"-- Original data --\". See sample runs. Test failed. ❌")
    exit(1)

if not useVerbose:
    print("(Testing in normal mode)")
    for i, word in enumerate(words):
        line = output.readline().strip()
        lineContent = line.split()
        if int(lineContent[0]) != i or lineContent[1] != word:
            print(f"Expected: \"{i} {word}\"")
            print(f"Received: \"{line}\"")
            print("Test failed. ❌")
            exit(1)
    line = output.readline().strip()
    if line == '':
        line = output.readline().strip()
    else:
        print("Remember to print an extra newline after printing the list")

    if "sorted" not in line.lower() or "clean" not in line.lower() or "data" not in line.lower():
        print("Expected: \"-- Clean and sorted data --\"")
        print("Received:", line)
        print("Test failed. ❌")
        print("Please compare your output with the expected output.")
        exit(1)

    words = [x.lower() for x in words]
    words.sort()
    for i, word in enumerate(words):
        line = output.readline().strip()
        while line == '':
            line = output.readline().strip()
        lineContent = line.split()
        if int(lineContent[0]) != i or lineContent[1] != word:
            print(f"Expected: \"{i} {word}\"")
            print(f"Received: \"{line}\"")
            print("Test failed. ❌")
            exit(1)
else: # Verbose mode
    print("(Testing in verbose mode)")
    line = output.readline().strip()
    while line == '':
        line = output.readline().strip()
    lineCheck = line.replace("|", "").split()
    expectedHeader = "  i  |   pointers[i]    | word\n"
    if(lineCheck[0] != 'i' or lineCheck[1] != 'pointers[i]' or lineCheck[2] != 'word'):
        print("Expected:", expectedHeader)
        print("Received:", line)
        print("Incorrect verbose table header. Test failed. ❌")
        exit(1)
    
    line = output.readline()
    if "-" not in line:
        print("Missing line of dashes (-) after table header. Test failed. ❌")
        exit(1)
        
    wordsWithPointers = []
    # print(words)
    for i, word in enumerate(words):
        line = output.readline().strip()
        while(line == ''):
            line = output.readline().strip()
        lineContent = line.replace("|", "").split()
        # print(lineContent)
        if int(lineContent[0]) != i:
            print(f"Received: {line}")
            print(f"Expected index {i}")
            print("Test failed. ❌")
            exit(1)
        if lineContent[2] != word:
            print(f"Received word |{lineContent[1]}|")
            print(f"Expected word |{word}|")
            print("Test failed. ❌")
            exit(1)
        wordsWithPointers.append((lineContent[2].lower(), lineContent[1]))   
    # print(wordsWithPointers)
    wordsWithPointers.sort(key=(lambda x: x[0]))
    # print(wordsWithPointers)

    print("Table output before sorting is correct. ✅")

    # Check sorted order
    line = output.readline().strip()
    while line == '':
        line = output.readline().strip()
    if "sorted" not in line.lower() or "clean" not in line.lower() or "data" not in line.lower():
        print("Expected: \"-- Clean and sorted data --\"")
        print("Received:", line)
        print("Test failed. ❌")
        print("Please compare your output with the expected output.")
        exit(1)
    line = output.readline().strip()
    while line == '':
        line = output.readline().strip()
    lineCheck = line.replace("|", "").strip().split()
    expectedHeader = "  i  |   pointers[i]    | word"
    # print(lineCheck)
    if(lineCheck[0] != 'i' or lineCheck[1] != 'pointers[i]' or lineCheck[2] != 'word'):
        print("Expected:", expectedHeader)
        print("Received:", line)
        print("Incorrect verbose table header. Test failed. ❌")
        exit(1)
    line = output.readline().strip()
    while line == '':
        line = output.readline().strip()
    if "-" not in line:
        print("Missing line of dashes (-) after table header. Test failed. ❌")
        exit(1)
    for i, (word, pointer) in enumerate(wordsWithPointers):
        line = output.readline().strip()
        while(line == ''):
            line = output.readline().strip()
        lineContent = line.replace("|", "").split()
        if int(lineContent[0]) != i:
            print(f"Received: {line}")
            print(f"Expected index {i}")
            print("Test failed. ❌")
            print("Check your indexing in the sorted table. It should start from 0 and increment by 1 every row.")
            exit(1)
        if lineContent[2] != word:
            print(f"Received word |{lineContent[2]}|")
            print(f"Expected word |{word}|")
            print("Test failed. ❌")
            print("Incorrect sorting order. Please check your sorting code.")
            exit(1)
        if lineContent[1] != pointer:
            print(f"Received pointer |{lineContent[1]}|")
            print(f"Expected pointer |{word}|")
            print("Test failed. ❌")
            print("It looks like your sorting algorithm implementation may not be stable.")
            exit(1)   

print("Sorting is correct ✅")



