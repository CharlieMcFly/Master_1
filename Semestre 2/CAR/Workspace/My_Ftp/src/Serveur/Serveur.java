package Serveur;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Le serveur 
 * @author charlie
 *
 */
public class Serveur extends Thread {

	private static Socket socket; 
	private static ServerSocket serverSocket;
	
	/**
	 * Fait écouter le serveur sur le port 1666
	 */
	public void initServeur(){
		try {
//			Ouvre le socket sur le port 1666 et accept une connection
			serverSocket = new ServerSocket(1666);
			System.out.println("Initialisation du serveur : OK !");
		} catch (IOException e) {
			System.out.println("Erreur lors de l'initialisation du serveur");
		}
	}
	
	/**
	 * Attend la connection de clients.
	 * Lors de la connection, on lance un nouveau thread FTPRequest
	 */
	public void run(){
		while(true){
			System.out.println("En attente de client ...");
			try {
				// Accepte le client
				this.socket = this.serverSocket.accept();
				new Thread(new FtpRequest(this.socket)).start();
			} catch (IOException e) {
				System.out.println("Erreur lors du lancement du serveur");
			}
		}
	}


}
