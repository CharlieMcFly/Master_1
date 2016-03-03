package Strategy;

import Serveur.FtpRequest;

public class RequestSYST implements Request {

	public void doRequest(FtpRequest ftp, String[] request) {
		ftp.sendMessage("200 action successfull");
	}

}
