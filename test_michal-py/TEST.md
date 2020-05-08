# Tests

For unit tests used [unittest package](https://docs.python.org/3/library/unittest.html).
All tests are in the directory *michal-py/test_michal-py*.

---

## Unit

- Case 1. Test specific image. We set file name<br/> 
```fname = 'MwPic_30_1_2015__16_1__29_407.JPG'``` after that imread:<br/>
```img = cv2.imread('./dataset/' + fname)``` and put into main module function:<br/>
```final, d1, d2, hw = hw_detector(img, fname, template, config)```
Exelent we get an annotated image, two bounding box diagonals and calculated hardness. 
Unit test is passed when template and input images sizes not empty, 
and output bounding box parameters are greater than 0.

Start unit tests:<br />
```
cd michal-py
./scripts/test.sh
```
or using PyCharmIDE:<br/>

```*Run->* 'test.py':```

---