package Strategy;

import Serveur.FtpRequest;

public class RequestPORT implements Request{

	public void doRequest(FtpRequest ftp, String[] request){

		String[] split = request[1].split(",");
		if (split.length != 6) {
			ftp.sendMessage("501 Syntax error in parameters");
		} else {
			String hostname = split[0] + "." + split[1] + "." + split[2] + "." + split[3];
			int port = Integer.parseInt(split[4]) * 256 + Integer.parseInt(split[5]);
			ftp.getDataService().initActive(hostname, port);
			ftp.sendMessage("200 PORT command successfull");
		}
	}

}
