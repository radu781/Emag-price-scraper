import nest_asyncio

nest_asyncio.apply()

from controllers import app
from controllers.mine import mine_blueprint
from controllers.user_logout import user_logout_blueprint
from controllers.user_login import user_login_blueprint
from controllers.item_page import item_page_blueprint
from controllers.track_items import track_item_blueprint
from controllers.search_items import search_api
from controllers.user_register import user_register_blueprint

from views.index import index_blueprint
from views.track_item_view import track_item_view_blueprint
from views.login_view import user_login_view_blueprint
from views.logout_view import user_logout_view_blueprint
from views.mine_view import mine_view_blueprint
from views.item_view import item_page_view_blueprint
from views.register_view import user_register_view_blueprint
from views.login_inner import user_login_inner_blueprint
from views.register_inner import user_register_inner_blueprint

app.register_blueprint(index_blueprint)
app.register_blueprint(mine_blueprint)
app.register_blueprint(user_logout_blueprint)
app.register_blueprint(user_login_blueprint)
app.register_blueprint(track_item_blueprint)
app.register_blueprint(item_page_blueprint)
app.register_blueprint(search_api)
app.register_blueprint(track_item_view_blueprint)
app.register_blueprint(user_login_view_blueprint)
app.register_blueprint(user_logout_view_blueprint)
app.register_blueprint(mine_view_blueprint)
app.register_blueprint(item_page_view_blueprint)
app.register_blueprint(user_register_blueprint)
app.register_blueprint(user_register_view_blueprint)
app.register_blueprint(user_login_inner_blueprint)
app.register_blueprint(user_register_inner_blueprint)

if __name__ == "__main__":
    app.run(port=80, debug=True)
