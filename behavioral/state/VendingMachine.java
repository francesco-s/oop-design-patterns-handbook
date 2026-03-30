// State interface
interface State {
    void insertCoin(VendingMachine machine);
    void pressButton(VendingMachine machine);
    void dispense(VendingMachine machine);
}


// Concrete States
class IdleState implements State {
    @Override
    public void insertCoin(VendingMachine machine) {
        System.out.println("Coin inserted");
        machine.setState(machine.hasCoinState);
    }

    @Override
    public void pressButton(VendingMachine machine) {
        System.out.println("Insert a coin first");
    }

    @Override
    public void dispense(VendingMachine machine) {
        System.out.println("Insert a coin first");
    }
}


class HasCoinState implements State {
    @Override
    public void insertCoin(VendingMachine machine) {
        System.out.println("Coin already inserted");
    }

    @Override
    public void pressButton(VendingMachine machine) {
        System.out.println("Button pressed");
        machine.setState(machine.dispensingState);
    }

    @Override
    public void dispense(VendingMachine machine) {
        System.out.println("Press the button first");
    }
}


class DispensingState implements State {
    @Override
    public void insertCoin(VendingMachine machine) {
        System.out.println("Please wait, dispensing in progress");
    }

    @Override
    public void pressButton(VendingMachine machine) {
        System.out.println("Already dispensing");
    }

    @Override
    public void dispense(VendingMachine machine) {
        if (machine.count > 0) {
            machine.count--;
            System.out.println("Item dispensed!");
        }
        if (machine.count == 0) {
            System.out.println("Out of stock!");
            machine.setState(machine.outOfStockState);
        } else {
            machine.setState(machine.idleState);
        }
    }
}


class OutOfStockState implements State {
    @Override
    public void insertCoin(VendingMachine machine) {
        System.out.println("Machine is out of stock");
    }

    @Override
    public void pressButton(VendingMachine machine) {
        System.out.println("Machine is out of stock");
    }

    @Override
    public void dispense(VendingMachine machine) {
        System.out.println("Machine is out of stock");
    }
}


// Context
public class VendingMachine {
    public final State idleState       = new IdleState();
    public final State hasCoinState    = new HasCoinState();
    public final State dispensingState = new DispensingState();
    public final State outOfStockState = new OutOfStockState();

    public int count;
    private State state;

    public VendingMachine(int count) {
        this.count = count;
        this.state = count > 0 ? idleState : outOfStockState;
    }

    public void setState(State state) { this.state = state; }

    public void insertCoin()  { state.insertCoin(this); }
    public void pressButton() { state.pressButton(this); }
    public void dispense()    { state.dispense(this); }

    public static void main(String[] args) {
        VendingMachine machine = new VendingMachine(2);

        System.out.println("-- Normal purchase --");
        machine.insertCoin();
        machine.pressButton();
        machine.dispense();

        System.out.println("\n-- Invalid actions --");
        machine.pressButton();
        machine.dispense();

        System.out.println("\n-- Last item --");
        machine.insertCoin();
        machine.pressButton();
        machine.dispense();

        System.out.println("\n-- Out of stock --");
        machine.insertCoin();
    }
}