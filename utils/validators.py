# utils/validators.py

def validate_rule(rule):
    # contoh validasi sederhana
    if "IF" not in rule or "THEN" not in rule:
        raise ValueError("Rule harus memiliki IF dan THEN")
    return True

def validate_input(input_data):
    # contoh validasi input gejala
    if not isinstance(input_data, list):
        raise ValueError("Input harus berupa list gejala")
    return True
