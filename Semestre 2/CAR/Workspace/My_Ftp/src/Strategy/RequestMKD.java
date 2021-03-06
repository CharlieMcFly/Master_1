package Strategy;

import java.io.File;

import Serveur.FtpRequest;

public class RequestMKD implements Request{

	public void doRequest(FtpRequest ftp, String[] request) {
	
		File folder = new File(ftp.getClient().getPathname() + request[1]);

		if (folder.exists()) {
			ftp.sendMessage("553 Directory already exists");
		} else if (folder.mkdirs()) {
			ftp.sendMessage("257 MKD command successfull");
		} else {
			ftp.sendMessage("550 Unable to make directory");
		}
	}

}
