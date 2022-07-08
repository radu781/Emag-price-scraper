import nest_asyncio
from controllers.base import app
from controllers.index import index_blueprint
from controllers.mine import mine_blueprint

nest_asyncio.apply()
app.register_blueprint(index_blueprint)
app.register_blueprint(mine_blueprint)

if __name__ == "__main__":
    app.run(port=80, debug=True)
