# Protobuf oneof-cases listing plugin

A protobuf plugin to generate listing text of oneof-cases in protobuf's protocol file using template text.

This plugin uses [jinja2 template engine](https://jinja.palletsprojects.com/). We can use [jinja2 format](https://jinja.palletsprojects.com/en/3.0.x/templates/) in template texts.

This is a short plugin written in Python.
This plugin can use as a simple example for writing protobuf(protoc) plugins.

## Dependencies
(Version numbers are versions checked by me, not mean must-use versions)
  - Python 3.8.9
  - jinja2 2.11.3
  - inflection 0.5.1
  - protobuf 3.15.2


## Plugin Parameters
  * template: template file glob (e.g. "*.tpl", "templates/*.txt.tpl")
    * Out filename will be the same as input filename without ".tpl"

## Example

This repository contains example files. (listing-test-example.proto, listing-test-example.txt.tpl)

Example usage: 
```bash
# (In repo root)
$ mkdir out
$ protoc listing-test-example.proto --plugin="protoc-gen-list=./protoc_oneof_listing_plugin.py" \
    --list_out=templates=./listing-test-example.txt.tpl:./out/
```

should out (in out/listing-test-example.txt)

```
This is test of listing.

[ Oneof: test::TestCases1::body ]
TestMessage1 - test_msg1
 // Name converted: TestMsg1, testMsg1, test_msg1, TEST_MSG1

TestMessage2 - test_msg2
 // Name converted: TestMsg2, testMsg2, test_msg2, TEST_MSG2

TestMessage3 - test_msg3
 // Name converted: TestMsg3, testMsg3, test_msg3, TEST_MSG3

[ Oneof: test::TestCasesFoo::body ]
TestMessage1 - foo1
 // Name converted: Foo1, foo1, foo1, FOO1

TestMessage2 - foo2
 // Name converted: Foo2, foo2, foo2, FOO2
```

## License

- Copyright (C) 2021 Sunaga-Lab, Inc.
- This software is released under the MIT License.
- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
