from functions.get_files_info import get_files_info

def run_case(wd, directory, label):
    print(label)
    result = get_files_info(wd, directory)
    if isinstance(result, str) and result.startswith("Error:"):
        print(f"    {result}")
    else:
        print(result)
    print()

def main():
    run_case("calculator", ".", "Result for current directory:")
    run_case("calculator", "pkg", "Result for 'pkg' directory:")
    run_case("calculator", "/bin", "Result for '/bin' directory:")
    run_case("calculator", "../", "Result for '../' directory:")

main()
