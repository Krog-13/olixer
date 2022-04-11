query_url = "SELECT url FROM urls WHERE type_url=%(type)s"
query_insert = "INSERT INTO urls (urls_id, url, type_url) VALUES (%s, %s, %s)"
arg_url_simple = {'type':'simpled'}
arg_url = 'http:stestste/test'
arg_url_top = {'type':'top'}

query_exists = "SELECT id FROM subscribers WHERE personal_uid= :uid"
query_add = "INSERT INTO subscribers (personal_uid, status) VALUES (:uid, :status)"
query_filter = "INSERT INTO filters (query_post, user_id) VALUES (:query_post, :user_id)"
query_filter_update = "UPDATE filters SET query_post = :query_post WHERE user_id = :user_id"
query_update = "UPDATE subscribers SET status = :status WHERE personal_uid = :uid"
query_update_f = "UPDATE subscribers SET filters_id = %s WHERE personal_uid = %s"
query_get_filters = "SELECT query_post, last_post, user_id FROM filters " \
                    "LEFT JOIN subscribers ON filters.user_id=subscribers.id" \
                    "WHERE status = true"
query_update_filters = "UPDATE filters SET last_post= :last_post WHERE user_id= :user_id"
query_person = "SELECT id FROM subscribers WHERE personal_uid=:uid"
query_exist_filter = "SELECT * FROM filters WHERE user_id=:user_id"
query_send_user = "SELECT personal_uid FROM subscribers WHERE id=:id"

table1 = "CREATE TABLE subscribers (id INTEGER PRIMARY KEY, personal_uid INTEGER NOT NULL, status BOOLEAN NOT NULL);"

table2 = "CREATE TABLE filters (id INTEGER PRIMARY KEY, query_post VARCHAR(300), last_post VARCHAR(300), user_id INTEGER," \
         "CONSTRAINT pk_filters_sub FOREIGN KEY(user_id) REFERENCES subscribers (id));"

query = "DROP TABLE subscribersq"
query1 = "DROP TABLE filtersq"