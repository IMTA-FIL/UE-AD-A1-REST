# Introduction

This Repo contains the Practical work on REST and FLASK

## Installation

### 1. With a docker container

If docker is installed on your computer, you must :

1. clone the github repository
2. open a cmd
3. go into the repository using

   ```bash
   cd path/to/your/repository
   ```

4. open the docker app to start the kernel
5. run

   ```
   docker-compose up --build
   ```

### 2. Without a docker container

If you don't have docker on your computer, you can :

1. clone the github repository
2. open a 4 cmd
3. go into the repository using

   ```bash
   cd path/to/your/repository
   ```

4. go into showtimes using

   ```bash
   cd ./showtime
   ```

5. then, to launch the service, use

   ```bash
   python showtime.py
   ```

6. repeat in a different cmd for user, movie and booking

## What we did

We suceeded to finish the integrality of what was asked in this pratical work. Moreover, we add enough time to complexify a
the services Movies, Bookings and User. Let's see what we add in each service :

### Movies

As explained before we suceeded to produce a service movie which respects what was ask in the practical work.
Furthemore, we added few entry points which were not asked :

1. _/help_ which gives all the entries available in the service movie

2. _/directors_ which returns all the **directors** of the movies available

3. _/directors/<**movie_id**>/<**director_name**>_ which change the **director** of the movie with the id **movie_id**

4. _/movies_per_ratings_ which returns the list of the movies available \*sorted by **decreasing rate\***

5. _/movieid_linked_movietitle_ which returns a dict python which associates an **id** to a **movie name** (used in **User**)

We also added few **error code** to our service.

### Bookings

Same as above :

1. _/bookings/<**userid**>_ which change a little. Here decided to not throw and error and take account of the case when the _user isn't in the database_, when _the user is in the database and there isn't any bookings at the date_ given and finally when _the user is in the database and the date exists but the movie wasn't booked at this date_.

2. _/movies_at_the_date/<**date**>_ which calls the service showtime and return all the movies available at the date **date**

### User

We decided to deem this service as our frontend so all the entry points returns a html page associated with a template located in the folder _/templates_.

Moreover, we decided to suppose that user of this service give only his name and not his id. Thus we convert his name into an id thanks to the user.json database

Let's see what is able **User** :

1. _/movies_per_ratings_ : It is able to show the list of the movies available calling **Movies**.

2. _/movies_available/<**date**>_ : By calling **Movies** (to get the names of the movies) and **Bookings**, this service can show the name of the movies available at **date**.

3. _/book_a_movie_ : this entry call **Booking** to book a movie at the specified date. It needs to also call **Movies** because the user gives the name of the movie and we need the id of the movie

4. _/booking_made/<**username**>_ : It calls **Booking** to get all the bookings made by the user **username**
