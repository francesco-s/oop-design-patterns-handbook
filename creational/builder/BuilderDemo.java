package creational.builder;

import java.util.ArrayList;
import java.util.List;

// Product
class Computer {
    private String cpu;
    private int ram;
    private int storage;
    private String gpu;
    
    public void setCpu(String cpu) {
        this.cpu = cpu;
    }
    
    public void setRam(int ram) {
        this.ram = ram;
    }
    
    public void setStorage(int storage) {
        this.storage = storage;
    }
    
    public void setGpu(String gpu) {
        this.gpu = gpu;
    }
    
    @Override
    public String toString() {
        List<String> components = new ArrayList<>();
        if (cpu != null) {
            components.add("CPU: " + cpu);
        }
        if (ram > 0) {
            components.add("RAM: " + ram + "GB");
        }
        if (storage > 0) {
            components.add("Storage: " + storage + "GB");
        }
        if (gpu != null) {
            components.add("GPU: " + gpu);
        }
        
        return "Computer with " + String.join(", ", components);
    }
}

// Builder interface
interface Builder {
    Builder buildCpu(String cpu);
    Builder buildRam(int ram);
    Builder buildStorage(int storage);
    Builder buildGpu(String gpu);
    Computer getComputer();
}

// ConcreteBuilder
class ComputerBuilder implements Builder {
    private Computer computer;
    
    public ComputerBuilder() {
        this.computer = new Computer();
    }
    
    @Override
    public Builder buildCpu(String cpu) {
        computer.setCpu(cpu);
        return this;
    }
    
    @Override
    public Builder buildRam(int ram) {
        computer.setRam(ram);
        return this;
    }
    
    @Override
    public Builder buildStorage(int storage) {
        computer.setStorage(storage);
        return this;
    }
    
    @Override
    public Builder buildGpu(String gpu) {
        computer.setGpu(gpu);
        return this;
    }
    
    @Override
    public Computer getComputer() {
        return computer;
    }
}

// Director
class Director {
    public static Computer buildGamingPC(Builder builder) {
        return builder
            .buildCpu("Intel i9")
            .buildRam(32)
            .buildStorage(1000)
            .buildGpu("NVIDIA RTX 3080")
            .getComputer();
    }
    
    public static Computer buildOfficePC(Builder builder) {
        return builder
            .buildCpu("Intel i5")
            .buildRam(16)
            .buildStorage(512)
            .getComputer();
    }
}

public class BuilderDemo {
    public static void main(String[] args) {
        Builder builder = new ComputerBuilder();
        
        // Build using Director
        Computer gamingPC = Director.buildGamingPC(builder);
        System.out.println(gamingPC);
        
        // Reset builder and build another computer
        builder = new ComputerBuilder();
        Computer officePC = Director.buildOfficePC(builder);
        System.out.println(officePC);
        
        // Custom build without Director
        Computer customPC = new ComputerBuilder()
            .buildCpu("AMD Ryzen 7")
            .buildRam(64)
            .buildStorage(2000)
            .buildGpu("AMD Radeon")
            .getComputer();
        System.out.println(customPC);
    }
}