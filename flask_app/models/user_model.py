from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash
import re
# from flask_app.models import tree_model
# from flask_app.models import tree_model this is the good one 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#------- class constructor created from the MySql database-----#
class User :
    def __init__(self,data) :
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.gym_level = data ['gym_level']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


#----- create a method to add a user on registration ------#
    @classmethod
    def create_user(cls,data):
        query = '''
            INSERT INTO users (first_name,last_name,email,gym_level,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(gym_level)s,%(password)s)
        '''
        return connectToMySQL(DATABASE).query_db( query, data )


#------- finds user by email--------#
    @classmethod
    def find_by_email(cls,data):
        query = '''
            SELECT * FROM users
            WHERE email = %(email)s
        '''
        results = connectToMySQL(DATABASE).query_db( query, data )

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False


#------- finds user by id--------#
    @classmethod
    def find_by_user(cls,id):

        data = {
            'id' : id,
        }
        query = '''
            SELECT * FROM users
            WHERE id = %(id)s
        '''
        results = connectToMySQL(DATABASE).query_db( query, data )

        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        else:
            return False



#----- this staticmethod makes flash messages pop up-------#
    @staticmethod
    def validate(data):
        is_valid= True
        #---- if statements for each input----#
        if len(data['first_name']) < 2:
            flash('please provide first name longer than 1 letter')
            is_valid = False

        if len(data['last_name']) < 2:
            flash('please provide last name longer than 1 letter')
            is_valid = False

        if len(data['gym_level']) < 2:
            flash('please provide gym_level longer than 1 letter')
            is_valid = False

        if len(data['password']) < 8:
            flash('please provide a password of at least 8 characters')
            is_valid = False

        if data['password'] != data['password2']:
            flash('passwords did not match, please reenter ')
            is_valid = False
            
        if len(data['email']) < 1:
            flash('please provide an email')
            is_valid = False
        # to run regex must import re and EMAIL_REGEX at top
        if not EMAIL_REGEX.match(data['email']):
            flash('please enter a VALID email')
            is_valid = False

        elif User.find_by_email(data):
            flash('Email already registered')
            is_valid = False

        return is_valid

#------- validate login------#
    @classmethod 
    def validate_login (cls,data):
    
        found_user = cls.find_by_email(data)
        # print(found_user)
        #---- checking to see if user exist------#
        if not found_user:
            flash('invalid login')
            return False

#---if user does exist checking to see if password matches data---#
        elif not bcrypt.check_password_hash(found_user.password,data['password']):
            flash('invalid login')
            return False




#----- if neither of those triggered then we can return user thats logging in-----#
        return found_user
