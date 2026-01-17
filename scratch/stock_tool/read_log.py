try:
    with open('screening_results.txt', 'r', encoding='utf-16') as f:
        print(f.read())
except UnicodeError:
    try:
        with open('screening_results.txt', 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")
except Exception as e:
    print(f"Error reading file: {e}")
