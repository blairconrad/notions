#!/usr/bin/env python

import cvs_history


class TestSort:
    def test_sortWithNumericsEmpty(self):
        a = []
        cvs_history.sortWithNumerics(a)
        assert [] == a

    def test_sortWithNumericsNoNumerics(self):
        input = ["hippo", "a", "zebra"]
        cvs_history.sortWithNumerics(input)
        assert ["a", "hippo", "zebra"] == input

    def test_sortWithNumericsOnlyNumbers(self):
        input = ["134", "0", "19"]
        cvs_history.sortWithNumerics(input)
        assert ["0", "19", "134"] == input

    def test_sortWithNumericsInitialNumbers(self):
        input = ["134", "0b", "19a"]
        cvs_history.sortWithNumerics(input)
        assert ["0b", "19a", "134"] == input

    def test_sortWithNumericsFinalNumbers(self):
        input = ["a134", "c217", "c23", "b0", "c19", "c0"]
        cvs_history.sortWithNumerics(input)
        assert ["a134", "b0", "c0", "c19", "c23", "c217"] == input

    def test_sortWithNumericsEmbeddedNumbers(self):
        input = ["a134z", "c217", "c23", "a134b", "b0", "c19z", "c0"]
        cvs_history.sortWithNumerics(input)
        assert ["a134b", "a134z", "b0", "c0", "c19z", "c23", "c217"] == input

    def test_sortWithNumericsShorterStringSortsFirst(self):
        input = ["1.170", "1.170.0.2"]
        cvs_history.sortWithNumerics(input)
        assert ["1.170", "1.170.0.2"] == input


class TestSplitOffEndingNumbers:
    def test_splitOffEndingNumbersEmpty(self):
        assert ("", "") == cvs_history.splitOffEndingNumbers("")

    def test_splitOffEndingNumbersNoNumbers(self):
        assert ("abc", "") == cvs_history.splitOffEndingNumbers("abc")

    def test_splitOffEndingNumbersOneNumber(self):
        assert ("abc", "3") == cvs_history.splitOffEndingNumbers("abc3")

    def test_splitOffEndingNumbersAllNumbers(self):
        assert ("", "153") == cvs_history.splitOffEndingNumbers("153")

    def test_splitOffEndingNumbersSomeNumbers(self):
        assert ("abdfa", "153") == cvs_history.splitOffEndingNumbers("abdfa153")
