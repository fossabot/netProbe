import redis
import time

def connect():
   global backOff
   global r

   while(True):
      print("connect to redis")
      r = redis.Redis(db=1, max_connections=1, socket_timeout=2)
      try:
         r.ping()
         break

      except redis.ConnectionError, e:
         print("ERROR on redis : {}, try in {:.2f}".format(e.message, backOff))
         time.sleep(backOff)
         backOff = backOff*1.5
         
   backOff = 1


def process():
   global r
   print(r.get('a'))
   r.incr('a')
   time.sleep(1)

def main():
   connect()

   while(True):
      try:
         process()

      except redis.ConnectionError, e:
         print("ERROR on redis : {}, try in {}".format(e.message, backOff))
         connect()

      except redis.TimeoutError, e:
         print("Timeout on redis : {}".format(e.message))
         time.sleep(1)

backOff = 1

main()
