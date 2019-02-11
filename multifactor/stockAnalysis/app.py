import os,sys
sys.path.append('/Users/admin/Desktop/soft/flask/examples/web')

from flask import Flask
# from web import stockAnalysis
from stockAnalysis import finance


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY='dev',
    #     # store the database in the instance folder
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    app.register_blueprint(finance.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5001)


  



