#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32.h>
#include <Servo.h>

#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;

ros::NodeHandle pressure_input;

std_msgs::Float32 depth_msg;

ros::Publisher pub('depth', &depth_msg)

float d;

void setup() {

    pressure_input.initNode();

    pressure_input.advertise(pub);

    Serial.begin(9600);
    
    delay(7000); // delay to allow the ESC to recognize the stopped signal<br />

    Wire.begin();
    
    while (!sensor.init()) 
    {
        Serial.println("Init failed!");
        delay(1000);
    }

    sensor.setModel(MS5837::MS5837_30BA);
    sensor.setFluidDensity(997); 
}
 
void loop() {

    sensor.read();
    
    d = 23 + (sensor.depth()*100);

    depth_msg.data = depth;

    pub.publish(&depth_msg);

    Serial.println(depth); 

    nh.spinOnce();
}
            
