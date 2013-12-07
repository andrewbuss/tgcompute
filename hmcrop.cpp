#include <gzstream.h>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MIN_LAT atoi(argv[1])
#define MAX_LAT atoi(argv[2])
#define MIN_LONG atoi(argv[3])
#define MAX_LONG atoi(argv[4])
#define MIN_X int(floor(43200+MIN_LONG/0.004166667))
#define MAX_X int(ceil(43200+MAX_LONG/0.004166667))
#define MIN_Y int(floor(21600-MAX_LAT/0.004166667))
#define MAX_Y int(ceil(21600-MIN_LAT/0.004166667))

int main(int argc, char** argv){
  if(argc!= 7){
    printf("Usage: hmcrop min_lat max_lat min_long max_long input output\n");
    return -1;
  }
  printf("Min X: %i\n",MIN_X);
  printf("Max X: %i\n",MAX_X);
  printf("Min Y: %i\n",MIN_Y);
  printf("Max Y: %i\n",MAX_Y);
  int npoints = 0;
  printf("Cropping compressed binary file \n");
  igzstream in(argv[5]);
  std::ofstream out(argv[6]);
  out.put((MAX_X-MIN_X)/256);
  out.put((MAX_X-MIN_X)%256);
  out.put((MAX_Y-MIN_Y)/256);
  out.put((MAX_Y-MIN_Y)%256);
  char inbuffer[86400*2];
  for(int y=0;y<MAX_Y;y++){
    in.read(inbuffer,86400*2);
    if(y>=MIN_Y && y<=MAX_Y){
      for(int x=MIN_X*2;x<MAX_X*2;x+=2){
	    npoints++;
	    out.put(inbuffer[x]);
	    out.put(inbuffer[x+1]);
      }
    }
  }
  out.close();
  in.close();
  return 0;
}
