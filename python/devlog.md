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

# 10-18-26 9:08 pm Session 4
Now I need to connect driver.py to logger.py with a pipe, and have logger.py use the exact required format. The logger needs ot parse the first word as action, put brackets around it, and treat the rest of the line as message. The driver needs to log startup and shutdown as well. I am considering having a new logger process subprocess.run() everytime a log needs to be written. I don't think this could work because it doesn't make sense for feasibility to have a new process for each log line. I could use procedural driver.py with global variables for children, but then it would cause a log more bugs in encryptor.py with process handlers. I could also make a driver class to spawn a logger.py instance. This seems to be the standard so I will go with it. The steps I need are to have the logger.py spawned on __init__. Then it needs to have a self.logger_proc.

# 10-18-26 9:13 pm
The logger needs to log events witht he correct format. Driver.py also needs to launch logger.py with the file driver.py is run with using Popen. It needs to log the input commands and any other actions taken.

# 10-18-26 9:22 pm
2026-10-18 21:21 [START] Logging Started.
2026-10-18 21:21 [STOP] Driver stopped.
I got the output of the logging and driver connected, but it didn't work with the other commands, only quit and starting the file. I originally had line.split() which was only recrding the "Logging" part since I was just taking parts[1]. I changed to maxsplit of 1 to fix this. The log file also was blank when I first tested it because the logger was waiting on an stdin, so f.flush() was needed after each line to fix it. Now the cipher is next to make.

# 10-18-26 9:26 pm Session 5
Now I have to do the Vigenere cipher for encryptor.py and connect it to driver.py. This will require pipes going in both directions, so stdin and stdout will have subprocess.PIPE. I need to decide whether I handle language syntax within encryptor.py or in driver.py. I think that it makes more sense in encryptor.py since the Driver.py using a subprocess to communicate creates problems with child processes if the encryptor exits. The cipher formula is pretty simple to implement with (ord(char) - ord('A') + shift amount) % 26 + ord('A'). I also need to handle the errors for invlaid input and password not set for encrypt and decrypt.

# 10-18-26 9:40 pm
I connected the Driver.py UI and pipes with encryptor.py. It was stuck not working on the password command because it had the same buffering issue from the logger I/O. I just copied how logger fixed it. Now I need to edit encryptor.py to input the cipher formula for the input. The shift amount would be key[i % len(key)] for the encryption/decryption formula. The difference between encrypt and decrypt would just be adding vs subtracting the shift.

# 10-18-26 10:07 pm
$ python encryptor.py
pass hello
RESULT
encrypt hello
RESULT OIWWC
decrypt hello
RESULT AAAAA
decrypt oiwwc
RESULT HELLO
decrypt HELLO
RESULT AAAAA
decrypt OIWWC
RESULT HELLO
quit
The encryptor file is working, but it isn't fully connect to the driver yet. 

# 10-18-26 10:28 pm
The driver is connected to the encryptor and works. I forgot to create the function to connect driver commands to the encryptor.
