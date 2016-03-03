package Strategy;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

import Serveur.FtpRequest;

public class RequestSTOR implements Request {

	public void doRequest(FtpRequest ftp, String[] request){
		FileOutputStream fos = null;
		InputStream is = null;
		try {
			fos = new FileOutputStream(ftp.getClient().getPathname()+"/"+ request[1]);
			ftp.sendMessage("150 File status okay; about to open data connection");
			is = ftp.getDataService().openDataStream().getInputStream();
			
			byte[] buffer = new byte[1024];
			int nbBytes = 0;
			while ((nbBytes = is.read(buffer)) != -1) {
				fos.write(buffer, 0, nbBytes);
			}

			ftp.sendMessage("226 Closing data connection");
			ftp.getDataService().closeDataStream();
		} catch (FileNotFoundException e) {
			ftp.sendMessage("550 Requested action not taken; file unavailable");
		} catch (IOException ignore) {
			ftp.sendMessage("426 Closing data connection");
			ftp.getDataService().closeDataStream();
		} finally {
			try { fos.close(); } catch(Exception ignore) {};
			try { is.close(); } catch(Exception ignore) {};
		}
		
	}

	

}
