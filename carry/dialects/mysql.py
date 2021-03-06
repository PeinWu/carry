from sqlalchemy import text

from carry.dialects.base import GenericSqlHelper


class MySqlHelper(GenericSqlHelper):
    def relations(self, schema):
        sql = u"""
SELECT
  KCU.TABLE_NAME,
  COLUMN_NAME,
  KCU.CONSTRAINT_NAME,
  KCU.REFERENCED_TABLE_NAME,
  KCU.REFERENCED_COLUMN_NAME
FROM
  INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU
  LEFT JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC
    ON KCU.CONSTRAINT_NAME = RC.CONSTRAINT_NAME
WHERE RC.CONSTRAINT_SCHEMA = :schema
        """
        rows = self.engine.execute(text(sql), schema=schema)
        result = []
        for row in rows:
            result.append((row.TABLE_NAME, row.REFERENCED_TABLE_NAME))
        return result

    def create_view(self, name, sql):
        sql = u"""
        CREATE OR REPLACE VIEW {name}
        AS {sql}""".format(name=name, sql=sql)
        self.engine.execute(text(sql))
