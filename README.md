# memoryWords

A simple word-memory program based on Python.

## Features
1. When you give personal word list, this program helps to memorize them.

2. it gives N-random words from your word list, and the number can be selected by you.

3. It shows word, and pronounces it. (Voice by Google TTS)

4. 4 different choices of meanings will be shown, and you'll have to choose the right answer.

## Screenshots


## Requirements
- **Python 3.9**(or higher version)
- **NanumBarunGothic Font**(Not necessary) - Can be downloaded from https://hangeul.naver.com/font
- **Required Python libraries** - `gTTS`, `playsound`, `PyQt5`
```
> pip3 install gTTS
> pip3 install playsound
> pip3 install PyQt5
```

## How to use
1. Make your word list. The word and its meaning has to be divided by `|`, like `like|simmilar to`, and add the list to `lib` folder.

2. Then you'll have to enter the informations about how you're going to use this program. Open the file `lib/inf.txt`, and add the informations the file requires.

3. When everything is finished, you can run the program by running `src/exec.py`.
```
> python3 src/exec.py
```