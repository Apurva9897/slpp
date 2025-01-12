# @Author: Apurva Kulkarni
# @Description: This file contains the main Flask application code for the Petition Management System.


from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, Petitioner, Petition, BioID, CommitteeMember, AppConfig
from datetime import datetime
from initialize_db import initialize_bioids, initialize_committee_members, initialize_app_config
from slpp_api import api  

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("committee:"):
        email = user_id.split("committee:")[1]
        return CommitteeMember.query.get(email)
    else:
        return Petitioner.query.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        full_name = request.form['full_name']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        bio_id = request.form['bio_id']

        bioid_entry = BioID.query.filter_by(code=bio_id, used=0).first()
        if not bioid_entry:
            flash("Invalid or already used BioID.", "danger")
            return render_template('register.html')

        petitioner = Petitioner(email=email, fullname=full_name, dob=dob, password_hash=password, bioid=bio_id)
        db.session.add(petitioner)

        bioid_entry.used = 1
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        petitioner = Petitioner.query.filter_by(email=email).first()
        if petitioner and bcrypt.check_password_hash(petitioner.password_hash, password):
            login_user(petitioner)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    my_petitions = Petition.query.filter_by(petitioner_email=current_user.email).all()    
    all_petitions = Petition.query.all()    
    return render_template('dashboard.html', my_petitions=my_petitions, all_petitions=all_petitions)

@app.route('/create_petition', methods=['POST'])
@login_required
def create_petition():
    try:
        title = request.form['title']
        content = request.form['content']

        petition = Petition(
            title=title,
            content=content,
            petitioner_email=current_user.email
        )

        db.session.add(petition)
        db.session.commit()

        flash("Your petition has been created successfully!", "success")
    except Exception as e:
        flash(f"Error creating petition: {str(e)}", "danger")
    
    return redirect(url_for('dashboard'))


@app.route('/sign_petition/<int:petition_id>', methods=['POST'])
@login_required
def sign_petition(petition_id):
    petition = Petition.query.get(petition_id)

    if not petition:
        flash("Petition not found.", "danger")
        return redirect(url_for('dashboard'))

    if petition.petitioner_email == current_user.email:
        flash("You cannot sign your own petition.", "warning")
        return redirect(url_for('dashboard'))

    if petition.status != 'open':
        flash("This petition is closed and cannot be signed.", "danger")
        return redirect(url_for('dashboard'))

    if current_user in petition.signed_by:
        flash("You have already signed this petition.", "info")
        return redirect(url_for('dashboard'))

    petition.signed_by.append(current_user)
    petition.signature_count += 1
    db.session.commit()

    flash("You have successfully signed the petition.", "success")
    return redirect(url_for('dashboard'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


@app.route('/committee/login', methods=['GET', 'POST'])
def committee_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        committee_member = CommitteeMember.query.get(email)
        if committee_member and bcrypt.check_password_hash(committee_member.password_hash, password):
            login_user(committee_member)
            flash("Successfully logged in as committee member.", "success")
            return redirect(url_for('committee_dashboard'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('committee_login.html')

@app.route('/committee/dashboard')
@login_required
def committee_dashboard():
    if not isinstance(current_user, CommitteeMember):
        flash("Access restricted to committee members.", "danger")
        return redirect(url_for('committee_login'))

    petitions = Petition.query.all()
    signature_threshold = AppConfig.query.first().signature_threshold if AppConfig.query.first() else 0

    return render_template(
        'committee_dashboard.html',
        petitions=petitions,
        signature_threshold=signature_threshold
    )

@app.route('/set_threshold', methods=['POST'])
@login_required
def set_threshold():
    if not isinstance(current_user, CommitteeMember):
        return redirect(url_for('login_committee'))

    try:
        new_threshold = int(request.form['threshold'])
        if new_threshold <= 0:
            flash("Threshold must be greater than 0. Please enter a valid value.", "danger")
            return redirect(url_for('committee_dashboard'))

        settings = AppConfig.query.first()
        if not settings:
            settings = AppConfig(signature_threshold=new_threshold)
            db.session.add(settings)
        else:
            settings.signature_threshold = new_threshold
        db.session.commit()
        flash("Signature threshold updated successfully.", "success")
    except ValueError:
        flash("Invalid input. Please enter a valid number for the threshold.", "danger")
    except Exception as e:
        flash(f"Error updating signature threshold: {str(e)}", "danger")

    return redirect(url_for('committee_dashboard'))

@app.route('/respond_to_petition', methods=['POST'])
@login_required
def respond_to_petition():
    if not isinstance(current_user, CommitteeMember):
        return redirect(url_for('login_committee'))

    petition_id = request.form['petition_id']
    response_text = request.form['response']

    try:
        petition = Petition.query.get(petition_id)
        if petition and petition.status == 'open' and petition.signature_count >= AppConfig.query.first().signature_threshold:
            petition.response = response_text
            petition.status = 'closed'
            db.session.commit()
            flash("Response saved successfully and petition has been closed.", "success")
        else:
            flash("Error: Petition is either invalid or does not meet the threshold.", "danger")
    except Exception as e:
        flash(f"Something went wrong {str(e)}", "danger")

    return redirect(url_for('committee_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
        initialize_bioids()
        initialize_committee_members(bcrypt)
        initialize_app_config()
    app.run(debug=True)
