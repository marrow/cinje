# encoding: utf-8

from __future__ import unicode_literals

import hashlib
import base64
import gzip

import cinje

from cinje import benchmark
from cinje.util import s


# Let's just say, the end result is tremendously large.
EXPECT = '04c074de62bad5d428f24b3610974c2096a8a0b6f13a3827d1267f3537c112e2'



def test_benchmark_bigtable():
	result = list(benchmark.bigtable())
	assert len(result) == 1
	result = hashlib.sha256(s(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_unsafe():
	result = list(benchmark.bigtable_unsafe())
	assert len(result) == 1
	result = hashlib.sha256(s(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_stream():
	result = list(benchmark.bigtable_stream())
	assert len(result) > 1
	result = hashlib.sha256(s(result).encode('utf8')).hexdigest()
	assert result == EXPECT


def test_benchmark_bigtable_fancy():
	result = list(benchmark.bigtable_fancy())
	assert len(result) > 1
	result = hashlib.sha256(s(result).encode('utf8')).hexdigest()
	assert result == EXPECT

