from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return 'This is a Flask app running on Docker!'

# Some simple routing to learn Flask
# 
# @app.route('/<name>')
# def name(name = None):
#     return render_template('base.html', name = name)
#
#
# @app.route('/login', methods=['GET','POST'])
# def login():
# 	if request.method == 'POST':
# 		return 'Send post request'
# 	else:
# 		return 'Login Page'
#
#
# @app.route('/user/<username>')
# def user(username):
# 	return 'User %s' % username

if __name__ == '__main__':
    app.run()
