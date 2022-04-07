query_url = "SELECT url FROM urls WHERE type_url=%(type)s"
query_insert = "INSERT INTO urls (urls_id, url, type_url) VALUES (?, ?, ?)"
arg_url_simple = {'type':'simpled'}
arg_url = 'http:stestste/test'
arg_url_top = {'type':'top'}

query_exists = "SELECT id FROM subscribers WHERE personal_uid=?"
query_add = "INSERT INTO subscribers (personal_uid, status) VALUES (?, ?)"
query_filter = "INSERT INTO filters (query_post, user_id) VALUES (?, ?)"
query_filter_update = "UPDATE filters SET query_post = ? WHERE user_id = ?"
query_update = "UPDATE subscribers SET status = ? WHERE personal_uid = ?"
query_update_f = "UPDATE subscribers SET filters_id = ? WHERE personal_uid = ?"
query_get_filters = "SELECT query_post, last_post, user_id FROM filters"
query_update_filters = "UPDATE filters SET last_post=? WHERE user_id=?"

up = "CREATE TABLE subscribers (id INTEGER PRIMARY KEY, personal_uid INTEGER, status BOOL)"

up1 = "CREATE TABLE filters (id INTEGER PRIMARY KEY, query_post TEXT, last_post TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES subsctibers(id))"