import typing as T
import pandas as pd
from django.utils import timezone

from baserow.contrib.database.table.models import Table
from baserow.contrib.database.rows.handler import RowHandler


class ServerFileUploadHandler:
    def get_table_by_name(self, name: str) -> Table:
        table = Table.objects.filter(name=name).first()
        if table is None:
            raise ValueError(f"{name} table does not exist")
        return table

    def get_servers_table(self):
        return self.get_table_by_name('Servers')

    def get_domains_table(self):
        return self.get_table_by_name('Domains')

    def run_enricher_on_servers(self, servers: T.List):
        simple_dataframe = pd.DataFrame([1, 2, 3], columns=['name']).copy()
        return (simple_dataframe, simple_dataframe)

    def upload_dict_to_table(self, user, row: T.Dict, table: Table):
        RowHandler().update_or_create_named_row(user=user, table=table, values=row, attribute_names=True)

    def upload_df_to_table(self, user, dataframe: pd.DataFrame, table: Table):
        for _, row in dataframe.iterrows():
            self.upload_dict_to_table(user, dict(row), table)

    def add_properties_to_df(self, dataframe: pd.DataFrame, properties: T.Dict[str, str]):
        print(dataframe)
        for property, value in properties.items():
            if property not in dataframe:
                dataframe.insert(0, property, value)
        return dataframe

    def create_upload_identifier(self, name: str, username: str, exploit: str):
        uploads_table = self.get_table_by_name('Uploads').get_model(attribute_names=True)

        creation_date = timezone.now()
        upload_record = uploads_table.objects.create(name=name,
            user=username,exploit=exploit,uploaddate=creation_date)
        return upload_record

    def upload(self, servers: T.List, user, name: str, exploit: str):
        first_row_of_servers_csv = servers
        enriched_domains, enriched_servers = self.run_enricher_on_servers(
            first_row_of_servers_csv)
        upload_identifier = self.create_upload_identifier(name, user.username, exploit)

        domains_dataframe_with_metadata = self.add_properties_to_df(enriched_domains, {
            'upload': upload_identifier, 'username': user.username})
        servers_dataframe_with_metadata = self.add_properties_to_df(enriched_servers, {
            'upload': upload_identifier, 'username': user.username})

        self.upload_df_to_table(user, domains_dataframe_with_metadata, self.get_domains_table())
        self.upload_df_to_table(user, servers_dataframe_with_metadata, self.get_servers_table())