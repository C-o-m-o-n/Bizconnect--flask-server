from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class JobData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    user_photo = db.Column(db.String(255))
    phone = db.Column(db.Integer )
    job_name = db.Column(db.String(255))
    job_photo = db.Column(db.String(255))
    job_description = db.Column(db.String(255))
    job_location = db.Column(db.String(255))


#users model for the bloodBank starts here
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    user_photo = db.Column(db.String(255))
    phone = db.Column(db.Integer )
    state = db.Column(db.String(255) )
    city = db.Column(db.String(255) )
    street = db.Column(db.String(255) )
    age = db.Column(db.Integer )
    gender = db.Column(db.String(255) )
    blood_type = db.Column(db.String(255) )
#users medel for the bloodBank ends here


@app.route('/jobs', methods=['GET','POST'])
def post_job():
  if request.method == 'POST':
    user_id = request.form.get('user_id')
    name = request.form.get('name')
    job_name = request.form.get('job_name')
    email = request.form.get('email')
    user_photo = request.form.get('user_photo')
    phone = request.form.get('phone')
    job_photo = request.form.get('jobPhoto')
    job_description = request.form.get('jobDescription')
    job_location = request.form.get('jobLocation')
    
    new_data = JobData(user_id=user_id, name=name, email=email,user_photo=user_photo,phone=phone, job_name=job_name, job_photo=job_photo,job_description=job_description, job_location=job_location)
    db.create_all()
    db.session.add(new_data)
    db.session.commit()
    return 'Data saved successfully'
  
  elif request.method == 'GET':
    jobs = JobData.query.all()
    serialized_jobs = []
    for job in jobs:
        print(job)
        serialized_job = {
            'id': job.id,
            'name': job.name,
            'email': job.email,
            'user_photo': job.user_photo,
            'user_id': job.user_id,
            'phone': job.phone,
            'job_title': job.job_name,
            'job_description': job.job_description,
            'job_location': job.job_location,
            'job_photo': job.job_photo,
        }
        serialized_jobs.append(serialized_job)

    response = jsonify(serialized_jobs)

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    return 'Job details saved successfully'


@app.route('/jobs/<int:id>', methods=['GET'])
def get_job(id):
    job = JobData.query.filter_by(id=id).first()
    serialized_job = {
            'id': job.id,
            'name': job.name,
            'email': job.email,
            'user_photo': job.user_photo,
            'user_id': job.user_id,
            'phone': job.phone,
            'job_title': job.job_name,
            'job_description': job.job_description,
            'job_location': job.job_location,
            'job_photo': job.job_photo,
    }
    response = jsonify(serialized_job)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/my_jobs', methods=['GET'])
def my_jobs():
    user_id = request.args.get('user_id')
    my_jobs = JobData.query.filter_by(user_id=user_id)
    for job in my_jobs:
        serialized_job = {
            'id': job.id,
            'name': job.name,
            'email': job.email,
            'user_photo': job.user_photo,
            'user_id': job.user_id,
            'phone': job.phone,
            'job_title': job.job_name,
            'job_description': job.job_description,
            'job_location': job.job_location,
            'job_photo': job.job_photo,
    }
    response = jsonify(serialized_job)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#users for the bloodBank starts here
@app.route('/users', methods=['GET','POST'])
def users():
  if request.method == 'POST':
    firebase_id = request.form.get('firebase_id')
    name = request.form.get('name')
    email = request.form.get('email')
    user_photo = request.files['user_photo']
    user_photo_name = user_photo.save(f'images/{user_photo.filename}')
    phone = request.form.get('phone')
    state = request.form.get('state')
    city = request.form.get('city')
    street = request.form.get('street')
    age = request.form.get('age')
    gender = request.form.get('gender')
    blood_type = request.form.get('blood_type')
    
    
    new_data = Users(
      name=name,
      phone=phone,
      firebase_id=firebase_id,
      email=email,
      user_photo=user_photo.filename,
      state=state,
      city=city,
      street=street,
      age=age,
      gender=gender,
      blood_type=blood_type,
      )
    db.create_all()
    db.session.add(new_data)
    db.session.commit()
    return 'Data saved successfully'
  
  elif request.method == 'GET':
    user_email = request.args.get('email')
    user = Users.query.filter_by(email=user_email).first()
    serialized_users = []
    serialized_user = {
      'id': user.id,
      'name': user.name,
      'firebase_id': user.firebase_id,
      'email': user.email,
      'user_photo': user.user_photo,
      'phone': user.phone,
      'state': user.state,
      'city': user.city,
      'street': user.street,
      'age': user.age,
      'gender': user.gender,
      'blood_type': user.blood_type,
        }
    serialized_users.append(serialized_user)

    response = jsonify(serialized_users)
    print("response:==", response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    


@app.route('/users/<int:id>', methods=['GET'])
def get_users(id):
    user = Users.query.filter_by(id=id).first()
    serialized_user = {
            'id': user.id,
            'name': user.name,
            'firebase_id': user.firebase_id,
            'email': user.email,
            'user_photo': user.user_photo,
            'phone': user.phone,
            'state': user.state,
            'city': user.city,
            'street': user.street,
        }
    serialized_userse.append(serialized_user)
    response = jsonify(serialized_users)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    return 'user details saved successfully'

#users for the bloodBank ends here


if __name__ == '__main__':
    app.run(debug=True)
