package Serveur;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

import Client.Client;
import Exceptions.FTPConnexionException;
import Exceptions.FTPDisconnexionException;
import Strategy.Request;

/**
 * Class lançant un thread pour la connection au ftp
 * 
 * @author charlie
 *
 */
public class FtpRequest extends Thread{
	
	private Socket socket;
	private BufferedReader reader;
	private PrintWriter writer;
	private List<Client> clients;
	private Client client;
	private DataService dataService; 
	private String ServerPath = "/";
	
	public void initClients(){
		clients = new ArrayList<Client>();
		Client c = new Client("Charlie", "123");
		c.setConnected(false);
		clients.add(c);
	}
	
	public FtpRequest(Socket socket) {
		this.initClients();
		this.socket = socket;
		this.dataService = new DataService(this);
		try {
			this.reader = new BufferedReader(new InputStreamReader(
					this.socket.getInputStream()));
			this.writer = new PrintWriter(new OutputStreamWriter(
					this.socket.getOutputStream()), true);
			this.sendMessage(220 + " Service ready, plz login");
			
		} catch (IOException e) {
			new FTPConnexionException();
		}
	}
	
	@Override
	public void run() {
		
		this.process();
		try {
			System.out.println("Closing connection");
			this.socket.close();
		} catch (IOException e) {
			throw new FTPDisconnexionException();
		}
	}
	
	/**
	 * Utilise la bonne strategie en fonction de la commande rentrée.
	 */
	public void process(){
		String line;
		try {
			while ((line = reader.readLine()) != null) {
				System.out.println(line);
				String request[] = line.split("\\s");
				Request r;
					/**
					 * Pattern Factory
					 * Recupère la class en fonction de ce qui est entrée par le client
					 */
					try {
						r = (Request) Class.forName("Strategy.Request"+request[0].toUpperCase()).newInstance();
						r.doRequest(this, request);
					} catch (ClassNotFoundException e) {
						this.sendMessage("Unknow Request");
					}
			}
		} catch (InstantiationException e) {
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/* Envoie un message */
	public void sendMessage(String message){
		this.getWriter().println(message);
	}
	
	/* SOCKET */
	public Socket getSocket() {
		return socket;
	}

	public void setSocket(Socket socket) {
		this.socket = socket;
	}
	
	/* SOCKET  DE DONNEES */
	public DataService getDataService() {
		return this.dataService;
	}

	public void setDataService(DataService dataService) {
		this.dataService = dataService;
	}

	/* READER */
	public BufferedReader getReader() {
		return reader;
	}

	public void setReader(BufferedReader reader) {
		this.reader = reader;
	}

	/* PRINTER */
	public PrintWriter getWriter() {
		return writer;
	}

	public void setWriter(PrintWriter writer) {
		this.writer = writer;
	}

	/* Client */
	public void setClient(Client clientConnecté) {
		this.client = clientConnecté;
	}

	public Client getClient() {
		return this.client;
	}
	
	/**
	 * Permet de vérifier si le client est dans la liste du serveur.
	 * 
	 * @param username
	 * @return true si l'username est dans la liste des clients
	 */
	public boolean contientClientUsername(String username) {
		for (Client u : this.clients) {
			if (u.isLogin(username))
				return true;
		}
		return false;
	}

	/**
	 * Retourne le client avec l'username passé en parametre
	 * 
	 * @param userName
	 * @return le client
	 */
	public Client getClientByUsername(String userName) {
		for (Client u : this.clients) {
			if (u.isLogin(userName))
				return u;
		}
		return null;
	}

	public List<Client> getClients() {
		return clients;
	}

	public void setClients(List<Client> clients) {
		this.clients = clients;
	}

	public String getServerPath() {
		return ServerPath;
	}

	public void setServerPath(String serverPath) {
		ServerPath = serverPath;
	}

}
