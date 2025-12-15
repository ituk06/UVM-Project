import yaml
import sys

def parse_yaml_to_intermediate(yaml_file):
    """Этап 1: Чтение YAML и создание промежуточного представления"""
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    intermediate = []
    for cmd in data:
        entry = {}
        
        if cmd['command'] == 'load_const':
            entry['A'] = 29
            entry['B'] = cmd['B']
            entry['C'] = cmd['C']
        elif cmd['command'] == 'read_mem':
            entry['A'] = 21
            entry['B'] = cmd['B']
            entry['C'] = cmd['C']
            entry['D'] = cmd['D']
        elif cmd['command'] == 'write_mem':
            entry['A'] = 16
            entry['B'] = cmd['B']
            entry['C'] = cmd['C']
            entry['D'] = cmd['D']
        elif cmd['command'] == 'abs':
            entry['A'] = 5
            entry['B'] = cmd['B']
            entry['C'] = cmd['C']
        
        intermediate.append(entry)
    
    return intermediate

def main():
    if len(sys.argv) < 3:
        print("Использование: python assembler_s1.py input.yaml output.txt [--test]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = len(sys.argv) > 3 and sys.argv[3] == '--test'
    
    intermediate = parse_yaml_to_intermediate(input_file)
    
    # Сохраняем промежуточное представление
    with open(output_file, 'w') as f:
        for i, cmd in enumerate(intermediate):
            f.write(f"Команда {i}: ")
            for key, value in cmd.items():
                f.write(f"{key}={value} ")
            f.write("\n")
    
    print(f"Создано промежуточное представление: {len(intermediate)} команд")
    
    if test_mode:
        print("\n=== Промежуточное представление ===")
        for i, cmd in enumerate(intermediate):
            print(f"Команда {i}: ", end="")
            for key, value in cmd.items():
                print(f"{key}={value} ", end="")
            print()

if __name__ == "__main__":
    main()