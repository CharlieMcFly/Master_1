package Serveur;

import java.io.IOException;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;

import Exceptions.FTPConnexionException;

/**
 * 
 * @author charlie
 *
 *	Sert pour la création des sockets pour les données
 */
public class DataService {

	/* Pour le transfert de données */
	private ServerSocket dataServSocket;
	private Socket dataSocket;
	private int port;
	private OutputStream dataStream;
	private FtpRequest ftp;
	private boolean isPassive =false; 
	
	public DataService(FtpRequest ftp){
		this.ftp = ftp;
	}
	
	/*
	 * Ouvre un socket pour les données
	 */
	public Socket openDataStream() {
		if (this.isPassive) {
			try {
				this.dataSocket = this.dataServSocket.accept();
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				try {
					this.dataServSocket.close();
				} catch (IOException ignore) {
				}
			}
		}
		return this.dataSocket;
		
	}

	/*
	 * Ferme le socket des données
	 */
	public void closeDataStream() {
		
		try {
			this.dataServSocket.close();
			this.dataSocket.close();
		} catch (final IOException e) {
		}
		this.dataSocket = null;
		this.dataServSocket = null;
	}

	public void initActive(String hostname, int port){
		this.isPassive = false;
		this.port = port;
		// Ouverture canal de données
		try {
			this.dataSocket = new Socket(hostname, port);
		} catch (UnknownHostException e) {
			throw new FTPConnexionException();
		} catch (IOException e) {
			throw new FTPConnexionException();
		}
	
	}
	
	public void initPassive(int port){
		this.isPassive = true;
		try {
			this.dataServSocket = new ServerSocket(port);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public int getPort() {
		return port;
	}

	public void setPort(int port) {
		this.port = port;
	}

	public Socket getDataSocket() {
		return dataSocket;
	}

	public OutputStream getDataStream() {
		return dataStream;
	}

	public FtpRequest getFtp() {
		return ftp;
	}

	
}

