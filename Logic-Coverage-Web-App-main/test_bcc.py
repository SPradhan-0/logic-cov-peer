"""Base choice coverage tests derived from HW #1."""

import pytest

from logic_coverage import LogicCoverage


def assert_predicate_coverage_has_true_and_false(predicate):
    lc = LogicCoverage(predicate)
    pc = lc.predicate_coverage()

    assert pc["true"] is not None
    assert pc["false"] is not None
    assert lc._evaluate(pc["true"]) is True
    assert lc._evaluate(pc["false"]) is False
    return lc, pc


def test_t0_base_predicate_pc_succeeds_with_true_and_false_tests():
    lc, _ = assert_predicate_coverage_has_true_and_false("A && B")

    assert set(lc.clauses) == {"A", "B"}


def test_t1_not_and_parentheses_pc_succeeds_and_includes_c():
    lc, _ = assert_predicate_coverage_has_true_and_false("A && (B || !C)")

    assert set(lc.clauses) == {"A", "B", "C"}


def test_t2_malformed_predicate_raises_value_error():
    with pytest.raises(ValueError):
        LogicCoverage("A &&& B")


def test_t3_empty_predicate_raises_value_error():
    with pytest.raises(ValueError):
        LogicCoverage("")


def test_t4_single_clause_pc_returns_false_and_true_assignments():
    lc = LogicCoverage("A")
    pc = lc.predicate_coverage()

    assert pc["false"] == {"A": False}
    assert pc["true"] == {"A": True}


def test_t5_multi_letter_clause_names_are_accepted():
    lc = LogicCoverage("flag1 && cond2")

    assert set(lc.clauses) == {"flag1", "cond2"}


def test_t6_compact_spacing_behaves_like_base_predicate():
    compact = LogicCoverage("A&&B")
    base = LogicCoverage("A && B")

    assert compact.clauses == base.clauses
    assert compact.generate_truth_table() == base.generate_truth_table()


def test_t7_large_predicate_combinatorial_coverage_has_256_assignments():
    predicate = "A && B && C && D && E && F && G && H"
    lc = LogicCoverage(predicate)

    assert len(lc.clauses) == 8
    assert len(lc.combinatorial_coverage()) == 2**8


def test_t8_clause_coverage_covers_each_base_clause_true_and_false():
    lc = LogicCoverage("A && B")
    cc = lc.clause_coverage()

    for clause in ("A", "B"):
        assert cc[clause]["true"] is not None
        assert cc[clause]["false"] is not None
        assert cc[clause]["true"][clause] is True
        assert cc[clause]["false"][clause] is False
