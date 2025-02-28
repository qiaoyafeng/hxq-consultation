pid=$(ps aux | grep main.py  | grep -v grep | awk '{print $2}')
echo "pid:$pid"

if [ -n "$pid" ];then
  echo "kill pid:$pid"
  kill -9  $pid
fi
( nohup python main.py  1>&2 > run_log.log  & )
