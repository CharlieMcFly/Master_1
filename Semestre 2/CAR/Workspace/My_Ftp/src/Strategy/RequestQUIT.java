package Strategy;

import java.io.IOException;

import Serveur.FtpRequest;

public class RequestQUIT implements Request{

	public void doRequest(FtpRequest ftp, String[] request) {
		
		ftp.getWriter().println(231 + " logout");
		try {
			ftp.getSocket().close();
			System.out.println(ftp.getClient() + " disconnected");
		} catch (IOException e) {
			e.printStackTrace();
		}		
	}



}
