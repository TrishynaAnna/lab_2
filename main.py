from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.uset_form import UserForm
from forms.group_form import GroupForm
from forms.user_group_form import UserGroupForm
from sqlalchemy.sql import func
import plotly
import json
import plotly.graph_objs as go
from dao.orm.model import *

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/postgres'
db = SQLAlchemy(app)



@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
def user():

    result = db.session.query(User).all()

    return render_template('user.html', users = result)


@app.route('/new_user', methods=['GET','POST'])
def new_user():

    form = UserForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('user_form.html', form=form, form_name="New user", action="new_user")
        else:
            new_user = User(
                                user_id=form.user_id.data,
                                user_name=form.user_name.data,
                            )

            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('user'))

    return render_template('user_form.html', form=form, form_name="New user", action="new_user")



@app.route('/edit_user', methods=['GET','POST'])
def edit_user():

    form = UserForm()


    if request.method == 'GET':

        user_id =request.args.get('user_id')
        user = db.session.query(User).filter(User.user_id == user_id).one()

        # fill form and send to user
        form.user_id.data = user.user_id
        form.user_name.data = user.user_name

        return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")


    else:

        if form.validate() != False:
            return render_template('user_form.html', form=form, form_name="Edit user", action="edit_user")
        else:
            # find user
            user = db.session.query(User).filter(User.user_id == form.user_id.data).one()

            # update fields from form data
            user.user_id = form.user_id.data
            user.user_name = form.user_name.data

            db.session.commit()

            return redirect(url_for('user'))





@app.route('/delete_user', methods=['POST'])
def delete_user():

    user_id = request.form['user_id']

    result = db.session.query(User).filter(User.user_id == user_id).one()

    db.session.delete(result)
    db.session.commit()


    return user_id


@app.route('/group', methods=['GET'])
def group():

    result = db.session.query(Group).all()

    return render_template('group.html', groups = result)


@app.route('/new_group', methods=['GET','POST'])
def new_group():

    form = GroupForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('group_form.html', form=form, form_name="New group", action="new_group")
        else:
            new_group= Group(
                                group_id=form.group_id.data,
                                group_name=form.group_name.data,
                                group_topic=form.group_topic.data
                            )

            db.session.add(new_group)
            db.session.commit()


            return redirect(url_for('group'))

    return render_template('group_form.html', form=form, form_name="New group", action="new_group")



@app.route('/edit_group', methods=['GET','POST'])
def edit_group():

    form = GroupForm()


    if request.method == 'GET':

        group_id = request.args.get('group_id')
        group = db.session.query(Group).filter(Group.group_id == group_id).one()

        # fill form and send to user
        form.group_id.data = group.group_id
        form.group_name.data = group.group_name
        form.group_topic.data = group.group_topic

        return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")


    else:

        if form.validate() != False:
            return render_template('group_form.html', form=form, form_name="Edit group", action="edit_group")
        else:
            # find user
            group = db.session.query(Group).filter(Group.group_id == form.group_id.data).one()

            # update fields from form data
            group.group_id = form.group_id.data
            group.group_name = form.group_name.data
            group.group_topic = form.group_topic.data

            db.session.commit()

            return redirect(url_for('group'))





@app.route('/delete_group', methods=['POST'])
def delete_group():

    group_id = request.form['group_id']

    result = db.session.query(Group).filter(Group.group_id == group_id).one()

    db.session.delete(result)
    db.session.commit()


    return group_id

@app.route('/gpoupuser', methods=['GET'])
def gpoupuser():

    result = db.session.query(User_Group).all()

    return render_template('groupuser.html', gpoupusers = result)


@app.route('/new_gpoupuser', methods=['GET','POST'])
def new_gpoupuser():

    form = UserGroupForm()


    if request.method == 'POST':
        if form.validate() != False:
            return render_template('groupuser_form.html', form=form, form_name="New gpoupuser", action="new_gpoupuser")
        else:
            new_gpoupuser= User_Group(
                                user_id=form.user_id.data,
                                group_id=form.group_id.data,
                            )

            db.session.add(new_gpoupuser)
            db.session.commit()


            return redirect(url_for('gpoupuser'))

    return render_template('groupuser_form.html', form=form, form_name="New gpoupuser", action="new_gpoupuser")



@app.route('/delete_gpoupuser', methods=['POST'])
def delete_gpoupuser():

    user_id = request.form['user_id']
    group_id = request.form['group_id']


    result = db.session.query(User_Group).filter(User_Group.user_id == user_id).filter(User_Group.group_id == group_id).one()

    db.session.delete(result)
    db.session.commit()


    return str(result.user_id)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print("")
    query1 = (
        db.session.query(
            User.user_name,
            func.count(User_Group.group_id).label('group_count')
        ).
            outerjoin(User_Group).
            group_by(User.user_name)
    ).all()

    query2 = (
        db.session.query(
            Group.group_name,
            func.count(Group_Post.post_id).label('hashtag_count')
        ).
            outerjoin(Group_Post).
            group_by(Group.group_name)
    ).all()

    name, group_count = zip(*query1)
    bar = go.Bar(
        x=name,
        y=group_count
    )

    name, hashtag_count = zip(*query2)
    pie = go.Pie(
        labels=name,
        values=hashtag_count
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)
if __name__ == "__main__":
    app.run()




