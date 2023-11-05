import re

# C++ 소스 코드를 읽어오는 함수
def read_cpp_file(file_path):
    with open(file_path, 'r') as file:
        cpp_code = file.read()
    return cpp_code

# C++ 소스 코드에서 메소드(함수)의 종류와 수를 세는 함수
def count_cpp_methods(cpp_code):
    # C++ 메소드 정의 패턴: 반환형 함수이름(매개변수)
    method_pattern = r'\b\w+\s+\w+\s*\(.*?\)\s*{'
    methods = re.findall(method_pattern, cpp_code, re.DOTALL)
    method_names = [method.split()[1] for method in methods]
    method_count = len(methods)
    unique_method_count = len(set(method_names))
    return unique_method_count, method_count

# C++ 소스 코드 파일 경로
cpp_file_path = 'hello.cpp'  # 실제 파일 경로로 변경해주세요

# C++ 소스 코드를 읽어오기
cpp_code = read_cpp_file(cpp_file_path)

# 메소드의 종류와 수 세기
unique_method_count, total_method_count = count_cpp_methods(cpp_code)

# 결과 출력
print(f'총 {total_method_count}개의 메소드가 정의되어 있습니다.')
print(f'유니크한 메소드의 수: {unique_method_count}')