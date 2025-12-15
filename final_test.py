# final_test.py - Этап 5 (тестовая задача)
import random
import yaml
import subprocess
import os

def create_vector_program():
    """Создает YAML-программу для обработки вектора длины 9"""
    program = []
    
    # 1. Создаем вектор из 9 случайных чисел
    vector = [random.randint(-10, 10) for _ in range(9)]
    
    # 2. Записываем вектор в память (адреса 0-8)
    for i, value in enumerate(vector):
        program.append({
            'command': 'load_const',
            'B': 1,
            'C': value
        })
        program.append({
            'command': 'write_mem',
            'B': 1,
            'C': 0,
            'D': i
        })
    
    # 3. Применяем abs к каждому элементу
    for i in range(9):
        program.append({
            'command': 'read_mem',
            'B': 0,
            'C': 2,
            'D': i
        })
        program.append({
            'command': 'abs',
            'B': 2,
            'C': 100 + i
        })
    
    return program, vector

def run_test():
    """Запускает полный тест"""
    print("=== ТЕСТОВАЯ ЗАДАЧА: abs() для вектора длины 9 ===")
    print()
    
    # Создаем программу
    program, vector = create_vector_program()
    
    # Сохраняем в YAML
    with open('vector_test.yaml', 'w') as f:
        yaml.dump(program, f, default_flow_style=False)
    
    print("1. Создан вектор:")
    print(f"   {vector}")
    
    print("\n2. Ожидаемый результат:")
    expected = [abs(x) for x in vector]
    print(f"   {expected}")
    
    print("\n3. Ассемблируем программу:")
    try:
        subprocess.run([sys.executable, 'assembler_s2.py', 'vector_test.yaml', 'vector.bin', '--test'], 
                      check=True)
    except:
        print("   Для ассемблирования выполните:")
        print("   python assembler_s2.py vector_test.yaml vector.bin --test")
    
    print("\n4. Выполняем программу:")
    try:
        subprocess.run([sys.executable, 'interpreter_s4.py', 'vector.bin', 'result.xml', '100', '108'],
                      check=True)
    except:
        print("   Для выполнения выполните:")
        print("   python interpreter_s4.py vector.bin result.xml 100 108")
    
    print("\n5. Дополнительные примеры:")
    print("   Пример 1: все положительные")
    vec1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"   Вектор: {vec1}")
    print(f"   Результат: {[abs(x) for x in vec1]}")
    
    print("\n   Пример 2: все отрицательные")
    vec2 = [-1, -2, -3, -4, -5, -6, -7, -8, -9]
    print(f"   Вектор: {vec2}")
    print(f"   Результат: {[abs(x) for x in vec2]}")
    
    print("\n   Пример 3: смешанный")
    vec3 = [-5, 3, -8, 0, 7, -2, 4, -9, 1]
    print(f"   Вектор: {vec3}")
    print(f"   Результат: {[abs(x) for x in vec3]}")

def main():
    run_test()

if __name__ == "__main__":
    main()