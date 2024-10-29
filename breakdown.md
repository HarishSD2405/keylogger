# basic keylogger
- count : This variable counts the number of keystrokes recorded. 
    - It’s used to track when to save the recorded keystrokes to the log file.
- keys : This list stores each keystroke as it’s recorded. 
    When a certain number of keystrokes are reached (in this case, immediately after each keystroke due to count >= 0), they are written to the file, and keys is reset.

- on_press - used as a handler with the Listener class from the pynput library, which is listening for keyboard events
    - handler is a function designed to be trigerred to respond to a specific event (in this case a keystroke)\
    - 'key' variable holds the value of the key that was pressed like 'a' or Key.space

# sending email
- MIMEMultipart - used to create an email with multiple parrts like text, html, attachments as separat components into one email
- setting headers - define the structure and format of the mail
    - from - who from
    - to - who to
    - subject - one line subject

- MIMEBase - used to represent binary data in emails
    - application is the generic application type
    - octet-stream is subtype of binary data whcih says it can be any type of binary file
        - used for file types that dont fall under more specific categories like text, image, audio
    - to be read by clients in various formats

# computer information
- why processor info - how powerful the machine is or if this processor has any vulnerabilities
- why private ip - if on univerity network for example, you can target the victim specifically as public ip would be the same

# microphone
- why sampling frequency


# timer
how it works is in a 15 second interval, if esc hasnt been pressed then it automatically stop listening and does the other operations of the iteration
inside the listener 'if currentTime > stopTime' is to make sure the keylogger doesnt go on for longer than 15 seconds otherwise keylogger delays the others
outside the listener 'if currentTime > stopTime' is to make sure all other operations are logged at the end of every 15 seconds otherwise keylogger will stop but post key logger ops will not happen

# encryption
why encrypt - to ensure victim doesnt get suspicious of all the log files created


## LATER UPDATES
i want this to write into file everytime something new is copied into clipboard while running   
better way to automate the whole process so i wont have to manually generate a key, decrypt files
