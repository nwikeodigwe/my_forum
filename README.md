Single-database configuration for Flask.
# ForumAPP

# Description:
 A web-based forum application built using Flask and SQLAlchemy, where users can create posts, comment on posts, and interact with each other by liking posts and comments.

# API References

 Endpoints                  Method      Parameters                       Description
 /users/                    GET          -                               Retrieve all users
 /users/<id>                GET         :id                              Retrieve user with given id
 /users/<id>/posts          GET         :id                              Retrive posts for user
 /users/<id>/comments       GET         :id                              Retrive comments for user
 /users/<id>/likes/posts    POST        :id, user_id, post_id            Like post with given id
 /users/<id>/unlike/posts   DELETE      :id, post_id                     Unlike post with given id
 /users/<id>/likes/comments POST        :id, user_id, post_id            Like comment with given id
 /users/<id>/unlike/commentsDELETE      :id, comment_id                  Unlike comment with given id
 /users/                    POST        username,name,password           Create new user
 /users/<id>                PATCH|PUT   :id,username|name|password       Update user with id
 /users/<id>                DELETE      :id                              Delete user with given id
 /posts/                    GET          -                               Retrieve all posts
 /posts/<id>                GET         :id                              Retrieve post with given id
 /posts/<id>/likes          GET         :id                              Retrive likes for posts
 /posts/<id>/comments       GET         :id                              Retrive comments for posts
 /posts/                    POST        user_id,title,description        Create new post
 /posts/<id>                PATCH|PUT   :id,username|name|password       Update post with given id
 /posts/<id>                DELETE      :id                              Delete post
 /comments/                 GET          -                               Retrieve comments
 /comments/<id>             GET         :id                              Retrieve comment with id
 /comments/<id>/likes       GET         :id                              Retrieve likes for comment
 /comments/                 POST        user_id,post_id,description      Create new comment
 /comments/<id>             PATCH|PUT   :id,description                  Update comment with id


# How did the project's design evolve over time?

Initially the design was simpler with minimal endpoint, but over time during the documentation I realised there were other notworthy endpoins that could be included as well as other features like the like and unlike of posts and comments

# Did you choose to use an ORM or raw SQL? Why?

I chose to use an ORM as opposed to using raw sql because of the simplicity of executing queries and defining relationships as well as migrations with database design. Using SQLAchemy removes alot of abstration from executing simple queries as well as complex queries, defining table relationship and creating migrations. The flexibility SQLAchemy offers as well as compactibility with other database engines enhances scalability and improves code readablity

# What future improvements are in store, if any?

Considering how this system has evolved over a short time given that my intention was only to build a simple REST api for a forum app, I can see how much more improvement can be done and these include
An auth system to authenticate users
A role based login system for users
Further improving the database design to congest comments like and posts like table
implementation of better security and access to api endpoints
Categorizing post based on topics 
