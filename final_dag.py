from airflow import DAG
from custom.common.email_alert import email_alert


def valid(dag_id, schedule_interval, start_date, default_args):
    if dag_id is None:
        raise ValueError('DAG ID not provided')
    if start_date is None:
        raise ValueError('Start date not provided')
    if default_args.get("owner") == "":
        raise ValueError('owner not provided')


def create_dag(dag_id, schedule_interval, start_date, default_args,
               description,
               params,
               concurrency,
               max_active_runs,
               dagrun_timeout,
               catchup,
               **kwargs):
    dag_id = dag_id.lower().replace("_", "-") + "-workflow"
    valid(dag_id, schedule_interval, start_date, default_args)
    args_list = {}
    # Update the default args with the provided arguments
    args_list.update(kwargs)
    dag = DAG(dag_id=dag_id,
              schedule_interval=schedule_interval,
              start_date=start_date,
              default_args=default_args,
              description=description,
              params=params,
              concurrency=concurrency,
              max_active_runs=max_active_runs,
              dagrun_timeout=dagrun_timeout,
              catchup=catchup,
              on_failure_callback=email_alert,
              **kwargs)
    return dag
