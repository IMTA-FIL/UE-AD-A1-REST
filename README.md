1. Proposez des point d’entrée supplémentaires dans le service Movie pour récupérer des informations sur les films. Proposez aussi un point d’entrée help permettant de connaître l’ensemble des points d’entrée de votre service Movie. Mettez à jour la spécification openAPI en conséquence.

2. Testez votre microservice avec Postman ou une solution équivalente (https://www.postman.com/).

3. Écrivez le microservice Times à partir de la spécification OpenAPI fournie dans le repository (UE-archi-distribuees-Showtime-1.0.0-resolved.yaml) et testez votre service (sauvegardez bien vos collections de requêtes).

4. Coder le service Booking à partir de la spécification OpenAPI disponible (UE-archi-distribuees-Booking-1.0.0-resolved.yaml) et testez votre service (sauvegardez bien vos collections de requêtes).

5. Regarder le contenu du fichier user.json et imaginez une spécification openAPI pour le service User en conséquence de façon à ce qu’il utilise à la fois les services Booking et Movie. Des exemples :

6. un point d’entrée permettant d’obtenir les réservations à partir du nom ou de l’ID d’un utilisateur ce qui demandera à interroger le service Booking pour vérifier que la réservation est bien disponible à la date demandée

7. un point d’entrée permettant de récupérer les informations des films pour les réservations d’un utilisateur ce qui demandera à interroger à la fois Booking et Movie

8. Écrivez le microservice correspondant et testez votre service (sauvegardez bien vos collections de requêtes).