import time
from commands import *
from motor import motor,device
import matplotlib.pyplot as plt
import numpy as np
from math import exp
def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
def soft_log(x,max_,k):
    return -max_/2+max_/(1+exp(-x*k))
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
    curr_deg = [-0]*100 + [0]*100
    deriv = [-1]*100 + [1]*100
    avg = [-33]*100 + [33]*100 
    fig, (ax1, ax2) = plt.subplots(1,2, sharey=False, sharex=True)
    # fig, ax1 = plt.subplots(1,1, sharey=False, sharex=True)
    line, = ax1.plot(all_vals)
    line2, = ax2.plot(curr_deg)
    plt.show(block=False)
    ax1.set_ylabel("torque current")
    ax2.set_ylabel("encoder_value")

    start = time.time()
    t_mode = False
    target = 0




    Kp = 1.75
    Kd = 2.5
    Ki = 0.5

    err = 0
    err_p = 0
    err_i = 0

    i_prev = 0
    i_delta = 0
    while True:
        test_motor.read_state2()
        test_motor.read_single_loop()
        test_motor.read_motor_encoder()
        #vals.append(test_motor.curr_i)        

        #tstart = time.time()
        num_plots = 0
        # all_vals.append(np.interp(test_motor.curr_i, [-2048,2048], [-33,33]))
        all_vals.append(test_motor.curr_i)
        # curr_deg.append(test_motor.curr_encod1)
        curr_deg.append(test_motor.curr_deg)
        all_vals.pop(0)
        curr_deg.pop(0)
        line.set_ydata(all_vals)
        line2.set_ydata(curr_deg)
        ax1.draw_artist(ax1.patch)
        ax1.draw_artist(line)


        ax2.relim()
        ax2.autoscale_view()

        ax1.relim()
        ax1.autoscale_view()

        # print(test_motor.curr_encod1)
        # print(test_motor.curr_deg)
        # print(test_motor.curr_i)
        ax2.draw_artist(ax2.patch)
        ax2.draw_artist(line2)

        avg = moving_average(all_vals, 10) 
        deriv = np.gradient(avg, 1) 


        #print(avg)
        # line2, = ax2.plot(deriv)

        # line2.set_ydata(deriv)
        # ax2.draw_artist(ax2.patch)
        # ax2.draw_artist(line2) 

        fig.canvas.draw()
        fig.canvas.flush_events()
        num_plots += 1
        #print(num_plots/5)

        time.sleep(0.001)
        curr_t = time.time()
        delta_t = curr_t - start 
        print("t_mode:", t_mode,end="\n")
        print("target: {:.2f}".format(target),end="\n")


        if delta_t < 3:
            continue
        
        target = location/803
        err = target-test_motor.curr_deg
        t_val = Kp*(err)
        i_delta = test_motor.curr_i - i_prev
        i_prev = test_motor.curr_i

        if not t_mode:
            t_mode = True
            print(err)
            print(t_val)
            test_motor.torque_control_move(int(t_val))
        if t_mode:
            print("err:{:.2f}".format(err),end="\t")            
            if abs(err) > 5 and abs(test_motor.curr_i) < 20:
                # test_motor.goto_single_loop(target,0,speed)
                delta_angle = ((target - test_motor.curr_deg))*800
                print(delta_angle)
                test_motor.increment(delta_angle,300)
            else:
                t_mode = False

        # if t_mode:
        #     err = target-test_motor.curr_deg
        #     err = soft_log(err,35,0.5)
        #     err_d = err - err_p
        #     err_i += err*0.5
        #     err_i *= 0.9
        #     # err_i *= 0.8
        #     err_p = err
        #     print("err:{:.2f}".format(err),end="\t")
        #     print("err_d:{:.2f}".format(err_d),end="\t")
        #     print("err_i:{:.2f}".format(err_i),end="\t")
        #     t_val = Kp*(err) + Kd*(err_d) + Ki*err_i;
        #     # if t_val > 100:
        #     # t_val *= 0.
        #     print("q:{:.2f}".format(t_val))
        # if t_mode and abs(err) > 1:
        #     test_motor.torque_control_move(int(t_val))
        # if t_mode and abs(err) < 1:
        #     test_motor.torque_control_move(0)
        # if t_mode and test_motor.curr_i < 50:
        #     delta_angle = int(target - test_motor.curr_deg)
        #     test_motor.increment(delta_angle,speed)
        #     t_mode = False

        # if(deriv[i] > thresh or deriv[i] < thresh):
            
        #     location = location + int(deriv[i]) 
        #     test_motor.goto_single_loop(location,0,speed)

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
    # uca = device("/dev/tty.usbserial-140")
    uca = device("/dev/ttyUSB0")
    test_motor = motor(3,uca.port())
    try:
        detect_touch()
    except Exception as e:
        print(e)
        test_motor.motor_disarm()



    