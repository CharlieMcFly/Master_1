package Strategy;

import Serveur.FtpRequest;

public class RequestUSER implements Request{

	public void doRequest(FtpRequest ftp, String [] request){
		
		if(ftp.contientClientUsername(request[1])){
			ftp.sendMessage(331 + " Username correct ");
			ftp.setClient(ftp.getClientByUsername(request[1]));
		}else{
			ftp.sendMessage(430 + " Username incorrect ");
		}
	}

}
