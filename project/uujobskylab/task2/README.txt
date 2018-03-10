A solution can be to hookup the firstaction section of a logrotate config file

The logic that checks if is time to rotate or not is implemented in check_time.sh

The config file is xrotate.conf

The key idea is to rotate hourly and check if time mod period is zero
period is 4 in this case
It is also possible to shift time
