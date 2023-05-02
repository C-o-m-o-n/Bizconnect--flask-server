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
    
        
if __name__ == '__main__':
    app.run(debug=True)
