
def parse_angle(frame):
    if not len(frame) == 13:
        return
    print(frame)
    [ print(hex(i)) for i in frame ]
    # print([(i,hex(j)) for i,j in enumerate(frame)])
    if frame[4] == 0x90: 
        print("Position:", int.from_bytes(frame[6:8],byteorder='big', signed=False), end = '\t')
        print("Raw:", int.from_bytes(frame[8:10],byteorder='big', signed=False), end = '\t')
        print("Zero:", int.from_bytes(frame[10:12],byteorder='big', signed=False), end = '\t')
    if frame[4] == 0x94: 
        print("VAL:", frame[10] + frame[11] * 255 , end = '\t')
    print()
