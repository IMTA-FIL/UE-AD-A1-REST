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
   pip install foobar
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

We suceeded in finishing everything that was asked in the assignement. Moreover, we added more elements to the services Movies, Bookings and User. Let's see what we add in each service :

### Movies

As explained before we suceeded in producing a "movie" service that respects the assignement.
Furthemore, we added a few additional entry points :

1. _/help_ : gives all the entries available in the service movie

2. _/directors_ : returns all the **directors** of the available movies

3. _/directors/<**movie_id**>/<**director_name**>_ : changes the **director** of the movie with the id **movie_id**

4. _/movies_per_ratings_ : returns the list of the movies available \*sorted by **decreasing rate\***

5. _/movieid_linked_movietitle_ : returns a dict python which associates an **id** to a **movie name** (used in **User**)

We also added a few **error code** to our service.

### Bookings

Just like Movies, we managed to add a couple of new entry points :

1. _/bookings/<**userid**>_ : changes the user associated to a booking. Here, we decided not to throw an error when the _user isn't in the database_, when _the user is in the database and there isn't any bookings at the date_ given and finally when _the user is in the database and the date exists but the movie wasn't booked at this date_.

2. _/movies_at_the_date/<**date**>_ : calls the service showtime and return all the movies available at the date **date**

### User

We decided to deem this service as our frontend so that all of the entry points return a html page associated with a template located in the folder _/templates_.

Moreover, we are supposing that the user would only give his name and not his id as well. The id will be obtained by converting the user's name, thanks to the user.json database

The entry points available for **User** are :

1. _/movies_per_ratings_ : Shows the list of the movies available, sorted by rating calling **Movies**.

2. _/movies_available/<**date**>_ : By calling **Movies** (to get the names of the movies) and **Bookings**, it returns a list with the names of the movies available at **date**.

3. _/book_a_movie_ : Calls **Booking** to book a movie at the specified date. It needs to also call **Movies** because the user gives the name of the movie and we need its id for the booking

4. _/booking_made/<**username**>_ : It calls **Booking** to get all the bookings made by the user **username**

### Showtime

For showtime, we decided to follow the instructions of the assignement and therefore we ended up with the two entry points :

1. /showtimes : returns the whole database (the full schedule with all the movies at all dates)

2. /showmovies/{date} : returns all movies set to be shown during the specific **date**
