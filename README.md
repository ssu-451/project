## *OCR — Optical Character Recognition System*

[![Build Status](https://travis-ci.org/ssu-451/project.svg?branch=master)](https://travis-ci.org/ssu-451/project)

**Description:**
*The system is a neural network that recognizes text presented by the picture. 
The system takes a picture with text as input data. At the output, user receives text from the image.*

**Details:** 
- Development language is **_Python 3_**.
- Used technologies and tools see in [requirements.txt](https://github.com/ssu-451/project/blob/master/requirements.txt).
- To get started see [getting_started.rst](https://github.com/ssu-451/project/blob/master/docs/getting_started.rst).

**System description:**
1. The text in the picture is typed (not handwritten).
2. The text is black on a white background.
3. The picture is in the format *jpeg, png* or *bmp*.
4. System recognizes the following **characters**:
   - **_numbers:_** 0123456789
   - **_letters of english alphabet:_** abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
   - **_symbols:_** .,"?'!-
5. Image should be clear and have proper resolution.
6. If the system can not recognize the text, it displays error message.
7. If the system receives too large or wrong formatted file, it displays error message.
8. Before first time functioning, neural network should be trained. Result of training should be correct recognition of all valid symbols (each symbol separately).
