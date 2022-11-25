# Framework

This package implements a task-based framework for data transformation using Pandas and model training using Tensorflow.
A task is defined by a Python dictionary (called the task definition) containing:
* `workspace` - the workspace name (string)
* `function` - a tuple containing the module and the name of the Python function (called the job) to be executed
* any other arbitrary parameters passed by the developer
Each task is executed by calling the function with the input dictionary and the working directory path.

Tasks can be combined into a pipeline, which are sequences of tasks sharing the same artifact space (called the upstream dictionary).
The upstream dictionary is passed to the function under the `upstream` key of the input dictionary.
The framework uses the file system to pass artifacts between tasks. When a task wants to read a previous task's output, it
looks at the upstream dictionary, which contains the working directories of all previously executed tasks. A pipeline
may also contain groups of tasks that are executed concurrently (via multiprocessing).

A pipeline may start with a runtime of a previously (potentially partially) executed pipeline. This allows to skip
re-execution of tasks, if the artifacts are expected to be the same. Task functions are pure functions of their input dictionary.
A pipeline's definition can be dynamically constructed, but it must be fully determined prior to calling the framework.
 
## Environment Variables

* `APP_STORAGE_PATH` - the local path to the storage directory
* `APP_S3_BUCKET_PRIVATE` - the name of the S3 bucket where to upload the workspace