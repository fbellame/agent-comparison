from autogenstudio import WorkflowManager
# load workflow from exported json workflow file.
workflow_manager = WorkflowManager(workflow="./workflow_stock_analysis_ReaAct_workflow.json")

# run the workflow on a task
task_query = """first for a given ticker: NVDA fetch the data using the yahoo finance skill 
then get warren buffett's investment principles by opening
the file warren_buffet_investement_principles.txt with the read file skill
then you provide a comprehensive analysis of the ticker
write short and concise the pros why warren buffett would invest in
this company and the cons why he wouldn't
then summarize the company evaluation and provide a recommendation
then you give a warren buffet buy recomendation from 0 to 10 (10 is best)
finally write the result to the file 
stock_analysis.md using write_file skill
expected_output:
- Pros why Warren Buffett would invest in this company
- Cons why Warren Buffett wouldn't invest in this company
- Company Evaluation Summary
- Warren Buffet Buy Recommendation"""

workflow_manager.run(message=task_query)