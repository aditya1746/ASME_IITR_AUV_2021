#include <ros.h>
#include <std_msgs/String.h>
#include <sauvc_qualification/distance_and_center.h>

int d,x,y;

ros::NodeHandle controller;

void callback (const sauvc_qualification::distance_and_center& msg)
{
    d = msg.distance;
    x = msg.centerx;
    y = msg.centery;

    Serial.println(d);

    if (depth<0.8) move_down();
    else if (depth>1.2) move_up();
    else decide();
}

void decide()
{
    if(d>=1.95 && d<=2.1)
    {
        // go 3 meters and then come at the top
    }
    else move_forward()

    if (d!=0 && x<-5 || x>5)
    {
        
    }
}

ros::Subscriber<sauvc_qualification::distance_and_center> sub('gate_pos',&callback)

void setup()
{
    controller.initNode();
    controller.subscribe(sub);
    Serial.begin(9600);
}

void loop()
{
    nh.spinOnce();
    delay(500);
}
