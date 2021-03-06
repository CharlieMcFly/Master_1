package Stategy;

import static org.mockito.Mockito.mock;

import org.junit.Test;
import org.mockito.Mockito;

import Client.Client;
import Serveur.FtpRequest;
import Strategy.Request;
import Strategy.RequestPASS;

public class RequestPASSTest {

	@Test
	public void testPASSok() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"PASS", "123"};
		Client c = mock(Client.class);
		
		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(c.isPassword("123")).thenReturn(true);

		RequestPASS pass = new RequestPASS();

		pass.doRequest(ftp, request);

		Mockito.verify(ftp).sendMessage(230 + " Password correct");
	}
	
	@Test
	public void testPASSko() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"PASS", "123"};
		Client c = mock(Client.class);
		
		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(c.isPassword("111")).thenReturn(false);

		RequestPASS pass = new RequestPASS();

		pass.doRequest(ftp, request);

		Mockito.verify(ftp).sendMessage(430 + " Invalid Password");
	}

}
