import typing as T
import pandas as pd

from baserow.contrib.database.table.models import Table
from baserow.contrib.database.rows.handler import RowHandler


class ServerFileUploadHandler:
    def get_table_by_name(self, name: str):
        table = Table.objects.filter(name=name).first()
        if table is None:
            raise ValueError(f"{name} table does not exist")
        return table

    def get_servers_table(self):
        return self.get_table_by_name('Servers')

    def get_domains_table(self):
        return self.get_table_by_name('Domains')

    def run_enricher_on_servers(self, servers: T.List):
        print(servers)
        simple_dataframe = pd.DataFrame([1, 2, 3], columns=['name'])
        return (simple_dataframe, simple_dataframe)

    def upload_dict_to_table(self, user, row: T.Dict, table: Table):
        field_id_to_value = {RowHandler().field_id_by_name(field): value for field, value in row.items()}
        RowHandler().create_row(user=user, table=table, values=field_id_to_value)

    def upload_df_to_table(self, user, dataframe: pd.DataFrame, table: Table):
        for _, row in dataframe.iterrows():
            self.upload_dict_to_table(user, dict(row), table)

    def add_properties_to_df(self, dataframe: pd.DataFrame, properties: T.Dict[str, str]):
        pass

    def create_upload_identifier(self, name: str, username: str, exploit: str):
        pass

    def upload(self, servers: T.List, user, name: str, exploit: str):
        print(servers)
        first_row_of_servers_csv = servers
        enriched_domains, enriched_servers = self.run_enricher_on_servers(
            first_row_of_servers_csv)
        upload_identifier = self.create_upload_identifier(name, user.username, exploit)

        for dataframe in [enriched_domains, enriched_servers]:
            self.add_properties_to_df(dataframe, {
                'upload': upload_identifier,
                'username': user.username
            })

        self.upload_df_to_table(user, enriched_domains, self.get_domains_table())
        self.upload_df_to_table(user, enriched_servers, self.get_servers_table())
