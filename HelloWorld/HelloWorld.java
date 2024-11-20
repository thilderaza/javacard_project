package HelloWorld;

import javacard.framework.*;

public class HelloWorld extends Applet {
    public HelloWorld() {
    }

    public static void install(APDU apdu) {
        new HelloWorld().register();
    }

    public void process(APDU apdu) throws ISOException {
        if (selectingApplet()) {
            return;
        }
        byte[] buffer = apdu.getBuffer();
        buffer[0] = (byte) 0x90; // Response status 9000 (OK)
        apdu.setOutgoingAndSend((short) 0, (short) 1);
    }
}
