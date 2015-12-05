# encoding: utf-8

from __future__ import unicode_literals

import io
import os.path
import hashlib
import pytest

from cinje import benchmark
from cinje.util import flatten


# Let's just say, the end result is tremendously large.
EXPECT = '04c074de62bad5d428f24b3610974c2096a8a0b6f13a3827d1267f3537c112e2'


def test_benchmark_io_open():
	a = io.open(os.path.join(os.path.dirname(__file__), '../cinje/benchmark.py'), mode='r', encoding='cinje').read()
	assert 'def bigtable(' in a
	env = dict()
	exec(a, env)


def test_benchmark_bigtable():
	result = list(benchmark.bigtable())
	assert len(result) == 1
	result = hashlib.sha256(flatten(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_unsafe():
	result = list(benchmark.bigtable_unsafe())
	assert len(result) == 1
	result = hashlib.sha256(flatten(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_stream():
	result = list(benchmark.bigtable_stream())
	assert len(result) > 1
	result = hashlib.sha256(flatten(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_fancy():
	result = list(benchmark.bigtable_fancy())
	assert len(result) > 1
	result = hashlib.sha256(flatten(result).encode('utf8')).hexdigest()
	assert result == EXPECT
