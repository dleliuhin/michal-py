# michal-py
Digital  processing method for determining microhardness based on image data obtained 
using a microhardness tester.

**michal-py** is the application for parsing a group of pictures with images of a 
depression after pressing various materials during the Vickers test with a Qness Q10 
microhardness tester. It is developed based on Python following OpenCV library and 
provides easy-to-use API. With **michal-py**, users can quickly quickly calculate the 
hardness of the material from the image and visualize them.

---

## Installation

The installation procedures in Windows 10 Linux Ubuntu 16.04/14.04 32-bit LTS or 
Linux Mint 19.* 64-bit are shown here as examples.

---

### Dependencies

There are list of inner package dependencies:

- glob
- unittest
- sys 

---

#### OpenCV:

The OpenCV 4.2.0 used as additional library. Install using 
[tutorial](https://pypi.org/project/opencv-python/).

---

#### PyCharm IDE:

See [PyCharm installing](https://www.jetbrains.com/ru-ru/pycharm/).

---

#### Submodules:

---

## [Tests](./test_michal-py/TEST.md)

---

## Development setup

Describing how to install all development dependencies and how to run an automated 
test-suite of some kind. Potentially do this for multiple platforms.

```
cd michal-py
git checkout master
./scripts/run.sh
```
Build project without updating submodules:
```
cd michal-py
git checkout master
./scripts/build.sh
```

Or using PyCharm IDE:

```*Run->* 'main':```

---

## [Release History](./HISTORY.md)

---
    
## Contributing

1. Clone it (<ssh://git@github.com:dleliuhin/michal-py.git>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git add . & git commit -m "Feature. Add some fooBar."`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request to `develop`

---

## Support

Reach out to me at one of the following places!

- Telegram at <a href="http://https://telegram.org" target="_blank">`@DLeliuhin`</a>
- Email at [dleliuhin@gmail.com]().

---
