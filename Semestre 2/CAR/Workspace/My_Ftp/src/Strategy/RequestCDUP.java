package Strategy;

import java.io.File;

import Serveur.FtpRequest;

public class RequestCDUP implements Request{

	public void doRequest(FtpRequest ftp, String[] request){
		

		String parent = new File(ftp.getServerPath()).getParent();
		if (parent != null) {
			ftp.setServerPath(parent);
			ftp.sendMessage("200 CDUP successfull");
		}
		else {
			ftp.sendMessage("550 No access to parent folder");
		}
	}



}
