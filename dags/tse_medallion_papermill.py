from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

# pyrefly: ignore [missing-import]
import papermill as pm
# pyrefly: ignore [missing-import]
from airflow import DAG
# pyrefly: ignore [missing-import]
from airflow.operators.python import PythonOperator


PROJECT_ROOT = Path("/app")
NOTEBOOK_DIR = PROJECT_ROOT / "notebook"
# Saída do papermill em volume nomeado (gravável pelo airflow, independente do UID do host).
OUTPUT_DIR = Path("/opt/airflow/papermill-output")
# Scratch local do Spark (spark-warehouse/, derby.log, metastore_db/) — efêmero, fora do /app montado.
SPARK_SCRATCH = Path("/tmp/spark-scratch")

NOTEBOOK_SEQUENCE = [
    "00_setup_buckets.ipynb",
    "01_landing.ipynb",
    "02_bronze.ipynb",
    "03_silver.ipynb",
    "04_gold.ipynb",
    "05_kpis.ipynb",
]


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value)


def run_notebook(notebook_name: str, **context) -> str:
    input_path = NOTEBOOK_DIR / notebook_name
    if not input_path.exists():
        raise FileNotFoundError(f"Notebook nao encontrado: {input_path}")

    logical_date = context["logical_date"].strftime("%Y%m%dT%H%M%S")
    run_id = _safe_name(context["run_id"])
    output_folder = OUTPUT_DIR / input_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{logical_date}_{run_id}.ipynb"

    SPARK_SCRATCH.mkdir(parents=True, exist_ok=True)

    pm.execute_notebook(
        input_path=str(input_path),
        output_path=str(output_path),
        kernel_name="python3",
        cwd=str(SPARK_SCRATCH),
        parameters={
            "airflow_run_id": context["run_id"],
            "airflow_logical_date": context["logical_date"].isoformat(),
        },
    )

    return str(output_path)


with DAG(
    dag_id="tse_medallion_papermill",
    description="Executa notebooks do pipeline TSE com Papermill.",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *", # diária às 02:00
    catchup=False,
    tags=["engenharia-dados", "papermill", "tse"],
) as dag:
    previous_task = None

    for notebook_name in NOTEBOOK_SEQUENCE:
        notebook_path = NOTEBOOK_DIR / notebook_name
        if not notebook_path.exists():
            continue

        task = PythonOperator(
            task_id=f"run_{notebook_path.stem}",
            python_callable=run_notebook,
            op_kwargs={"notebook_name": notebook_name},
        )

        if previous_task:
            previous_task >> task

        previous_task = task
