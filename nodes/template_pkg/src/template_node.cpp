#include "rclcpp/rclcpp.hpp"
#include <string>

class Template : public rclcpp::Node {

public:
    Template() : Node("template_node")
    {
        // TODO: create ROS subscribers and publishers
    }

private:

};
int main(int argc, char ** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Template>());
    rclcpp::shutdown();
    return 0;
}