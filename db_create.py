from config import db
from models import User
from models import BlogPost

db.create_all()
#create database and table create

# db.session.add(User("michael","michale@realpython.com","i will never tell"))
# db.session.add(User("admin","ad@min.com","admin"))
# db.session.add(User("mike","mike@herman.com","tell"))
# #insert User data
#
# db.session.add(BlogPost("Good","I am good"))
# db.session.add(BlogPost("Well","I am well"))
# db.session.add(BlogPost("Excellent","I am excellent"))
# db.session.add(BlogPost("Okay","i am okay"))
# db.session.add(BlogPost("postgres","we setuo a local postgres instance"))
#insert Blogpost data

# another convenient method
michael = User("michael","michale@realpython.com","i will never tell")
admin = User("admin","ad@min.com","admin")
mike = User("mike","mike@herman.com","tell")

michael.posts.append(BlogPost("Good","I am good"))
michael.posts.append(BlogPost("Excellent","I am excellent"))
mike.posts.append(BlogPost("Well","I am well"))
mike.posts.append(BlogPost("Okay","i am okay"))
admin.posts.append(BlogPost("postgres","we setuo a local postgres instance"))

db.session.add(michael)
db.session.add(mike)
db.session.add(admin)

db.session.commit()

