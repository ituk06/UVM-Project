import yaml
import struct
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

def intermediate_to_binary(intermediate):
    """Этап 2: Преобразование в бинарный код"""
    binary = bytearray()
    
    for cmd in intermediate:
        opcode = cmd['A']
        
        if opcode == 29:  # load_const
            b = cmd['B']
            c = cmd['C']
            word = (opcode & 0x1F) | ((b & 0x7) << 5) | ((c & 0x7FFFFF) << 8)
            binary.extend(struct.pack('<I', word))
        
        elif opcode in [21, 16]:  # read_mem или write_mem
            b = cmd['B']
            c = cmd['C']
            d = cmd['D']
            word = (opcode & 0x1F) | ((b & 0x7) << 5) | ((c & 0x7) << 8) | ((d & 0x3FFF) << 11)
            binary.extend(struct.pack('<I', word))
        
        elif opcode == 5:  # abs
            b = cmd['B']
            c = cmd['C']
            word = (opcode & 0x1F) | ((b & 0x7) << 5) | ((c & 0x3FFFFFF) << 8)
            binary.extend(struct.pack('<I', word))
    
    return binary

def main():
    if len(sys.argv) < 3:
        print("Использование: python assembler_s2.py input.yaml output.bin [--test]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = len(sys.argv) > 3 and sys.argv[3] == '--test'
    
    # Этап 1
    intermediate = parse_yaml_to_intermediate(input_file)
    
    if test_mode:
        print("=== Этап 1: Промежуточное представление ===")
        for i, cmd in enumerate(intermediate):
            print(f"Команда {i}: ", end="")
            for key, value in cmd.items():
                print(f"{key}={value} ", end="")
            print()
    
    # Этап 2
    binary_data = intermediate_to_binary(intermediate)
    
    with open(output_file, 'wb') as f:
        f.write(binary_data)
    
    print(f"\n=== Этап 2: Генерация кода ===")
    print(f"Создан файл: {output_file}")
    print(f"Размер: {len(binary_data)} байт")
    print(f"Команд: {len(intermediate)}")
    
    if test_mode:
        print("\nБайтовое представление:")
        for i in range(0, len(binary_data), 5):
            chunk = binary_data[i:i+5]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            print(f"  Команда {i//5}: {hex_str}")

if __name__ == "__main__":
    main()