# Copyright 2018 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import hafnian as hf
from hafnian import hafnian, haf_real, haf_complex


class TestVersion(unittest.TestCase):
    def test_version_number(self):
        res = hf.version()
        self.assertTrue(isinstance(res, str))


class TestPythonInterfaceWrapper(unittest.TestCase):

    def test_array_exception(self):
        with self.assertRaises(TypeError):
            hafnian(1)

    def test_square_exception(self):
        A = np.zeros([2, 3])
        with self.assertRaises(ValueError):
            hafnian(A)

    def test_odd_dim_exception(self):
        A = np.zeros([3, 3])
        with self.assertRaises(ValueError):
            hafnian(A)

    def test_non_symmetric_exception(self):
        A = np.ones([4, 4])
        A[0, 1] = 0.
        with self.assertRaises(ValueError):
            hafnian(A)

    def test_nan(self):
        A = np.array([[2, 1], [1, np.nan]])
        with self.assertRaises(ValueError):
            hafnian(A)

    def test_2x2(self):
        A = np.random.random([2, 2])
        A += A.T
        haf = hafnian(A)
        self.assertEqual(haf, A[0, 1])

    def test_4x4(self):
        A = np.random.random([4, 4])
        A += A.T
        haf = hafnian(A)
        expected = A[0, 1]*A[2, 3] + \
            A[0, 2]*A[1, 3] + A[0, 3]*A[1, 2]
        self.assertEqual(haf, expected)

    def test_real(self):
        A = np.random.random([6, 6])
        A += A.T
        haf = hafnian(A)
        expected = haf_real(A)
        self.assertEqual(haf, expected)

        A = np.random.random([6, 6])
        A += A.T
        A = np.array(A, dtype=np.complex128)
        haf = hafnian(A)
        expected = haf_real(np.float64(A.real))
        self.assertEqual(haf, expected)

    def test_complex(self):
        A = np.complex128(np.random.random([6, 6]))
        A += 1j*np.random.random([6, 6])
        A += A.T
        haf = hafnian(A)
        expected = haf_complex(A)
        self.assertEqual(haf, expected)


if __name__ == '__main__':
    unittest.main()
