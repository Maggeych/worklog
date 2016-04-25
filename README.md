# Worklog: A Python Work Time Logger Using SQLite

Worklog helps you __document your working time__ making use of python's _sqlite3_ module.  
Keep track of __working hours__, optionally __add short summaries__ and __print monthly time sheets__.

The corresponding database file will be created at `${HOME}/.worklog/database.db`.  
To keep multiple independent log timelines use different work names.  
Everything will be setup automatically the first time you use a new work name.

## Usage
`worklog <work name> [optional command]`

List of commands:
* `start` Starts the working ticket.
* `stop (<work notes>)` Stops the working ticket. Use `<work notes>` to summarize the work (optional).  
* `log (<month>)` Show a detailed list for `<month>` (format: _MM/YYYY_). Omitting `<month>` prints every record there is.  
* `sum <month>` Show a work summary for `<month>` (format: _MM/YYYY_).
* `add <date> <start time> <stop time> (<work notes>)` Create a work record with the given arguments.  
`<date>` _DD.MM.YYYY_  
`<start time>`, `<stop time>` _HH:MM_
* `delete <id number>` Delete the work record with the given `<id number>`.
* `help` Print help.
