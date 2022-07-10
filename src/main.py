import nest_asyncio
from controllers import app
from controllers.index import index_blueprint
from controllers.mine import mine_blueprint
from controllers.user_logout import user_logout_blueprint
from controllers.user_login import user_login_blueprint

nest_asyncio.apply()
app.register_blueprint(index_blueprint)
app.register_blueprint(mine_blueprint)
app.register_blueprint(user_logout_blueprint)
app.register_blueprint(user_login_blueprint)

if __name__ == "__main__":
    app.run(port=80, debug=True)
