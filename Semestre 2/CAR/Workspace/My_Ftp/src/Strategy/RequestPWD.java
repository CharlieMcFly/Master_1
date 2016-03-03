package Strategy;

import Serveur.FtpRequest;

public class RequestPWD implements Request{

	public void doRequest(FtpRequest ftp, String[] request) {
		ftp.sendMessage("257 "+ "\"" + ftp.getServerPath() + "\"" + " is the current directory.");		
	}


}
