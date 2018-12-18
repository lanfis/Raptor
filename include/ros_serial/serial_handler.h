#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <time.h>
#include "boost/asio.hpp"
#include "boost/bind.hpp"

#include <iostream>
#include <fstream>

using namespace std;
using namespace boost::asio;

class serial_handler
{
  private:
    io_service iosev_;
    boost::shared_ptr< serial_port > sp_;
    boost::system::error_code ec_;
    
    bool is_open_ = false;
    static const int buffer_size_ = 1024;
    char buffer_[buffer_size_];
    string buffer_packets = "\0";
    string tmp_packet;
    
    string port_name_ = "/dev/ttyACM0";
    int baudrate_ = 57600;

  public:
    bool is_open(){ return is_open_; };
    void set_port(string port){ port_name_ = port;};
    string get_port(){return port_name_;};
    void set_baudrate(int baudrate){baudrate_ = baudrate;};
    int get_baudrate(){return baudrate_;};
    
    bool read_port(vector< string >& packet, string deli="\n")
    {
        if(!this -> sync_read_port(tmp_packet, true))
            return false;
        buffer_packets.append(tmp_packet);
        while(buffer_packets.length() > 0)
        {
            if(buffer_packets.find(deli) > buffer_size_)
                break;
            packet.insert(packet.begin(), buffer_packets.substr(0, buffer_packets.find(deli)/* + deli.length()*/));
            buffer_packets.erase(0, buffer_packets.find(deli) + deli.length());
        }
        return true;
    }
    bool write_port(string& packet)
    {
        return this -> sync_write_port(packet);
    }
    
    bool sync_read_port(string& packet, bool is_auto_clear=false)
    { 
        if(!is_open()) return false; 
        int res = sp_ -> read_some(buffer(&buffer_, buffer_size_), ec_);
        if(res == 0)
        {
            if (ec_)
                cout << "serial reading error : " << ec_.message().c_str() << endl; 
            return false;
        }
        string buffer_string(buffer_, res);
        if(is_auto_clear) 
            packet.clear();
        packet.append(buffer_string);
        return true; 
    };
    
    bool sync_write_port(string& packet, bool is_auto_clear=false)
    {
        if(!is_open()) return false; 
        if(sp_ -> write_some(buffer(packet.c_str(), packet.length()), ec_) > 0)
        {
            if(is_auto_clear) 
                packet.clear();
            return true;
        }
        else
        {
            if (ec_)
                cout << "serial writing error : " << ec_.message().c_str() << endl; 
            return false;
        }
    };
    
    bool open_port();
    bool open_port(string port_name, int baudrate){ set_port(port_name); set_baudrate(baudrate); return open_port(); };
    bool close_port(){ if(!is_open_) return false; if(sp_ != NULL) {sp_ -> close(); /*delete sp_;*/} is_open_ = false; return true;};
    
    
    serial_handler();
    ~serial_handler();
};

serial_handler::serial_handler()
{
}

serial_handler::~serial_handler()
{
    close_port();
}

bool serial_handler::open_port()
{
    close_port();
    //sp_ = boost::shared_ptr< serial_port >(new serial_port(iosev_, port_name_));
    sp_ = boost::shared_ptr< serial_port >(new serial_port(iosev_));
    sp_ -> open(port_name_, ec_);
    if (ec_) 
    {
        cout << "error : port open failed...com_port_name = "
            << port_name_ << ", e = " << ec_.message().c_str() << endl; 
        is_open_ = false;
        return false;
    }
    sp_ -> set_option(serial_port::baud_rate(baudrate_));
    sp_ -> set_option(serial_port::flow_control(boost::asio::serial_port_base::flow_control::none));
    sp_ -> set_option(serial_port::parity(boost::asio::serial_port_base::parity::none));//none, odd, even
    sp_ -> set_option(serial_port::stop_bits(boost::asio::serial_port_base::stop_bits::one));//one, onepointfive, two
    sp_ -> set_option(serial_port::character_size(8));
    is_open_ = true;
    return true;
}

