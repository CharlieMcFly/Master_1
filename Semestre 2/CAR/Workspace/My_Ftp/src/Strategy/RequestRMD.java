package Strategy;

import java.io.File;

import Serveur.FtpRequest;

public class RequestRMD implements Request{

	public void doRequest(FtpRequest ftp, String[] request){

		File folder = new File(ftp.getClient().getPathname() + ftp.getServerPath() + request[1]);
		
		if (!folder.exists() || !folder.isDirectory()) {
			ftp.sendMessage("550 No such directory to delete");
		} else if (folder.delete()) {
			ftp.sendMessage("250 RMD command successfull");
		} else {
			ftp.sendMessage("550 Unable to delete directory");
		}
	}

}
