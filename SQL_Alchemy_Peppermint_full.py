
# coding: utf-8

# ## SQL Alchemy:
# *https://www.sqlalchemy.org/*
# 
# ### Its an Object Relational Mapper
# * Map objects to relations
# 
# ### So why do we need this?
# * A layer of abstraction, to be db agnostic (T-SQL, P-SQL etc)
# * Remove the need for writing sql syntax (everyone breathes a sigh of relief!)
# * Enable us to interface with other code, e.g front-end code or other Python stuff
# 
# ##### *(pip install sqlalchemy)*

# 
# 
# **Structures to understand:**
# 
# * A **Table** that represents a table in a database.
# * A **class object** that represents a Table in Python.
# * How **SQL Alchemy** fits into the larger picture of back and front end
# * The **CRUD** statements, and their equivalent in SQL Alchemy
#     * We'll learn about SQL Alchemy by doing some CRUD

# ---

# ### step by step guide to using sqlalchemy:

# * Setup your imports - sqlalchemy etc
# * Create a db connection - handshake between python and postgres
# * create a declarative base - explains the structure of the handshake (metadata) to postgres
# * create your classes - the objects which represent your postgres tables
# * run base.metadata.create_all - links the structure between python and postgres
# * create a sessionmaker - create a pipe for ferrying information (rows) between python and postgres
# * perform RUD (read, update, delete row) queries through the sessionmaker - the sqlalchemy syntax goes here
# * commit your queries
# * repeat as necessary!

# ---

# Setup your imports

# In[1]:


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer


# _(Have a look at the data structure we are going to access)_

# In[5]:


import pandas as pd
df = pd.read_csv('movies.csv')
df.head()


# ### And start to create our ORM structures
# 

# Create a database connection 

# In[2]:


user_name = 'postgres'
user_password = 'postgres'
db_name = 'movies'

windows_db_string = f'postgres://{user_name}:{user_password}@localhost/{db_name}'
mac_db_string = f'postgres://localhost/movies'


# In[3]:


db = create_engine(windows_db_string, echo=True) #echo will print out all the sql commands we are generating


# _Now we can do the simplest form of sql alchemy interaction:_
# * db.execute()
# * just put sql syntax directly into the parentheses
# * **We don't want to do this normally, but its nice to know**

# In[ ]:


db.execute('''create table if not exists movies(
                movieid int primary key,
                title varchar(512),
                genres varchar(1024)
            );''')


# **But this is clunky! We can do better, using SQL Alchemy (Python) code**

# ---

# **Create tables**
# 
# Create a declarative base (which allows to access all aspects of the ORM)

# In[6]:


base = declarative_base()


# ---

# 2: Now we create our tables:
# 
# *We use classes which is a python structure we'll cover soon*

# In[7]:


class Test_Movies(base):
    
    __tablename__ = 'test_movies'
    movieid = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)
    
    def __repr__(self):
        return f'movieid = {self.movieid}, title={self.title}'


# 3: run base.metadata.create_all(db): Create all tables in the Base
# 
# The base examines what we've created, and sends appropriate data to the db

# In[8]:


base.metadata.create_all(db)


# ---

# #### Update - we update our tables with row information

# 
# Create a sessionmaker to add items to the tables
# 
# _(Sessions are complicated to explain, they behave like a buffer, which remembers what we're doing in our Python code and updates the database with that information when we tell it to)_.

# In[9]:


Session = sessionmaker(db)
session = Session()


# Now perform all the RUD queries you want. For this the workflow is:
# 
# * Create the stuff you want to add 
# * Add the stuff to the session - data is not in the db (its in a buffered state), wipe the ram, wipe what you've done
# * Commit the stuff to the session - data is in the db, the ram is cleared

# **Lets add items one by one using add()**

# In[10]:


# row1 = Test_Movies(movieid=999, title='Mission Impossible', genres='Action')
# session.add(row1)
# session.commit()


# **Lets add items all together in a for loop using add_all()**

# In[ ]:


df.head()


# In[12]:


#create a sql table from a dataframe
df.to_sql('test_test_movies', db)


# In[11]:


table_items = []

for i, row in df.iterrows():
  #  if not session.query(Test_Movies).filter_by(movieid=row['movieid']):
     table_items.append(Test_Movies(movieid=row[0], title=row[1], genres=row[2]))
    
session.add_all(table_items)
session.commit()


# #### Read - lets do select statements in SQL Alchemy

# Return everything from a table using all()

# In[ ]:


#SELECT * FROM test_movies;
session.query(Test_Movies).all()


# Or make a filtered query using filter()

# In[ ]:


#SELECT * FROM test_movies WHERE title ~ 'Mission Impossible';
#session.query(Test_Movies).filter('mission impossible')
session.query(Test_Movies).filter(Test_Movies.title.like('Mission Impossible'))
session.query(Test_Movies).filter_by(title='Mission Impossible')


# #### Delete - lets delete some rows from our tables

# Delete items using delete()

# In[ ]:


session.delete(row1)
session.commit()

