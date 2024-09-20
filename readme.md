## Cowrywise Backend Task

Here is a repo that houses Frontend and Backend API services that attends to the task provided here url[https://coda.io/d/Backend-Assessment_deRE9tB1Cx_/Backend-Assessment_sui482LU#_lu85BJGs]


The Means of communication between the two application is RabbitMQ. The reason for this approach was to use the Fire and forget approach, such that when a message is published from a queue it stores in the queue just and only when the consumer is live it can recieve and acknowledge the message. 


The Apps (Frontend, Backend) are built with FastAPI, and a make file is available to make commands on the fly. The makefiles are in the respective sub_repos.

The entrypoint of the server is root.app and the command is `make start_server`, there is also tests available in the tests folder.
Tests can be run using `make all-test`.


There are unit tests, while the integration tests are being updated. 

