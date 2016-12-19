#wtfcf
> Disclaimer: there's no warranty of anything.

Currently, it only supports C++.

## Installation
To install it:
```shell
git clone https://github.com/monkey2000/wtfcf.git ~/.wtfcf
cp ~/.wtfcf/example/wtfcf.ini ~/.wtfcf.ini
pip install -r ~/.wtfcf/requirements.txt
```

Then add `~/.wtfcf/bin` to your `$PATH`.

## Getting Started
To download a problem:
```shell
mkcf http://www.codeforces.com/contest/689/problem/D    # Round #361 (Div. 2) Friends and Subsequences
```

To test your program:
```shell
testcf
```

## Setting Up a Proxy
Go and see `example/wtfcf.ini`.

