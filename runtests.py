#!/usr/bin/env python
import sys

import pytest


if __name__ == '__main__':
    args = sys.argv[1:]
    result_code = pytest.main(args)
    sys.exit(result_code)
