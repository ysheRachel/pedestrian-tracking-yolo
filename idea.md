
# idea 1: reduce miss detection by using consective image correlation  
``` if a person in previous frame is not assigned to any one in current frame  
 if this person has a track longer than t1, and its position in the middle  
(check miss detection)  
 while (w<W)  (W is the correlation window size)  
    assign the previous frame with the current frame no.+w              
if this person can be assigned (according to kalman filter IOU+ appearence likelihood)  
miss detection=true  
if miss detection=true  
    a rect is draw by interpolating, and assign this rect to the previous track
```



# idea 2: reduce false alarm 
  if track length is shorter than t2 and  no likelihood in that track is larger than r1
  then false alram=true
       delete this track


# idea 3: calculate the correlation window
  use the bench mark algorithm deep sort first
  
