from functions.get_file_content import get_file_content, MAX_CHARS


def test_lorem_truncation():
    working_dir = "calculator"
    file_name = "lorem.txt"

    result = get_file_content(working_dir, file_name)

    assert isinstance(result, str)

    expected_suffix = f'[...File "{file_name}" truncated at {MAX_CHARS} characters]'
    assert result.endswith(expected_suffix), "Truncation message missing or incorrect"

    content_only = result[:-len(expected_suffix)]
    assert len(content_only) == MAX_CHARS, "File content not truncated to MAX_CHARS"


def manual_output_tests():
    print("\n--- Manual Output Tests ---")

    print("\nmain.py:")
    print(get_file_content("calculator", "main.py"))

    print("\npkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\nAttempt to read /bin/cat (should error):")
    print(get_file_content("calculator", "/bin/cat"))

    print("\nNon-existent file (should error):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    test_lorem_truncation()
    print("Truncation test passed.")
    manual_output_tests()
