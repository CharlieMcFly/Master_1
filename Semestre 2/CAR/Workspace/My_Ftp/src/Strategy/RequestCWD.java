package Strategy;

import java.io.File;

import Serveur.FtpRequest;

public class RequestCWD implements Request{

	public void doRequest(FtpRequest ftp, String[] request){

		String arg = request[1];
		String path = "/";

		if (arg.isEmpty()) {
			ftp.sendMessage("501 Syntax error in parameters");
			return;
		}
		if (arg.contains("..")) {
			ftp.sendMessage("550 No access to parent folder");
			return;
		}
		// Root path
		else if (arg.equals("/")) {
			path = "/";
		}
		// Absolute path
		else if (arg.startsWith("/")) {
			path = arg + "/";
		}
		// Relative path
		else {
			path = ftp.getServerPath() + arg + "/";
		}

		// Check and set path
		File dir = new File(ftp.getClient().getPathname(), path);
		if (dir.isFile()) {
			ftp.sendMessage("550 Cannot go into a file (CWD on file)");
		} else if (!dir.exists()) {
			ftp.sendMessage("550 No such directory");
		} else {
			ftp.setServerPath(path);
			ftp.sendMessage("250 CWD command successfull");
		}
	}



}
