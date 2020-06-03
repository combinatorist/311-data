import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))


if __name__ == '__main__':
    import db
    import pb
    from datetime import datetime
    from utils.log import log_heading

    time_since_update = datetime.utcnow() - db.info.last_updated()
    if time_since_update.days >= 1:
        log_heading('updating database')
        db.requests.update()

    if pb.enabled:
        log_heading('populating picklebase')
        pb.populate()
    else:
        pb.clear_data()
