from smartcard.System import readers

# récupère la liste des lecteurs disponibles
r = reader()
print(r)

connection = r.[0].createConnection()
connection.connect()
