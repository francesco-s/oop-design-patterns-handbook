// SupportHandler.java


// Handler abstract class (holds next reference and chaining logic)
public abstract class SupportHandler {
    private SupportHandler next;

    public SupportHandler setNext(SupportHandler handler) {
        this.next = handler;
        return handler;  // allows chaining: a.setNext(b).setNext(c)
    }

    public abstract void handle(int level, String issue);

    protected void passToNext(int level, String issue) {
        if (next != null) {
            next.handle(level, issue);
        } else {
            System.out.println("Issue '" + issue + "' could not be resolved");
        }
    }

    public static void main(String[] args) {
        SupportHandler basic        = new BasicSupport();
        SupportHandler intermediate = new IntermediateSupport();
        SupportHandler advanced     = new AdvancedSupport();

        // Build the chain: basic → intermediate → advanced
        basic.setNext(intermediate).setNext(advanced);

        System.out.println("-- Ticket 1 (level 1) --");
        basic.handle(1, "Password reset");

        System.out.println("\n-- Ticket 2 (level 2) --");
        basic.handle(2, "Software installation failure");

        System.out.println("\n-- Ticket 3 (level 3) --");
        basic.handle(3, "Critical database corruption");

        System.out.println("\n-- Ticket 4 (level 4 - unhandled) --");
        basic.handle(4, "Unknown hardware malfunction");
    }
}


// Concrete Handlers
class BasicSupport extends SupportHandler {
    @Override
    public void handle(int level, String issue) {
        if (level == 1) {
            System.out.println("[Basic Support]        Resolved: '" + issue + "'");
        } else {
            System.out.println("[Basic Support]        Escalating: '" + issue + "'");
            passToNext(level, issue);
        }
    }
}


class IntermediateSupport extends SupportHandler {
    @Override
    public void handle(int level, String issue) {
        if (level == 2) {
            System.out.println("[Intermediate Support] Resolved: '" + issue + "'");
        } else {
            System.out.println("[Intermediate Support] Escalating: '" + issue + "'");
            passToNext(level, issue);
        }
    }
}


class AdvancedSupport extends SupportHandler {
    @Override
    public void handle(int level, String issue) {
        if (level == 3) {
            System.out.println("[Advanced Support]     Resolved: '" + issue + "'");
        } else {
            System.out.println("[Advanced Support]     Escalating: '" + issue + "'");
            passToNext(level, issue);
        }
    }
}