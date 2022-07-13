import nest_asyncio
from controllers import app
from controllers.index import index_blueprint
from controllers.mine import mine_blueprint
from controllers.user_logout import user_logout_blueprint
from controllers.user_login import user_login_blueprint
from controllers.track_item import track_item_blueprint
from controllers.item_page import item_page_blueprint
from controllers.api.search_items import search_api

nest_asyncio.apply()
app.register_blueprint(index_blueprint)
app.register_blueprint(mine_blueprint)
app.register_blueprint(user_logout_blueprint)
app.register_blueprint(user_login_blueprint)
app.register_blueprint(track_item_blueprint)
app.register_blueprint(item_page_blueprint)
app.register_blueprint(search_api)

if __name__ == "__main__":
    app.run(port=80, debug=True)
