import time
from commands import *
from motor import motor,device
import matplotlib.pyplot as plt
import numpy as np

def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def detect_touch(): 
    speed = 7200 
    location = 0

    test_motor.motor_disarm()

    time.sleep(1)

    print("current location: ", test_motor.read_single_loop())
    location = int(input("enter location\n")) 
    if (location < 0 or location > 360):
        location = int(input("enter valid location\n"))

    test_motor.motor_arm()

    location = location * 803

    time.sleep(0.1)
    
    test_motor.goto_single_loop(location,0,speed)

    time.sleep(0.01)
    i = 0
    pushed = False
    pulled = False 
    thresh = 0.1

    all_vals = [-33]*100 + [33]*100
    deriv = [-1]*100 + [1]*100
    avg = [-33]*100 + [33]*100 
    fig, (ax1, ax2) = plt.subplots(1,2, sharey=False, sharex=True)
    line, = ax1.plot(all_vals)
    plt.show(block=False)
    ax1.set_ylabel("torque current")
    ax2.set_ylabel("moving average of current")

    while True:
        test_motor.read_state2()
        #vals.append(test_motor.curr_i)        

        #tstart = time.time()
        num_plots = 0
        all_vals.append(np.interp(test_motor.curr_i, [-2048,2048], [-33,33]))
        all_vals.pop(0)
        line.set_ydata(all_vals)
        ax1.draw_artist(ax1.patch)
        ax1.draw_artist(line)

        avg = moving_average(all_vals, 10) 
        deriv = np.gradient(avg, 1) 

        #print(avg)
        line2, = ax2.plot(deriv)

        line2.set_ydata(deriv)
        ax2.draw_artist(ax2.patch)
        ax2.draw_artist(line2) 

        fig.canvas.update()
        fig.canvas.flush_events()
        num_plots += 1
        #print(num_plots/5)

        time.sleep(0.01)

        if(deriv[i] > thresh or deriv[i] < thresh):
            
            location = location + int(deriv[i]) 
            test_motor.goto_single_loop(location,0,speed)

        '''
        if(deriv[i] >= thresh):
            pushed = True
            pulled = False
            print("pushed: ", pushed) 
        
        elif (deriv[i] <= -(thresh) and pushed):
            pushed = False
            pulled = False
            print("pushed: ", pushed) 

        if (deriv[i] <= -(thresh)): 
            pulled = True
            pushed = False
            print("pulled: ", pulled) 
        
        elif (deriv[i] >= thresh and pulled): 
            pulled = False
            pushed = False
            print("pulled: ", pulled)
        '''

        i =+ 1
        


        

    

    '''
    for i in range(1000):
        test_motor.read_state3()
        #sleep(0.1)
    '''

    # test_motor.goto_single_loop(0, 1, speed)

if __name__ == "__main__":  
    #vals = []
    #countArr = []
    uca = device("/dev/tty.usbserial-140")
    test_motor = motor(3,uca.port())
    try:
        detect_touch()
    except:
        test_motor.motor_disarm()



    