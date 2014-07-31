Notes
=====

Educational documents on various topics.

= Git =

Git is a popular source code management system. Every Git working directory is a full-fledged repository, with complete history and full version tracking capabilities, not dependent on network access or a central server. In this sense, it trades off space for speed.

= GitHub =

GitHub is a web-based hosting service for source code management (SCM). It is built on the Git revision control system and offers free accounts for open source projects. According to the terms of service, if bandwidth usage of an account significantly exceeds the average of other GitHub customers, the associated file hosting service may be immediately disabled.

= Git Commands =

-> Init: The init command creates a new local repository.
-> Clone: Use clone to instantiate a working copy from a master repository. This is usually the first command employed to establish a local working hierarchy under this paradigm.
-> Add: The add command is used to add one or more files to staging. Only add pertinent files to the repository.
-> Commit: The commit command incorporates changes to your working copy of the repository.
-> Push: The push command sends changes to the master branch, typically a remote repository.
-> Pull: The pull command fetches and merges changes on the remote server to the local working directory.
-> Mergetool: Sometimes, there may be a discrepancy between the latest version of a file and its working copy on a given host. In such cases, the developer may need to take action to resolve these issues. This can be achieve through normal editing, followed by the Git add command. Alternatively, one can use the mergetool command, which initiates a visual tool.
-> Status: The status command lists the status of working files and directories.

