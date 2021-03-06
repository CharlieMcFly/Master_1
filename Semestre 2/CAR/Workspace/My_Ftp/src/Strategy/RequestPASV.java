package Strategy;

import Serveur.FtpRequest;

public class RequestPASV implements Request{

	public void doRequest(FtpRequest ftp, String[] request) {
		
		final int port = 1234 + ftp.getClient().getAlea();
		ftp.getDataService().initPassive(port);
		ftp.sendMessage("227 Entering passive mode " + ftp.getSocket().getInetAddress().getHostName().replaceAll("\\.", ",") + ","
				+ port / 256 + "," + port % 256);
	}

}
