# Databricks notebook source
from databricks.connect import DatabricksSession

from arxiv_curator.config import load_config
from pkgscout.ingest import fetch_all

# COMMAND ----------

cfg = load_config("project_config.yml", "dev")
spark = DatabricksSession.builder.profile("student-bot-4").serverless(True).getOrCreate()

# COMMAND ----------

rows = fetch_all()
df = spark.createDataFrame(
    rows, "name string, version string, summary string, release_date string, description string"
)
table = f"{cfg.catalog}.{cfg.schema}.pypi_packages"
df.write.mode("overwrite").saveAsTable(table)
print(table, spark.table(table).count())
