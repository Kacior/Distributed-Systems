import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;
import java.nio.*;
import java.util.*;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9008;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while(true) {
                Arrays.fill(receiveBuffer, (byte)0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
                int nb = ByteBuffer.wrap(receivePacket.getData()).getInt();
                System.out.println("received msg: " + nb);
                nb+=1;


                InetAddress address = InetAddress.getByName("localhost");
                byte[] sendBuffer = ByteBuffer.allocate(4).putInt(nb).array();
                DatagramPacket replyPacket = new DatagramPacket(sendBuffer, sendBuffer.length, address, receivePacket.getPort());
                socket.send(replyPacket);
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}
