query_url = "SELECT url FROM urls WHERE type_url=%(type)s"
query_insert = "INSERT INTO urls (urls_id, url, type_url) VALUES (%s, %s, %s)"
arg_url_simple = {'type':'simpled'}
arg_url = 'http:stestste/test'
arg_url_top = {'type':'top'}

query_exists = "SELECT id FROM subscribers WHERE personal_uid=%s"
query_add = "INSERT INTO subscribers (personal_uid, status) VALUES (%s, %s)"
query_filter = "INSERT INTO filters (query_post, user_id) VALUES (%s, %s)"
query_filter_update = "UPDATE filters SET query_post = %s WHERE user_id = %s"
query_update = "UPDATE subscribers SET status = %s WHERE personal_uid = %s"
query_update_f = "UPDATE subscribers SET filters_id = %s WHERE personal_uid = %s"
query_get_filters = "SELECT query_post, last_post, top_post, user_id FROM filters"
query_update_filters = "UPDATE filters SET last_post=%s WHERE user_id=%s"

table1 = "CREATE TABLE subscribersq (id INTEGER PRIMARY KEY, personal_uid INTEGER NOT NULL, status BOOLEAN NOT NULL);"

table2 = "CREATE TABLE filtersq (id INTEGER PRIMARY KEY, query_post VARCHAR(300), last_post VARCHAR(300), user_id INTEGER," \
         "CONSTRAINT pk_filters_sub FOREIGN KEY(user_id) REFERENCES subscribersq (id));"

query = "SELECT id FROM subscribers WHERE personal_uid=:uid"