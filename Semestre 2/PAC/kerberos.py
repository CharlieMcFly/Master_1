def connection_kerberos(self, ticket):
          # Authentification service
          dic = self.c.post('/bin/kerberos/authentication-service', username="gritchie")
          tgs = dic["Client-TGS-session-key"]
          tgt = dic["TGT"]
          mdp = "Vt*1fJsM7@"
          pw = decrypt(tgs, mdp)
          #  print('password : '+pw)
          #   Authentificateur
          d = {'username': 'gritchie', 'timestamp': time.time()}
          e = json.dumps(d)
          auth = encrypt(e, pw)
          # Ticket granting service
          dic2 = self.c.post('/bin/kerberos/ticket-granting-service', TGT=tgt, service="hardware", authenticator=auth)
          sesskey = dic2['Client-Server-session-key']
          servtick = dic2['Client-Server-ticket']
          cle = decrypt(sesskey, pw)
          #  Connection service
          d2 = {'username': 'gritchie', 'timestamp': time.time()}
          e2 = json.dumps(d2)
          auth2 = encrypt(e2, cle)
          serv = self.c.post('/service/hardware/hello', ticket=servtick, authenticator=auth2)
          print(serv)
