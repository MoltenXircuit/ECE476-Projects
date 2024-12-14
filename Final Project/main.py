import _thread
from micropython import const
import core_1
import core_2

N = const(3)
key_scaled_state = ([0] * N)




_thread.start_new_thread(core_2.main,(key_scaled_state,N))
#core_2.main(key_scaled_state)
#_thread.start_new_thread(core_1.main,(key_scaled_state))
core_1.main(key_scaled_state)
