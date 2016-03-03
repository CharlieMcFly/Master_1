package Stategy;

import static org.mockito.Mockito.mock;

import org.junit.Test;
import org.mockito.Mockito;

import Serveur.FtpRequest;
import Strategy.RequestTYPE;

public class RequestTYPETest {

	@Test
	public void test() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"TYPE"};
		RequestTYPE r = new RequestTYPE();
		
		r.doRequest(ftp, request);
		
		Mockito.verify(ftp).sendMessage("200 action successfull");	}

}
