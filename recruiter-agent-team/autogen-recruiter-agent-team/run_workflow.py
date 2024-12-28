from autogenstudio import WorkflowManager
# load workflow from exported json workflow file.
workflow_manager = WorkflowManager(workflow="./workflow_xxxx.json")

# run the workflow on a task
task_query = """PROMPT"""

workflow_manager.run(message=task_query)