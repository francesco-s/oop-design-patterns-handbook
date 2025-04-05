class Computer:
    """Product class"""
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        components = []
        if self.cpu:
            components.append(f"CPU: {self.cpu}")
        if self.ram:
            components.append(f"RAM: {self.ram}GB")
        if self.storage:
            components.append(f"Storage: {self.storage}GB")
        if self.gpu:
            components.append(f"GPU: {self.gpu}")
        
        return "Computer with " + ", ".join(components)

class ComputerBuilder:
    """Builder interface"""
    def __init__(self):
        self.computer = Computer()
    
    def build_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def build_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def build_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def build_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def get_computer(self):
        return self.computer

class Director:
    """Director class that defines the order of building steps"""
    @staticmethod
    def build_gaming_pc(builder):
        return builder.build_cpu("Intel i9").build_ram(32).build_storage(1000).build_gpu("NVIDIA RTX 3080").get_computer()
    
    @staticmethod
    def build_office_pc(builder):
        return builder.build_cpu("Intel i5").build_ram(16).build_storage(512).get_computer()

if __name__ == "__main__":
    builder = ComputerBuilder()
    
    # Build using Director
    gaming_pc = Director.build_gaming_pc(builder)
    print(gaming_pc)
    
    # Reset builder and build another computer
    builder = ComputerBuilder()
    office_pc = Director.build_office_pc(builder)
    print(office_pc)
    
    # Custom build without Director
    custom_pc = ComputerBuilder().build_cpu("AMD Ryzen 7").build_ram(64).build_storage(2000).build_gpu("AMD Radeon").get_computer()
    print(custom_pc)