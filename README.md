# memoryWords

A simple word-memory program based on Python.

[Download version 1.1](https://github.com/jhhan128/memoryWords/raw/main/memoryWords.zip)

## Features
1. When you give personal word list, this program helps to memorize them.

2. it gives N-random words from your word list, and the number can be selected by you.

3. It shows word, and pronounces it. (Voice by Google TTS)

4. 4 different choices of meanings will be shown, and you'll have to choose the right answer.


## Requirements
- **Python 3.9**(or higher version)
- **NanumBarunGothic Font**(Not necessary) - Can be downloaded from https://hangeul.naver.com/font
- **Required Python libraries** - `gTTS`, `playsound`, `PyQt5`
```
> pip3 install gTTS
> pip3 install playsound==1.2.2
> pip3 install PyQt5
```
> Note: On Higer version of `playsound`, there may be an error at playing the sound, please use version `1.2.2`



## How to use
1. Make your word list. The word and its meaning has to be divided by `|`, like `like|simmilar to`, and add the list to `dist` folder.

2. Then you'll have to enter the informations about how you're going to use this program. Open the file `dist/inf.txt`, and add the informations the file requires.

3. When everything is finished, you can run the program by running `Windows_RUN.bat` or `macOS_RUN.sh`.



## Screenshots

<img width="718" alt="스크린샷 2024-01-07 20 57 48" src="https://github.com/jhhan128/memoryWords/assets/54146988/5b732ae9-7092-4679-927d-be59351af048">
