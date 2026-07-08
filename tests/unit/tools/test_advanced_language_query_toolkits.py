# tests/unit/tools/test_advanced_language_query_toolkits.py
import pytest
from codegraphcontext.tools.advanced_language_query_tool import Advanced_language_query

def test_all_16_toolkits_registered():
    expected_languages = {
        "c", "cpp", "go", "java", "javascript", "python", "ruby", "rust",
        "typescript", "c_sharp", "dart", "elisp", "perl", "scala", "swift", "haskell"
    }
    assert expected_languages.issubset(Advanced_language_query.TOOLKITS.keys())

@pytest.mark.parametrize("language", [
    "c", "cpp", "go", "java", "javascript", "python", "ruby", "rust",
    "typescript", "c_sharp", "dart", "elisp", "perl", "scala", "swift", "haskell"
])
def test_toolkit_instantiation_and_standard_queries(language):
    toolkit_class = Advanced_language_query.TOOLKITS[language]
    # Instantiate with no arguments
    toolkit = toolkit_class()

    # The 11 standard queries
    queries = [
        "Repository", "Directory", "File", "Module", "Function",
        "Class", "Struct", "Enum", "Union", "Macro", "Variable"
    ]

    for q in queries:
        try:
            cypher = toolkit.get_cypher_query(q)
            assert isinstance(cypher, str)
            assert len(cypher.strip()) > 0
        except ValueError as e:
            # Raising ValueError for unsupported types is acceptable for Elisp
            if language == "elisp" and q in ("Directory", "Struct", "Enum", "Union", "Macro"):
                continue
            raise e
