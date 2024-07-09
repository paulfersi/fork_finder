# Fork Finder

This is my final project for the Web Technologies course.

## Introduction

Fork Finder is a social network for sharing restaurant reviews with your friends.
## Functionalities

The main view displays a feed with two tabs:
- **"Friends' Advice"** tab where users can see reviews from users they follow.
- **"Explore"** tab where users can see reviews recommended by the app.

Users can mark reviews as favorites and see them on their personal list, search for other users, and view restaurant locations on a map.

The app also enables logging in as a culinary critic to provide more detailed reviews with a 'verified' tag.

There are two groups of users: **regular users** and **culinary critics**. The users in the **Critics** group can write featured reviews,with a permission ensuring that they are the only ones who can do so.

Currently, user information and authentication logic are the same for all users, but the next step for the project is to implement a more robust and detailed authentication system for culinary critics.

## Screenshots

Feed:
<p align="center">
  <img src="/docs/screenshots/feed.png">
</p>

My Account page:
<p align="center">
  <img src="/docs/screenshots/my_account.png">
</p>

Add review for culinary critics:
<p >
  <img src="/docs/screenshots/add_critic_review.png" width="300">
</p>


## How to use it 

1 Clone the repo with 
```bash
git clone https://github.com/paulfersi/fork_finder.git

```

2. Make sure **pipenv** is installed.
   
   In the project folder execute:

```bash
   pipenv install
   pipenv shell  
```

3. Populate the database with the command:
   
```bash
python manage.py populate_db
```

4. Run the server ad connect to the localhost address:
   
```bash
python manage.py runserver
```    

Now you can login with the username "admin" and the password "1234".
To access the admin section offered by django go to the url "admin/"

#### Mapbox

1. Create a mapbox token on https://account.mapbox.com

2. At the root of the project, create a .env file and add your Mapbox token.

```env

MAPBOX_ACCESS_TOKEN=your_mapbox_access_token

```

## Technologies Used

- Python
- Django framework
- Bootstrap
- JavaScript
- Mapbox (for geocoding and map rendering)
- jQuery

For documentation on the geocoding API, visit https://docs.mapbox.com/api/search/geocoding-v5/.