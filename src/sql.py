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
query_send_user = "SELECT personal_uid FROM subscribers WHERE id=%s"