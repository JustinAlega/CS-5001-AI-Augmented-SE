# Code Translation: In Class Exercise with Prompting

## prompts
Contains 2 files: `system-prompt.txt` and `user-prompt.txt`. 

## cpp_programs
Contains 18 CPP programs

## output_code_translation
Inclues two folders:
### Python: Saves your output in this folder.
### Test: The test files for the python codes.

## code_translation.py
Run this python file to generate the code translation.

# How to Run:
```
python code_translation.py --user-prompt-file prompts/user-prompt.txt --system-prompt-file prompts/system-prompt.txt
```

# How to Run Test:
Go to `code_translation` folder. Then run:
```
python -m unittest discover -s test -v
```

# Instructions
- Go the the test output errors and understand what are the common themes. Plan how can you restrict them.

- Go through the tests as well and understand how the tests are setup.

- change only the prompts file and nothing else.