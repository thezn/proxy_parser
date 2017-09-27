from .database import session, proxy_table


class ProxyParserPipeline(object):
    def process_item(self, item, spider):
        present = session.query(proxy_table).filter_by(
            ip_address=item.get('ip_address'),
            port=item.get('port')
        ).first()

        if not present:
            query = proxy_table.insert().values(
                ip_address=item.get('ip_address'),
                port=item.get('port')
            )
            session.execute(query)
            session.commit()
        return item
