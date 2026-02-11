from functions.write_file import write_file


def test_writing():
    working_dir = "calculator"
    file_path = "lorem.txt"
    content = "wait, this isn't lorem ipsum"

    result = write_file(working_dir, file_path, content)

    assert isinstance(result, str)
    assert result == f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



def manual_output_tests():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    test_writing()
    print("Writing test passed.")
    manual_output_tests()
