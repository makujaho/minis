<?php

// Increase limit. This might not be necessary due to the fact that some 
// PHP binaries don't add the time from system() calls
set_time_limit(3600);

// Line break shortcut
define('B', '<br>');

// This is the configuration for your database. You need to specify everything
// If you don't know the host it is propably 'localhost'
define('DB_HOST', '');
define('DB_USER', '');
define('DB_NAME', '');
define('DB_PASS', '');
define('DB_PORT', '3306');

// You may have to change this to an existing directory. Be aware that you 
// *always* want to have your dumps above the document root of your server, 
// everything else is a security issue
define('OUTPUT_FILE', '../tmp/db-dump-' . DB_USER . '.sql');

// Test if the file already exists
if (file_exists(OUTPUT_FILE)) {
    passthru('tail -1 ' . OUTPUT_FILE);
    die('<br>SQL already exists. If the line above states "completed" your '. 
        'database dump is complete and can be downloaded.');
}

// Dump the database
system('/usr/bin/mysqldump --opt --host=' . DB_HOST . ' --user=' . 
            DB_USER . ' --password=' . DB_PASS . ' ' . DB_NAME . ' > ' .
            OUTPUT_FILE
        );

// Print the path to the database and the last line of the dump(which should
// be something like 'completed')
echo OUTPUT_FILE . B;
passthru('tail -1 ' . OUTPUT_FILE);
