#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32.h>

ros::NodeHandle pressure_sensor;



ros::Publisher pub('depth', &depth);

void setup()
{
    downMotion.initNode();
    downMotion.advertise(pub);
    downMotion.subscribe(sub);
}

void loop()
{

}
