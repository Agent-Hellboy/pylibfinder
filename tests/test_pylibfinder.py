import pylibfinder
import pytest


@pytest.fixture
def query():
    return "power"


def test_find_similar_basic(query):
    """Test basic semantic similarity search."""
    result = pylibfinder.find_similar(query)

    # Assert that the result is a list
    assert isinstance(result, list)

    # Assert that we found at least one match
    assert len(result) > 0

    # Assert that each item in the list is a dictionary
    for item in result:
        assert isinstance(item, dict)

        # Assert that each dictionary contains required keys
        assert "Module" in item
        assert "Object Name" in item
        assert "Score" in item

        # Assert that the values are of correct types
        assert isinstance(item["Module"], str)
        assert isinstance(item["Object Name"], str)
        assert isinstance(item["Score"], float)

        # Assert that similarity score is valid (0.0 to 1.0)
        assert 0.0 <= item["Score"] <= 1.0


def test_find_similar_with_threshold():
    """Test semantic similarity with custom threshold."""
    result = pylibfinder.find_similar("print", 0.9)

    # Assert that the result is a list
    assert isinstance(result, list)

    # Assert that all results meet the threshold
    for item in result:
        assert item["Score"] >= 0.9


def test_find_similar_exact_match():
    """Test exact match returns high similarity."""
    result = pylibfinder.find_similar("print", 0.5)

    # Find the exact match in results
    exact_match = None
    for item in result:
        if item["Object Name"] == "print" and item["Module"] == "builtins":
            exact_match = item
            break

    # Assert that exact match was found
    assert exact_match is not None

    # Assert that exact match has perfect or near-perfect score
    assert exact_match["Score"] >= 0.99


def test_find_similar_substring_match():
    """Test that substring matches get boosted similarity."""
    result = pylibfinder.find_similar("print_function", 0.5)

    # Assert that we found results
    assert len(result) > 0

    # Assert that print_function substring provides matches
    found_print_related = False
    for item in result:
        if "print" in item["Object Name"].lower():
            found_print_related = True
            break

    assert found_print_related


def test_find_similar_excludes_private_by_default():
    """Test that private functions (starting with _) are excluded by default."""
    result = pylibfinder.find_similar("parse", 0.5)

    # Assert that all results are public functions (don't start with _)
    for item in result:
        assert not item["Object Name"].startswith("_")


def test_find_similar_includes_private_when_flag_set():
    """Test that private functions are included when include_private=True."""
    result_without_private = pylibfinder.find_similar("parse", 0.5, include_private=False)
    result_with_private = pylibfinder.find_similar("parse", 0.5, include_private=True)

    # Assert that include_private=True returns more or equal results
    assert len(result_with_private) >= len(result_without_private)

    # If there are more results, at least some should be private
    if len(result_with_private) > len(result_without_private):
        has_private = any(item["Object Name"].startswith("_") for item in result_with_private)
        assert has_private
