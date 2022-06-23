# pypairtree [![Build Status](https://github.com/unt-libraries/pypairtree/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/pypairtree/actions)

pypairtree is a Python implementation of Pairtree for storing objects
in a filesystem hierarchy that maps object identifiers to two character
directory paths (http://tools.ietf.org/html/draft-kunze-pairtree-01).

## License

See LICENSE.txt.

## Acknowledgements

pypairtree was developed at the UNT Libraries and has been worked on
by a number of developers over the years including

- [Kurt Nordstrom](https://github.com/kurtnordstrom)
- Brandon Fredericks
- [Mark Phillips](https://github.com/vphill)
- [Lauren Ko](https://github.com/ldko)
- [Joey Liechty](https://github.com/yeahdef)
- [Gio Gottardi](https://github.com/somexpert)

If you have questions about the project feel free to contact Mark Phillips
at mark.phillips@unt.edu.

## Installation

Install with:
```sh
$ python setup.py install
```

## Tests

Unit tests are provided. To run them via Tox, ensure you are in the
pypairtree directory with the tox.ini file and execute:

```sh
$ tox
```
