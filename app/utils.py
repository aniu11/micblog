# coding:utf-8

PER_PAGE = 3
#
# Flask-SQLAlchemy 天生就支持分页。比如如果我们想要得到用户的前三篇文章，我们可以这样做：
#
# pagination = user.posts.paginate(1, PER_PAGE, False).items
# paginate 方法能够被任何查询调用。它接受三个参数:
#
# 页数，从 1 开始。
# 每一页的项目数，这里也就是说每一页显示的 blog 数。
# 错误标志。如果是 True，当请求的范围页超出范围的话，一个 404 错误将会自动地返回到客户端的网页浏览器。如果是 False，返回一个空列表而不是错误。
# 从 paginate 返回的值是一个 Pagination 对象。这个对象的 items 成员包含了请求页面项目（本文是指 blog ）的列表。在 Pagination 对象中还有其它有帮助的东西，我们将在后面能看到。
# http://127.0.0.1:5000/user/1           <-- page #1 (default)
# http://127.0.0.1:5000/user/1/page/1    <-- page #1
