import psycopg2


class DatabaseSource:
    def __init__(self, db_config=dict()) -> None:
        self.conn = psycopg2.connect(
            "dbname={} user={} password={} host={} port={}".format(
                db_config.get('DATABASE_NAME'),
                db_config.get('DATABASE_USER'),
                db_config.get('DATABASE_PASSWORD'),
                db_config.get('DATABASE_HOST'),
                db_config.get('DATABASE_PORT')))
        self.cur = self.conn.cursor()

    def save_live_web_health(self, payload):
        self.cur.execute(
            '''
            INSERT INTO web_health.live(web_url,response_time,status_code,last_checked_at)
            VALUES (%s,%s,%s,%s) ON CONFLICT (web_url) DO UPDATE
            SET status_code=EXCLUDED.status_code,
            response_time=EXCLUDED.response_time,
            last_checked_at=EXCLUDED.last_checked_at;''',
            [
                payload["web_url"],
                payload["response_time"],
                payload["http_status_code"],
                payload["last_checked_at"]])
        self.conn.commit()

    def terminate(self):
        if self.conn:
            self.cur.close()
            self.conn.close()
