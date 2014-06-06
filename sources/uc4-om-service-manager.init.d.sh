#!/bin/sh
#
# %{name}       UC4 Operations Manager Service Manager for Linux.
#
# chkconfig:    2345 80 20
# description:  UC4 Operations Manager is an enterprise automation platform.
#               This init script controls the Service Manager component.

# Source function library.
. /etc/rc.d/init.d/functions

prefix="%{prefix}"
prog="%{name}"
exec="${prefix}/bin/ucybsmgr"
lockfile="/var/lock/subsys/${prog}"
pidfile="/var/run/${prog}.pid"
config="${prefix}/bin/ucybsmgr.ini"

# Source sysconfig for this daemon.
[ -e "/etc/sysconfig/$prog" ] && . "/etc/sysconfig/$prog"

start() {
    [ -x $exec ] || exit 5
    [ -f $config ] || exit 6
    echo -n $"Starting $prog: "
    daemon --pidfile "${pidfile}" $exec
    retval=$?
    echo
    [ $retval -eq 0 ] && touch $lockfile
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    killproc $prog
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $lockfile
    return $retval
}

restart() {
    stop
    start
}

reload() {
    restart
}

force_reload() {
    restart
}

rh_status() {
    # Run checks to determine if the service is running or use generic status.
    status $prog
}

rh_status_q() {
    rh_status >/dev/null 2>&1
}

case "$1" in
    start)
        rh_status_q && exit 0
        $1
        ;;
    stop)
        rh_status_q || exit 0
        $1
        ;;
    restart)
        $1
        ;;
    reload)
        rh_status_q || exit 7
        $1
        ;;
    force-reload)
        force_reload
        ;;
    status)
        rh_status
        ;;
    condrestart|try-restart)
        rh_status_q || exit 0
        restart
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload}"
        exit 2
esac

exit $?
