import pytest


def calculate_dependency(
    supplier_relationships,
    total_relationships,
):
    """
    Test version of the supplier dependency formula.
    """

    if total_relationships == 0:
        return 0.0

    return (
        supplier_relationships
        / total_relationships
    )


def test_supplier_dependency():
    result = calculate_dependency(
        supplier_relationships=5,
        total_relationships=10,
    )

    assert result == 0.5


def test_zero_relationships():
    result = calculate_dependency(
        supplier_relationships=0,
        total_relationships=0,
    )

    assert result == 0.0


def test_full_supplier_dependency():
    result = calculate_dependency(
        supplier_relationships=10,
        total_relationships=10,
    )

    assert result == 1.0


def test_low_supplier_dependency():
    result = calculate_dependency(
        supplier_relationships=2,
        total_relationships=20,
    )

    assert result == 0.1


def test_dependency_range():
    result = calculate_dependency(
        supplier_relationships=7,
        total_relationships=10,
    )

    assert 0.0 <= result <= 1.0