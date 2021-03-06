package Client;

/**
 * Class client contenant le client qui se connecte au ftp
 * login / password / connected / pathname / alea
 * 	
 * 
 * @author charlie
 *
 */
public class Client {

	private String login;
	private String password;
	private boolean connected = false;
	private String pathname;
	private int alea;

	/**
	 * 
	 * Constructeur, prenant un login et un mot de passe
	 * 
	 * @param login
	 * @param pass
	 */
	public Client(String login, String pass){
		this.login=login;
		this.password=pass;
		// REMARQUE ~ ne marche pas ?
		this.pathname = "/home/charlie/CAR_TP1/"+this.login;
		// Utile pour le ftp Passif
		this.alea = login.length() + password.length() * 2;
	}

	// Getter et Setter
	
	public String getLogin() {
		return login;
	}

	public void setLogin(String login) {
		this.login = login;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}
	
	public boolean isConnected() {
		return connected;
	}

	public void setConnected(boolean connected) {
		this.connected = connected;
	}

	public String getPathname() {
		return pathname;
	}

	public void setPathname(String pathname) {
		this.pathname = pathname;
	}

	public int getAlea() {
		return alea;
	}

	public void setAlea(int alea) {
		this.alea = alea;
	}
	
	/**
	 * Vérification du login
	 */
	public boolean isLogin(String login){
		return this.login.equals(login);
	}
	
	/**
	 * Vérification du password
	 */	
	public boolean isPassword(String pass){
		if(this.password.equals(pass)){
			this.setConnected(true);
			return true;
		}else{
			this.setConnected(false);
			return false;
		}
	}
	
}
