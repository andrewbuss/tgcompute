import socket
import struct
import png
import math

ifile = open("srtm_ramp2.world.86400x43200.bin.cropped")
width = ord(ifile.read(1))*256+ord(ifile.read(1))
height = ord(ifile.read(1))*256+ord(ifile.read(1))
height = 100
print "Opened terrain file:", width, "by", height
print "Parsing terrain file"
terrain = [[struct.unpack(">h",ifile.read(1)+ifile.read(1))[0] for x in range(width)] for y in range(height)]
colors = [[0xa0FFFFFF for _ in range(width)] for __ in range(height)]
terraindata = ""
spoint = struct.Struct("Ifff")
scale = 4/float(max(height, width))
for y in range(height):
        for x in range(width):
            if terrain[y][x] == 0: colors[y][x]=0x22FF0000
            terraindata += spoint.pack(colors[y][x],(x+0.5)*scale-0.5,terrain[y][x]/30000.0,(y+0.5)*scale-0.5)
lookat = (0,0,0)
xres = 640
yres = 480
pointsize = 1
fps=30.0
f = 0
t = 0
camera = (math.sin(t),1,math.cos(t))
lookat = (0,-.2,0)



def sendpacket(frameinfo,f,t,camera,lookat,pointsize,xres,yres,height,width):
    print "Compiling packet"
    packet = frameinfo.ljust(32,chr(0))+struct.pack("IffffffffIIII",f,t,camera[0],camera[1],camera[2],lookat[0],lookat[1],lookat[2],pointsize,xres, yres, height,width)
    packet+=terraindata
    print "Sending packet"
    server = socket.create_connection(("192.168.0.186",7676))
    server.sendall(packet)
    print "Sent packet"
    server.setblocking(1)
    b = ""
    while len(b)<xres*yres*4: b += server.recv(xres*yres*4)
    print "Received image"
    spixel = struct.Struct("BBB")
    print "Parsing image"
    image = []
    [[image.extend(spixel.unpack_from(b,4*(y*xres+x))) for x in range(xres)] for y in range(yres)]
    print "Saving image"
    writer = png.Writer(xres,yres,alpha=False)
    outfile = open(frameinfo+"-F"+str(f)+"-T"+str(t)+"-R"+str(xres)+"x"+str(yres)+".png","wb")
    writer.write_array(outfile,image)



