import struct
import xml.etree.ElementTree as ET
import sys

class UVM:
    def __init__(self):
        self.memory = [0] * 1000  # Память данных
        self.registers = [0] * 8   # 8 регистров
    
    def load_program(self, filename):
        """Загружает бинарную программу в память"""
        with open(filename, 'rb') as f:
            data = f.read()
        
        for i in range(0, len(data), 4):
            if i + 4 <= len(data):
                chunk = data[i:i+4]
                word = int.from_bytes(chunk, 'little')
                self.memory[i//4] = word
    
    def run(self):
        """Выполняет программу"""
        pc = 0  # Program Counter
        
        while pc < len(self.memory):
            word = self.memory[pc]
            if word == 0:
                break
            
            opcode = word & 0x1F
            
            if opcode == 29:  # load_const
                b = (word >> 5) & 0x7
                const = (word >> 8) & 0x7FFFFF
                if const & 0x400000:
                    const -= 0x800000
                self.registers[b] = const
            
            elif opcode == 21:  # read_mem
                b = (word >> 5) & 0x7
                c = (word >> 8) & 0x7
                d = (word >> 11) & 0x3FFF
                addr = self.registers[b] + d
                self.registers[c] = self.memory[addr]
            
            elif opcode == 16:  # write_mem
                b = (word >> 5) & 0x7
                c = (word >> 8) & 0x7
                d = (word >> 11) & 0x3FFF
                addr = self.registers[c] + d
                self.memory[addr] = self.registers[b]
            
            elif opcode == 5:  # abs - ЭТАП 4
                b = (word >> 5) & 0x7
                c = (word >> 8) & 0x3FFFFFF
                value = self.registers[b]
                self.memory[c] = abs(value)  # Абсолютное значение
            
            pc += 1
    
    def save_dump(self, filename, start, end):
        """Сохраняет дамп памяти в XML"""
        root = ET.Element("memory")
        
        for addr in range(start, min(end + 1, len(self.memory))):
            elem = ET.SubElement(root, "cell")
            elem.set("address", str(addr))
            elem.set("value", str(self.memory[addr]))
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

def main():
    if len(sys.argv) != 5:
        print("Использование: python interpreter.py program.bin dump.xml start end")
        print("Пример: python interpreter.py output.bin dump.xml 0 100")
        return
    
    program_file = sys.argv[1]
    dump_file = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    
    uvm = UVM()
    uvm.load_program(program_file)
    uvm.run()
    uvm.save_dump(dump_file, start, end)
    
    print(f"Программа выполнена")
    print(f"Дамп памяти {start}-{end} сохранен в {dump_file}")

if __name__ == "__main__":
    main()