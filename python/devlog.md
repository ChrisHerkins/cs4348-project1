# 10-18-26 7:45 pm Session 1
Looking at project description of Project 1 and starter files. I need a logger, encryptor, and driver that connects them with pipes. I need to have the pieces talk to each other. I am thinking that the driver could opent he log file directly and append to it says few moving parts are needed. However, this wouldn't be using pipes properly so I can't use it. I need to have the driver launch logger as a seaparate process to put lines into stdin. Cpu.py launches child process, then holds onto its std file streams, pushes line commands, flushes the stream, and reads for response. I need to iether format messages as serialized JSON strings or whitspace-delmiited tokens. JSON works with structured payloads well, but plain text tokens will work better for parsing issues.

# 10-18-26 8:00 pm
I initialized the repository into github. I will need logger.py, encryptor.py, and driver.py, so I created the files. I next will need to create the basic input and output for the files. This will be easier to test than pipes without input nor output.

# 10-18-26 8:12 pm Session 2
The first step is to make a command loop in driver.py for the commands. The interface int he termanl needs to work well before background processes happen so that testing is more clear. The menu needs to have password, encrypt, decrypt, history, and quite. It must continuously prompt until quit is submitted. I am wondering whether I should have a separate function for each command or whether they should go in a switch/elif chain. For now, I will just use an elif chain.

# 10-18-26 8:37 pm
I created the basic driver.py commands for the user to input. It also makes sure that the user runs the file with the log file. I needed to add lowercase and strip so that caps and spaces don't affect the command the user gives. Next, I need to create the I/O loops for logger.py and encryptor.py.

# 10-18-26 8:42 pm Session 3
I am moving devlog.md into python folder for now since it is easier to commit the files together with git add . instead of writing the devlog.md file every commit. I need to create the I/O for logger.py and encryptor.py. This needs to be set up before the pipes since they are much less complicated. For logger.py, I need to take the log file name from the program calling. It then needs to read from stdin and write them to the file until quit is read. I can do the encryptor.py right now, but it will cause too much bug testing, so I want ot keep it within logger.py for now. I could use sys.stdin.read(), but that doesn't make sense since logger and encryptor are supposed to be long-running processes that read per line rather than all lines. I'll use a simple sys.stdin iteration. I will set it up so that I run logger.py directly instead of calling it from driver.py.

# 10-18-26 8:49 pm
The quit isn't case sensitive so I need to add that, but also it is successfully writing to the end of log.txt which I used for testing. Now I need to do encryptor.py. I am keeping it separate from the other files for bug testing sake. It is fairly similar to logger.py's code, so it won't be too bad. I will split lines on spaces to extract command and argument, have the program print an acknowledgement for the commands, and give the same error for unknown commands that driver has.

# 10-18-26 9:04 pm
The encryptor.py file is working with tests. They have the commnd receiving and the quitting working. It recognizes the input as well when taking in commands.