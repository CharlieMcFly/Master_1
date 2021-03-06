package Stategy;

import static org.mockito.Mockito.mock;

import org.junit.Test;
import org.mockito.Mockito;

import Serveur.FtpRequest;
import Strategy.RequestUSER;

public class RequestUSERTest {

	@Test
	public void testUSERok() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"USER", "username"};
		RequestUSER r = new RequestUSER();
		Mockito.when(ftp.contientClientUsername("username")).thenReturn(true);
		
		r.doRequest(ftp, request);
		
		Mockito.verify(ftp).sendMessage(331 + " Username correct ");
	}

	@Test
	public void testUSERko() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"USER", "username"};
		RequestUSER r = new RequestUSER();
		Mockito.when(ftp.contientClientUsername("username")).thenReturn(false);
		
		r.doRequest(ftp, request);
		
		Mockito.verify(ftp).sendMessage(430 + " Username incorrect ");
	}

}
