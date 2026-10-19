# 10-18-26 7:45 pm Session 1
Looking at project description of Project 1 and starter files. I need a logger, encryptor, and driver that connects them with pipes. I need to have the pieces talk to each other. I am thinking that the driver could opent he log file directly and append to it says few moving parts are needed. However, this wouldn't be using pipes properly so I can't use it. I need to have the driver launch logger as a seaparate process to put lines into stdin. Cpu.py launches child process, then holds onto its std file streams, pushes line commands, flushes the stream, and reads for response. I need to iether format messages as serialized JSON strings or whitspace-delmiited tokens. JSON works with structured payloads well, but plain text tokens will work better for parsing issues.

# 10-18-26 8:00 pm
I initialized the repository into github. I will need logger.py, encryptor.py, and driver.py, so I created the files. I next will need to create the basic input and output for the files. This will be easier to test than pipes without input nor output.

# 10-18-26 8:12 pm Session 2
The first step is to make a command loop in driver.py for the commands. The interface int he termanl needs to work well before background processes happen so that testing is more clear. The menu needs to have password, encrypt, decrypt, history, and quite. It must continuously prompt until quit is submitted. I am wondering whether I should have a separate function for each command or whether they should go in a switch/elif chain. For now, I will just use an elif chain.

# 10-18-26 8:37 pm
I created the basic driver.py commands for the user to input. It also makes sure that the user runs the file with the log file. I needed to add lowercase and strip so that caps and spaces don't affect the command the user gives. Next, I need to create the I/O loops for logger.py and encryptor.py.